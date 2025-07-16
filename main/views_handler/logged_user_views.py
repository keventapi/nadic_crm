from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from ..models import Product, CartItems
from ..utilits.purchase_handler import BuyManagement, CartManagement, ProductDetails
from ..forms import ProductForm
from ..form_handler.product_form_handler import ProductFormHandler
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
#adicionar um decorador pra url de ações para evitar repetir o codigo tipo exec_action dps exec_redirect

class Index(LoginRequiredMixin, ListView):
    model = Product
    template_name = "index.html"
    context_object_name = "products"
    paginate_by = 10
    
    def get_queryset(self):
        search = self.request.GET.get('search')
        products = ProductDetails().products()
        print(search)
        if search:
            products = products.filter(product_name__icontains=search)
        return products



class Profile(LoginRequiredMixin, ListView):
    model = Product
    template_name = "profile.html"
    context_object_name = "product"
    paginate_by = 10
    
    def get_queryset(self):
        return ProductDetails(self.kwargs['user_id']).product_by_owner()



class ViewCart(LoginRequiredMixin, ListView):
    model = CartItems
    template_name = "cart.html"
    context_object_name = "cart_itens"
    paginate_by = 10
    
    def get_queryset(self):
        return CartManagement(self.request).cart_items

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == "comprar tudo":
            cart_object = CartManagement(request)
            cart_items = cart_object.cart_items
            BuyManagement(request).handle_cart_sale(cart_items)
            messages.success(request, 'compras realizadas com sucesso')
        return redirect('cart')
        
class SellerDashboard(LoginRequiredMixin, ListView):
    model = Product
    template_name = "seller_dashboard.html"
    context_object_name = "products"
    paginate_by = 10
    
    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faturamentoobj = BuyManagement(self.request)
        faturamentoobj.calcular_faturamento()
        if self.request.user.is_superuser:
            faturamento = faturamentoobj.faturamento_empresa
        else:
            faturamento = faturamentoobj.faturamento_vendedor
        context['faturamento'] =  faturamento
        return context

@login_required
def add_product(request):
    status, action = ProductFormHandler(request).add_product_handler()
    if status:
        return redirect(action)
    return render(request, 'user_product_manager.html', {'form': action})


@login_required
def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    status, action = ProductFormHandler(request).view_product_handler(product)
    if status:
        return redirect(action)
    product_owner_status =  product.owner == request.user    
    return render(request, 'product_view.html', {'product': product, 'form': action, 'owner': product_owner_status})

@login_required
def edit_product(request, product_id):
    product_info = get_object_or_404(Product, id=product_id)
    status, action = ProductFormHandler(request).edit_product_handler(product_info)
    print(status, action)
    if status:
        return redirect(action)
    return render(request, 'product_edit.html', {'form': action})

@login_required
def add_to_cart(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)
    product_quantity = int(quantity)
    ProductFormHandler(request).add_cart(product, product_quantity)
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('index')

@login_required
def buy_item(request, product_id, quantity):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(quantity)
    ProductFormHandler(request).buy_item(product, quantity)
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('index')

@login_required
def remove_from_cart(request, product_id):
    cartobj = CartManagement(request).cartobj
    cartitem = cartobj.items.filter(product__id=product_id).first()
    if cartitem:
        cartitem.delete()
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('index')

@login_required
def handle_logout(request):
    logout(request)
    return redirect('index')