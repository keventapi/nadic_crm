
from ..forms import SignupForm, ComissionForm
from ..models import Sales
from .. import auth, utilits
from django.shortcuts import render
from ..decorators import super_user_required
from django.contrib import messages

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
