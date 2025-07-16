from rest_framework import viewsets, permissions
from ..models import Comissions
from ..serializers import ComissionSerializer
from ..utilits.purchase_handler import ProductDetails, CartManagement
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from ..utilits.purchase_handler import BuyManagement
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser

class ComissionViewSet(viewsets.ModelViewSet):
    queryset = Comissions.objects.all()
    serializer_class = ComissionSerializer
    permission_classes = [IsSuperUser]
    http_method_names = ['get', 'post']
    
    def list(self, request, *args, **kwargs):
        latest = Comissions.objects.order_by('-id').first()
        if latest is None:
            return Response({"detail": "Nenhuma comissão registrada"}, status=404)
        serializer = self.get_serializer(latest)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        raise PermissionDenied({'detail': 'comissões não podem ser destruidas, pois afeta o historico, tente utilizar create'}, 403)

    def perform_create(self, serializer):
        try:
            owner = str(self.request.data.get('owner_share'))
            company = str(self.request.data.get('company_comission'))
        
            serializer.save(owner_share=owner, company_commission=company)
        except:
            return Response({'error':' defina o owner_share e o company_comission'}, 400)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def faturamento(request):
    data = BuyManagement(request)
    data.calcular_faturamento()
    if request.user.is_superuser:
        faturamento_total = data.faturamento_total
        company_faturamento = data.faturamento_empresa
        return Response({'faturamento total': faturamento_total, 'faturamento empresa': company_faturamento}, 200)
    vendedor_faturamento = data.faturamento_vendedor
    return Response({'seu faturamento': vendedor_faturamento}, 200)

        
