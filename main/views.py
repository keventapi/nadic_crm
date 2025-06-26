from django.shortcuts import render, redirect, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import AuthForm, SignupForm, ProductForm
from . import auth
from .decorators import loged_out_required


# Create your views here.
@login_required
def index(response):
    products = Product.objects.all()
    context = {'products': products}
    return render(response, 'index.html', context)

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'user_product_manager.html', context)

@login_required
def view_product(response, product_id):
    product_info = get_list_or_404(Product, id=product_id)[0]
    product_context = {'title': product_info.product_name,
                       'image': product_info.product_image,
                       'price': product_info.product_price,
                       'description': product_info.product_description,
                       'type': product_info.product_type}
    print(product_context)
    return render(response, 'product_view.html', {'product': product_context})

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


