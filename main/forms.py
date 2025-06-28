from django import forms 
from .models import Product, Sales
#criar validação extra para evitar uma quantidade de compras > stock



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
        exclude = ['owner']
        labels = {
            'product_name': 'product name',
            'product_image': 'product image',
            'product_price': 'product price R$',
            'product_stock': "stock do produto",
            'product_description': 'product description',
            'product_type': 'product type',
        }
        widgets = {
            'product_name': forms.TextInput(),
            'product_image': forms.ClearableFileInput(),
            'product_price': forms.NumberInput(),
            'product_stock': forms.NumberInput(),
            'product_description': forms.Textarea(),
            'product_type': forms.Select(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_stock'].widget.attrs.update({'min': 1})

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['owner']
        labels = {
            'product_name': 'product name',
            'product_image': 'product image',
            'product_price': 'product price R$',
            'product_stock': "stock do produto",
            'product_description': 'product description',
            'product_type': 'product type',
        }
        widgets = {
            'product_name': forms.TextInput(),
            'product_image': forms.ClearableFileInput(),
            'product_price': forms.NumberInput(),
            'product_stock': forms.NumberInput(),
            'product_description': forms.Textarea(),
            'product_type': forms.Select(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_stock'].widget.attrs.update({'min': 1})
       
class ProductSale(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['quantity']
        labels = {
            'quantity': "quantidade desejada:"
        }
        widgets = {
            "quantity": forms.NumberInput()
        }
    def __init__(self, *args, product, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].initial = 1
        self.fields['quantity'].max_value = product.product_stock
        self.fields['quantity'].widget.attrs.update({'max': product.product_stock, 'min': 1})