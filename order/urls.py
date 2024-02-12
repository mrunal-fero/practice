from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, BulkCreateViewSet
from django.urls import path
router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'order', BulkCreateViewSet, basename='bulk-upload')
urlpatterns = router.urls