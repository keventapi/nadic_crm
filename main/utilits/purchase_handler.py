from ..utilits import BuyManagement
from ..models import Cart

class Cart(BuyManagement):
    def __init__(self, response):
        super().__init__(response=response)
        self.response = response

    @property
    def cart(self):
        return Cart.objects.get(cart_owner=self.response.user)
    
    @property
    def cart_items(self):
        return self.cart.items.filter(product__product_visibility = True)
    