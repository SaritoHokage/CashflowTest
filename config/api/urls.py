from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StatusViewSet, TxTypeViewSet, CategoryViewSet, SubCategoryViewSet,
    CashFlowEntryViewSet, ping
)

router = DefaultRouter()
router.register(r'statuses', StatusViewSet)
router.register(r'types', TxTypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'entries', CashFlowEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ping/', ping, name='api_ping'),
]
