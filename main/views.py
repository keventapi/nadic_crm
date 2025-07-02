from django.shortcuts import render, redirect, get_object_or_404
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

# Create your views here.

#login required


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