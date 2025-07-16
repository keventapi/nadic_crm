from functools import wraps
from django.shortcuts import redirect
from .models import Comissions

def loged_out_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return function(request, *args, **kwargs)
    return wrapper

def super_user_required(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        return redirect('index')
    return wrapper
