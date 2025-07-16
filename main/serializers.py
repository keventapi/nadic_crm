from rest_framework import serializers
from .models import Product, ProductType, Cart, CartItems, Comissions

class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ["id", "cart_owner", "items"]

    def get_items(self, obj):
        visible_items = obj.items.filter(product__product_visibility = True)
        return CartItemsSerializer(visible_items, many=True).data

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ["id", "type_name"]
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["owner", "product_visibility"]
        
class ComissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comissions 
        fields = "__all__"