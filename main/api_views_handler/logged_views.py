from rest_framework import viewsets, permissions
from ..models import Product, ProductType, Cart, CartItems
from ..serializers import ProductSerializer, ProductTypeSerializer, CartSerializer
from ..utilits.purchase_handler import ProductDetails, CartManagement
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from ..utilits.purchase_handler import BuyManagement
from rest_framework.response import Response

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']
    
    def get_queryset(self):
        queryset = Cart.objects.filter(cart_owner=self.request.user)
        return queryset
    
    def get_object(self):
        obj = super().get_object()
        if obj.cart_owner != self.request.user:
            raise PermissionDenied({'error': "Você não tem permissão para acessar este carrinho."}, 400)
        return obj
    
class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(product_visibility=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_name', 'product_type__id']
    

class ProductManipulationSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(product_visibility=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post', 'put', 'patch', 'delete']
    
    def get_queryset(self):
        return ProductDetails(self.request.user.id).product_by_owner()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied({'error': "voce não pode editar produtos que não são seus"}, 400)
        serializer.save()
        
    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied({'error': "voce não pode deletar produtos que não são seus"}, 400)
        instance.product_visibility = False
        instance.save()
    
class BuyItem(APIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']
    
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        if product_id is None or quantity is None:
            return Response({'response': 'dados invalidos'}, 400)

        if product_id and quantity:
            cleaned_product_id = int(product_id)
            cleaned_quantity = int(quantity)
            if cleaned_quantity > 0:
                product = Product.objects.get(id=cleaned_product_id, product_visibility = True)
                if product:
                    BuyManagement(request).handle_single_sale(product=product, quantity=cleaned_quantity)

                return Response({'response': 'compra realizada com sucesso'}, 200)
            return Response({'response':'erro a efetuar a compra, produto nao existe'}, 400)
        
class BuyAllFromCart(APIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']
    
    def get(self, request):
        cart_items = CartManagement(request).cart_items
        if not cart_items:
            return Response({'response': 'carrinho vazio'})
        BuyManagement(request).handle_cart_sale(cart_items)
        return Response({'response': 'compra do carrinho feita com sucesso'}, 200)
    
class AddToCart(APIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']
    
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        
        if product_id is None or quantity is None:
            return Response({'response': 'dados invalidos, preencha product_id e quantity com valores validos'}, 400)
        
        try:
            cleaned_product_id = int(product_id)
            cleaned_quantity = int(quantity)
        except:
            return Response({'error': 'product_id ou quantity estão invalidos'})
        product = Product.objects.get(id=cleaned_product_id, product_visibility = True)
        CartManagement(request).add_product_to_cart(product, cleaned_quantity)
        return Response({'response': 'produto adicionado ao carrinho'})

class RemoveCartItem(APIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']
    
    def post(self, request):
        product_id = request.data.get('product_id')
        if product_id is None:
            return Response({'response': 'product_id é um campo obrigatorio'}, 400)
        
        try:
            product_id = int(product_id)
        except:
            return Response({'error': "product_id é um inteiro"})
        
        cart = Cart.objects.get(cart_owner = request.user)
        product = Product.objects.filter(id=product_id).first()
        if product:
            cart_item = cart.items.filter(product=product).first()
            if not cart_item:
                return Response({'response': 'voce nao tem esse produto no carrinho'}, 400)
            cart_item.delete()
            return Response({'response': 'item removido do carrinho'}, 200)
        return Response({'error': 'produto não achado'}, 404)
        