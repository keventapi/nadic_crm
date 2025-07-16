
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from ..form_handler.auth_form_handler import AuthHandler

@api_view(["POST"])
def signup_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    if username and email and password:
        user = User.objects.create_user(username, email, password)
        AuthHandler(request).check_cart_instance(user)
        return Response({'response': "usuario criado com sucesso"}, 200)
    return Response({'error': 'erro ao criar o usuario'}, 400)
