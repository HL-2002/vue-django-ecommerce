from django.urls import include, path
from . import views
from rest_framework import routers

# URL conf
# REST framework registry
router = routers.DefaultRouter()
router.register(r'products', views.ProductsViewSet)
router.register(r'dimensions', views.DimensionsViewSet)


urlpatterns = [
    path('', include(router.urls)),
]