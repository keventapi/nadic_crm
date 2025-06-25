from django import forms 
from .models import Product

class AuthForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
    
class SignupForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'product_name': 'product name',
            'product_image': 'product image',
            'product_price': 'product price R$',
            'product_description': 'product description',
            'product_type': 'product type',
        }
        widgets = {
            'product_name': forms.TextInput(),
            'product_image': forms.ClearableFileInput(),
            'product_price': forms.NumberInput(),
            'product_description': forms.Textarea(),
            'product_type': forms.CheckboxSelectMultiple(),
        }