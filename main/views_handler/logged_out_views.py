from ..form_handler.auth_form_handler import AuthHandler
from ..decorators import loged_out_required
from django.shortcuts import render, redirect

@loged_out_required
def login_page(request):
    status, action = AuthHandler(request).auth_form_handler()
    if status:
        return redirect(action)

    return render(request, "login.html", {"form": action})

@loged_out_required
def signup_page(request):
    status, action = AuthHandler(request).signup_form_handler(False)
    if status:
        return redirect(action)
    
    return render(request, 'signup.html', {'form': action})