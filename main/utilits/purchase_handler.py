from ..models import Sales, Comissions, Product, Cart, CartItems
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ..forms import ComissionForm
class BuyManagement:
    def __init__(self, request):
        self.request = request
        self.is_superuser = self.request.user.is_superuser
        self.get_last_comission()
        self.calcular_faturamento()

    def objeto_faturamento(self):
        if self.is_superuser:
            self.sales = Sales.objects.all()
        else:
            self.sales = Sales.objects.filter(product__owner=self.request.user)

    def calcular_faturamento(self):
        if not hasattr(self, 'sales'):
            self.objeto_faturamento()
        self.faturamento_total = 0
        self.faturamento_empresa = 0
        self.faturamento_vendedor = 0
        for i in self.sales:
            self.faturamento_total += i.total_product_sale
            if self.is_superuser:
                self.faturamento_empresa += i.company_net_earning
            else:
                self.faturamento_vendedor += i.owner_net_earning

    def update_comissions(self):
        if self.request.method == "POST":
            form = ComissionForm(self.request.POST)
            if form.is_valid():
                form.save()
        else:
            form = ComissionForm()
        return True, form

    def get_last_comission(self):
        latest_comission = Comissions.objects.order_by('-id').first()
        if latest_comission is None:
            latest_comission = Comissions()
            latest_comission.save()
        self.latest_comission = latest_comission

    def handle_cart_sale(self, cart_items): #adicionar isatomic
        self.get_last_comission()
        for item in cart_items:
            sale = Sales(
                product=item.product,
                quantity=item.quantity,
                price_at_sale=item.product.product_price,
                comissions=self.latest_comission,
                owner_share_at_sale=self.latest_comission.owner_share,
                company_commission_at_sale=self.latest_comission.company_commission
            )
            sale.save()
        cart_items.delete()

    def handle_single_sale(self, product, quantity):
        self.get_last_comission()
        sale = Sales(
            product=product,
            quantity=quantity,
            price_at_sale=product.product_price,
            comissions=self.latest_comission,
            owner_share_at_sale=self.latest_comission.owner_share,
            company_commission_at_sale=self.latest_comission.company_commission
        )
        sale.save()
        
        


class CartManagement:
    def __init__(self, request):
        self.request = request

    @property
    def cartobj(self):
        return Cart.objects.get(cart_owner=self.request.user)
    
    @property
    def cart_items(self):
        return self.cartobj.items.filter(product__product_visibility = True)

    def add_product_to_cart(self, product, quantity):
        cart = self.cartobj
        obj, created = CartItems.objects.get_or_create(product=product, cart=cart, defaults={
            "quantity": quantity
        })
        
        if not created:
            obj.quantity = quantity
            obj.save()

    def buy_all(self):
        pass


class ProductDetails:
    def __init__(self, user_id=None):
        self.user_id = user_id
    
    def products(self):
        return Product.objects.filter(product_visibility=True)
    
    def product_by_owner(self):
        if self.user_id:
            owner = get_object_or_404(User, id=self.user_id)
            products = Product.objects.filter(owner=owner, product_visibility = True)
            return products
    
