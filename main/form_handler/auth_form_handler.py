from ..forms import AuthForm, SignupForm
from ..models import Cart
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class AuthHandler:
    def __init__(self, request):
        self.request = request

    def get_login_credentials(self):
        if self.form.is_valid():
            return self.form.cleaned_data['username'], self.form.cleaned_data['password']
        return None, None

    def get_signup_credentials(self):
        if self.form.is_valid():
            return (
                self.form.cleaned_data['username'],
                self.form.cleaned_data['email'],
                self.form.cleaned_data['password'],
            )
        return None, None, None

    def check_cart_instance(self, user):
        Cart.objects.get_or_create(cart_owner=user)

    def login_user(self):
        username, password = self.get_login_credentials()
        if username and password:
            user = authenticate(self.request, username=username, password=password)
            if user:
                login(self.request, user)
                self.check_cart_instance(user)
                return user
        return None

    def signup_user(self, is_superuser=False):
        username, email, password = self.get_signup_credentials()
        if username and email and password:
            if is_superuser and self.request.user.is_superuser:
                user = User.objects.create_superuser(username, email, password)
            else:
                user = User.objects.create_user(username, email, password)
                self.check_cart_instance(user)
                login(self.request, user)
            return user
        return None
    
    def auth_form_handler(self):
        if self.request.method == "POST":
            self.form = AuthForm(self.request.POST)
            if self.form.is_valid():
                self.login_user()
                return True, "index"
            return False, self.form
        else:
            return False, AuthForm()

    def signup_form_handler(self, is_superuser=False):
        if self.request.method == "POST":
            self.form = SignupForm(self.request.POST)
            if self.form.is_valid():
                self.signup_user(is_superuser)
                
                if not is_superuser:
                    return True, "index"
                return True, "staff_account"
            return False, self.form
        else:
            return False, SignupForm()
        
    
    def logout_handler(self):
        logout(self.request)
        