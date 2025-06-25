from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def login_user(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        print('logado')
        return True
    else:
        return False
    
def signup_user(request, username, email, password):
    user = User.objects.create_user(username, email, password)
    login(request, user)
    if authenticate(request, username=username, password=password) is not None:
        print('registrado e logado com sucesso')
        return True
    return False