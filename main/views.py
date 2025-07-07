from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Sales, Cart, CartItems, Comissions
from .forms import AuthForm, SignupForm, ProductForm, ProductSale, EditProductForm, ComissionForm
from . import auth
from django.core.exceptions import ValidationError
from .decorators import loged_out_required, super_user_required
from . import utilits
from django.contrib import messages
from django.contrib.auth.models import User
import json

#adicionar um trhottle para o evento de autocomplete
#add blacklist, add athomic pra save entre duas tabelas
# Create your views here.



#super user required

@super_user_required
def faturamento(response):
    vendas = Sales.objects.all()
    faturamento_total, faturamento_empresa = utilits.calcular_faturamento(vendas)
    return render(response, 'faturamento.html', context={'faturamento_total': faturamento_total, 'faturamento_empresa': faturamento_empresa})

@super_user_required
def create_staff_account(response):
    if response.method == "POST":
        form = SignupForm(response.POST)
        if form.is_valid() and auth.signup_super_user(response, form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password']):
            messages.success(response, "conta de funcionario criado com sucesso")
        else:
            messages.warning(response, "erro na criação da conta de funcionario, cheque se não esta colidindo com alguma outra conta")
    else:
        form = SignupForm()
    return render(response, 'signup.html', context={"form": form})

@super_user_required
def comission_update(response):
    if response.method == "POST":
        form = ComissionForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = ComissionForm()
    return render(response, 'comission_update.html', {'form': form})

#login required

@login_required
def index(response):
    products = Product.objects.filter(product_visibility = True)
    context = {'products': products, 'user': response.user.id}
    return render(response, 'index.html', context)

@login_required
def profile(response, user_id):
    owner = get_object_or_404(User, id=user_id)
    products = Product.objects.filter(owner=owner, product_visibility=True)
    return render(response, 'profile.html', context={'product': products})

@login_required
def view_cart(response):
    cart = Cart.objects.get(cart_owner=response.user)
    cart_items = cart.items.filter(product__product_visibility = True)
    if response.method == "POST":
        action = response.POST.get('action')
        if action == "comprar tudo":
            utilits.handle_sales_from_cart(cart_items)
            cart_items.delete()
            messages.success(response, 'compras realizadas com sucesso')
    return render(response, 'cart.html', {'cart_itens': cart_items})

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'user_product_manager.html', {'form': form})


@login_required
def view_product(response, product_id):
    product = get_object_or_404(Product, id=product_id)
    if response.method == "POST":
        action = response.POST.get('action')
        form = ProductSale(response.POST, product=product)
        
        if action == "comprar":
            if form.is_valid():
                cleaned_quantity = form.fields['quantity'].clean(response.POST.get('quantity'))
                utilits.handle_unique_sells(product, cleaned_quantity)
                messages.success(response, "comprado com sucesso")
            
        elif action == "carrinho":
            cart = Cart.objects.get(cart_owner=response.user)
            if form.is_valid():
                chekcer = CartItems.objects.filter(product=product, cart=cart)
                if len(chekcer) == 0:
                    item = CartItems.objects.create(
                        product=product, 
                        quantity=form.cleaned_data['quantity'], 
                        cart=cart
                    )
                else:
                    item = CartItems.objects.get(product=product)
                    item.save()
                messages.success(response, "produto adicionado ao carrinho com sucesso")

    else:
        form = ProductSale(product=product)
        
    product_context = {'id': product_id, 
                       'name': product.product_name,
                       'image': product.product_image,
                       'price': f'{product.product_price}R$',
                       'stock': product.product_stock,
                       'description': product.product_description,
                       'type': product.product_type}
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
                messages.success(response, 'produto editado com sucesso')
                return redirect('seller_dashboard')
        if action == "delete":
            product_info.product_visibility = False
            product_info.save()
            messages.success(response, 'produto deletado com sucesso')
            return redirect('seller_dashboard')
        if action == "cancel":
            return redirect('seller_dashboard')
    else:
        form = EditProductForm(instance=product_info)
    context = {"form": form}
    return render(response, 'product_edit.html', context)

@login_required
def seller_dashboard(response):
    products_list = Product.objects.filter(owner=response.user)
    faturamento = 0
    if len(products_list) > 0:
        for products in products_list:
            sales = Sales.objects.filter(product=products)
            for sale in sales:
                faturamento += sale.owner_net_earning
        
    return render(response, 'seller_dashboard.html', {'products': products_list, 'faturamento': faturamento})


#loged out required

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



#funcionalidades

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