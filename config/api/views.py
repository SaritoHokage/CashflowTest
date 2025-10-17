from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from core.models import Status, TxType, Category, SubCategory
from cashflow.models import CashFlowEntry
from .serializers import (
    StatusSerializer, TxTypeSerializer, CategorySerializer, SubCategorySerializer,
    CashFlowEntrySerializer
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def ping(request):
    return Response({'status': 'ok'})

class BaseReadOnlySet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['id']
    ordering = ['-id']

class StatusViewSet(BaseReadOnlySet):
    queryset = Status.objects.all().order_by('id')
    serializer_class = StatusSerializer

class TxTypeViewSet(BaseReadOnlySet):
    queryset = TxType.objects.all().order_by('id')
    serializer_class = TxTypeSerializer

class CategoryViewSet(BaseReadOnlySet):
    queryset = Category.objects.select_related('type').all()
    serializer_class = CategorySerializer
    filterset_fields = ['type']

class SubCategoryViewSet(BaseReadOnlySet):
    queryset = SubCategory.objects.select_related('category').all()
    serializer_class = SubCategorySerializer
    filterset_fields = ['category']

class CashFlowEntryViewSet(BaseReadOnlySet):
    queryset = CashFlowEntry.objects.select_related(
        'status','type','category','subcategory'
    ).all()
    serializer_class = CashFlowEntrySerializer
    filterset_fields = ['status', 'type', 'category', 'subcategory']
    ordering_fields = ['id', 'created_at', 'amount']
    ordering = ['-created_at', '-id']


    def get_queryset(self):
        qs = super().get_queryset()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            d = parse_date(date_from)
            if d:
                qs = qs.filter(created_at__gte=d)
        if date_to:
            d = parse_date(date_to)
            if d:
                qs = qs.filter(created_at__lte=d)
        return qs

@api_view(['GET'])
@permission_classes([AllowAny])
def ping(request):
    return Response({'status': 'ok'})