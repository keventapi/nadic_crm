from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Cart

def check_cart_instance(user):
    Cart.objects.get_or_create(cart_owner=user)


def authentication(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user:
        check_cart_instance(user)
    return user 

def login_user(request, username, password):
    user = authentication(request, username, password)
    if user:
        login(request, user)
        print('logado')
    return user

def signup_super_user(request, username, email, password):
    user = User.objects.create_superuser(username, email, password)
    check_cart_instance(user)
    return user

def signup_user(request, username, email, password):
    user = User.objects.create_user(username, email, password)
    check_cart_instance(user)
    login(request, user)
    return user
