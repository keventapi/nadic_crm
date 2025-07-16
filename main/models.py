from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal, ROUND_DOWN



class ProductType(models.Model):
    type_name = models.CharField(max_length=60)
    type_category = models.TextField()
    
    def save(self, *args, **kwargs):
        self.type_name = self.type_name.lower()
        self.type_category = self.type_category.lower()
        
        super().save(*args, **kwargs)
    def __str__(self):
        return self.type_name

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to='imgs/')
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_stock = models.PositiveIntegerField()
    product_description = models.TextField()
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    product_visibility = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        if self.product_stock == 0:
            self.product_visibility = False
        else:
            self.product_visibility = True
        self.product_name = self.product_name.lower()
        self.product_description = self.product_description.lower()
        
        super().save(*args, **kwargs) 
           
    def update_data(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.full_clean()
        self.save()
    
    def __str__(self):
        return f"product name:{self.product_name} product price:{self.product_price} product description:{self.product_description} product type:{self.product_type}"

class Cart(models.Model):
    cart_owner = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.cart_owner.username

class CartItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    
    def save(self, *args, **kwargs):
        if self.quantity > self.product.product_stock:
            raise ValidationError('quantidade maior que o esperado')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product.product_name}: {self.quantity}"

class Comissions(models.Model):
    owner_share = models.DecimalField(max_digits=4, decimal_places=2, default=0.9)
    company_commission = models.DecimalField(max_digits=4, decimal_places=2, default=0.1)
    def clean(self):
        total = self.owner_share + self.company_commission
        if abs(total - Decimal('1.00')) > Decimal('0.001'):
            raise ValidationError("Comissão + parte do dono deve ser igual a 100% (1.00)")

    def __str__(self):
        return f"Owner: {self.owner_share}, company: {self.company_commission}"


class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    comissions = models.ForeignKey(Comissions, on_delete=models.PROTECT)
    owner_share_at_sale = models.DecimalField(max_digits=4, decimal_places=2)
    company_commission_at_sale = models.DecimalField(max_digits=4, decimal_places=2)

    @property
    def total_product_sale(self):
        return self.quantity * self.price_at_sale

    @property
    def owner_net_earning(self):
        return self.total_product_sale * self.owner_share_at_sale

    @property
    def company_net_earning(self):
        return self.total_product_sale * self.company_commission_at_sale
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.owner_share_at_sale = self.comissions.owner_share
            self.company_commission_at_sale = self.comissions.company_commission
        self.full_clean()
        with transaction.atomic():
            product_stock = self.product.product_stock
            if (product_stock - self.quantity) < 0:
                raise ValueError('houve a tentativa de comprar mais itens que o disponivel em estoque')
            self.product.product_stock -= self.quantity
            self.product.save()
            super().save(*args, **kwargs)

    def clean(self):
        total = self.owner_share_at_sale + self.company_commission_at_sale
        
        if total != Decimal('1.00'):
            raise ValidationError("Comissão + parte do dono deve ser igual a 100% (1.00)")

    def __str__(self):
        return f"{self.quantity} × {self.price_at_sale} = {self.total_product_sale}"
