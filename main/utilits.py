from .models import Sales, Comissions, Product
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class BuyManagement:
    def __init__(self, response):
        self.response = response
        self.is_superuser = self.response.is_superuser

    def objeto_faturamento(self):
        if self.is_superuser:
            self.sales = Sales.objects.all()
        else:
            self.sales = Sales.objects.filter(product__in=Product.objects.filter(owner=self.response.user))

    def calcular_faturamento(self):
        self.faturamento_total = 0
        self.faturamento_empresa = 0
        self.faturamento_vendedor = 0

        if hasattr(self, 'sales') and self.sales is not None:
            for i in self.sales:
                self.faturamento_total += i.total_product_sale
                if self.is_superuser:
                    self.faturamento_empresa += i.company_net_earning
                else:
                    self.faturamento_vendedor += i.owner_net_earning

    def get_last_comission(self):
        latest_comission = Comissions.objects.order_by('-id').first()
        if latest_comission is None:
            latest_comission = Comissions()
            latest_comission.save()
        self.latest_comission = latest_comission

    def handle_cart_sale(self, cart_items):
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

class ProductDetails:
    @property
    def get_products(self):
        return Product.objects.filter(product_visibility=True)
    
    @property
    def get_product_by_owner(self, user_id):
        owner = get_object_or_404(User, id=user_id)
        products = Product.objects.filter(owner=owner, product_visibility = True)
        return products
    
def get_products():
    return Product.objects.filter(product_visibility = True)