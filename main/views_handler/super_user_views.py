

from django.shortcuts import render, redirect
from ..decorators import super_user_required
from ..form_handler.auth_form_handler import AuthHandler
from ..utilits.purchase_handler import BuyManagement

@super_user_required
def faturamento(request):
    faturamento = BuyManagement(request)
    faturamento.calcular_faturamento()
    
    return render(request, 'faturamento.html', context={'faturamento_total': faturamento.faturamento_total, 'faturamento_empresa': faturamento.faturamento_empresa})

@super_user_required
def create_staff_account(request):
    status, action = AuthHandler(request).signup_form_handler(True)
    if status:
        return redirect(action)
    return render(request, 'signup.html', context={"form": action})

@super_user_required
def comission_update(request):
    status, action = BuyManagement(request).update_comissions()
    return render(request, 'comission_update.html', {'form': action})
