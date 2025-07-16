from ..forms import ProductForm, ProductSale
from django.shortcuts import redirect
from ..utilits.purchase_handler import BuyManagement, CartManagement
from ..models import Product
from django.urls import reverse
# fazer metodo para retornar o productform com ou sem instance de maneira limpa e sem me repetir

class ProductFormHandler:
    def __init__(self, request):
        self.request = request
        self.buy_management = BuyManagement(request)
        self.cart_management = CartManagement(request)
    
    def add_product_handler(self, product=None):
        if self.request.method == "POST":
            
            if not product:
                form = ProductForm(self.request.POST, self.request.FILES)
            else:
                form = ProductForm(self.request.POST, self.request.FILES, instance=product)
                
            if form.is_valid():
                product = form.save(commit=False)
                product.owner = self.request.user
                product.save()
                
                return True, 'seller_dashboard'
            else:
                return False, form
            
        else:
            if not product:
                form = ProductForm()
            else:
                form = ProductForm(instance=product)
                
            return False, form
        
    def edit_product_handler(self, product):
        if product.owner != self.request.user:
            return redirect('index')
        if self.request.method == "POST":
            action = self.request.POST.get('action')
            if action == "submit":
                status, action = self.add_product_handler(product)
                return status, action
            elif action == "delete":
                self.delete_product(product)
                return True, "seller_dashboard"
            elif action == "cancel":
                return True, "seller_dashboard"
        else:
            form = ProductForm(instance=product)
            return False, form
        
    def delete_product(self, product):
        Product.objects.filter(pk=product.pk).update(product_visibility=False)

        
    def get_product_quantity(self, form):
        if form.is_valid():
            return form.cleaned_data['quantity']
        else:
            return None
        
    def buy_item(self, product, quantity):
        if quantity is not None:
            self.buy_management.handle_single_sale(product, quantity)
                
    def add_cart(self, product, quantity):
        if quantity is not None and isinstance(quantity, int):
            self.cart_management.add_product_to_cart(product, quantity)
    
    def view_product_handler(self, product):
        if self.request.method == "POST":
            form = ProductSale(self.request.POST, product=product)
            action = self.request.POST.get('action')
            if form.is_valid():
                quantity = form.cleaned_data['quantity']
                if quantity > 0:
                    if action == "comprar":
                        return True, reverse('buy_item', args=[product.id, quantity])
                    
                    elif action == "carrinho":
                        return True, reverse('add_to_cart', args=[product.id, quantity])
        else:
            form = ProductSale()

        return False, form


