from django.db import models
from django.contrib.auth.models import User



class ProductType(models.Model):
    type_Name = models.CharField(max_length=60)
    type_category = models.TextField()
    
    def __str__(self):
        return self.type_Name

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to='imgs/')
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_stock = models.PositiveIntegerField()
    product_description = models.TextField()
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    
    def update_data(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.full_clean()
        self.save()
    
    def __str__(self):
        return f"product name:{self.product_name} product price:{self.product_price} product description:{self.product_description} product type:{self.product_type}"


class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_product_sale(self):
        return self.quantity * self.price_at_sale

    def __str__(self):
        return f"{self.quantity} X {self.price_at_sale} = {self.total_product_sale}"
    
    