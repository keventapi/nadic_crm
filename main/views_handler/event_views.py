from django.http import JsonResponse
from ..models import Product
import json

def auto_complete(response):
    print('autocomplete')
    if response.method == "POST":
        data = json.loads(response.body.decode('utf-8'))
        product_name = data.get("value")
        if product_name is not None:
            products = Product.objects.filter(product_name__icontains=product_name.lower(), product_visibility=True)
            product_list = [{'name': p.product_name, 'id': p.id} for p in products]
            return JsonResponse({'query': product_list})
        return