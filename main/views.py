from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Sales
from .forms import AuthForm, SignupForm, ProductForm, ProductSale, EditProductForm
from . import auth
from django.core.exceptions import ValidationError
from .decorators import loged_out_required, super_user_required
from . import utilits
from django.contrib import messages
from django.contrib.auth.models import User
import json

# Create your views here.
@login_required
def index(response):
    products = Product.objects.all()
    context = {'products': products}
    return render(response, 'index.html', context)

@login_required
def profile(response, user_id):
    owner = get_object_or_404(User, id=user_id)
    products = Product.objects.filter(owner=owner)
    return render(response, 'profile.html', context={'product': products})

@super_user_required
def faturamento(response):
    vendas = Sales.objects.all()
    faturamento = 0
    for i in vendas:
        faturamento += i.total_product_sale
    return render(response, 'faturamento.html', context={'faturamento': faturamento})

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('index')
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'user_product_manager.html', context)

@login_required
def view_product(response, product_id):
    product = get_object_or_404(Product, id=product_id)
    if response.method == "POST":
        action = response.POST.get('action')
        if action == "comprar":
            form = ProductSale(response.POST, product=product)
            if form.is_valid():
                product.product_stock -= form.cleaned_data['quantity']
                product.save()
                sale = form.save(commit=False)
                sale.product = product
                sale.price_at_sale = product.product_price
                sale.save()
                messages.success(response, "compra realizada com sucesso")
    else:
        form = ProductSale(product=product)
    product_info = get_object_or_404(Product, id=product_id)
    product_context = {'id': product_id, 
                       'name': product_info.product_name,
                       'image': product_info.product_image,
                       'price': f'{product_info.product_price}R$',
                       'stock': product_info.product_stock,
                       'description': product_info.product_description,
                       'type': product_info.product_type}
    product_owner_status =  product.owner == response.user
    return render(response, 'product_view.html', {'product': product_context, 'form': form, 'owner': product_owner_status})

@login_required
def edit_product(response, product_id):
    product_info = get_object_or_404(Product, id=product_id)
    if product_info.owner != response.user:
        return redirect('index')
    if response.method == 'POST':
        action = response.POST.get('action')
        if action == "submit":
            form = EditProductForm(response.POST, response.FILES, instance=product_info)
            if form.is_valid():
                form.save()
                return redirect('index')
        if action == "delete":
            product_info.delete()
            return redirect('index')
    else:
        form = EditProductForm(instance=product_info)
    context = {"form": form}
    return render(response, 'product_edit.html', context)

@loged_out_required
def login_page(response):
    if response.method == "POST":
        form = AuthForm(response.POST)
        if form.is_valid() and auth.login_user(response, form.cleaned_data['username'], form.cleaned_data['password']):
            return redirect('index')
    else:
        form = AuthForm()
    context = {"form": form}
    return render(response, "login.html", context)

@loged_out_required
def signup_page(response):
    if response.method == "POST":
        form = SignupForm(response.POST)
        if form.is_valid() and auth.signup_user(response, form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password']):
            return redirect('index')
    else:
        form = SignupForm()
    context = {'form': form}
    return render(response, 'signup.html', context)


def auto_complete(response):
    print('autocomplete')
    if response.method == "POST":
        data = json.loads(response.body.decode('utf-8'))
        product_name = data.get("value")
        if product_name is not None:
            products = Product.objects.filter(product_name__icontains=product_name)
            product_list = [{'name': p.product_name, 'id': p.id} for p in products]
            return JsonResponse({'query': product_list})
        return