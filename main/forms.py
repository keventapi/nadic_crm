from django import forms 
from .models import Product, Sales, Comissions
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
        exclude = ['owner', 'product_visibility']
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
        self.fields['product_stock'].widget.attrs.update({'min': 0})

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['owner', 'product_visibility']
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
        self.fields['product_stock'].widget.attrs.update({'min': 0})
       
class ProductSale(forms.Form):
    quantity = forms.IntegerField()
    
    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product
        if self.product:
            self.fields['quantity'].max_value = self.product.product_stock
            self.fields['quantity'].widget.attrs.update({
                'max': self.product.product_stock,
                'min': 1
            })
    
    def clean(self):
        cleaned_data = super().clean()
        if self.product and cleaned_data:
            if self.product.product_stock < cleaned_data.get('quantity') and cleaned_data.get('quantity') > 0:
                raise forms.ValidationError('tentativa de comprar algo acima do estoque')
        return cleaned_data

class ComissionForm(forms.ModelForm):
    class Meta:
        model = Comissions
        fields = '__all__'
        labels = {
            'owner_share': 'the seleer part from 0.01 to 1',
            'company_commission': 'the company commision it must result to 1',
        }
        widgets = {
            'owner_share': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '1'}),
            'company_commission': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '1'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner_share'].widget.attrs.update({'min': 0, 'max': 1})
        self.fields['company_commission'].widget.attrs.update({'min': 0, 'max': 1})