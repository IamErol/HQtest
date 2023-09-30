from django.urls import path
from .views import StudentProduct, AllProducts
from rest_framework.routers import DefaultRouter

app_name = 'courses'
router = DefaultRouter()
router.register('product_access', StudentProduct, basename='product_access')
router.register('all_products', AllProducts, basename='all_products')
urlpatterns = router.urls