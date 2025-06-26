from django.db import models

# Create your models here.
class ProductType(models.Model):
    type_Name = models.CharField(max_length=60)
    type_category = models.TextField()
    
    def __str__(self):
        return self.type_Name

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to='imgs/')
    product_price = models.IntegerField()
    product_stock = models.IntegerField()
    product_description = models.TextField()
    product_type = models.ManyToManyField(ProductType)    
    def __str__(self):
        return f"product name:{self.product_name} product price:{self.product_price} product description:{self.product_description} product type:{self.product_type}"