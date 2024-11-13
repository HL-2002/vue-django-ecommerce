from django.urls import include, path
from . import views
from rest_framework import routers

# URL conf
# REST framework registry
router = routers.DefaultRouter()
router.register(r"product", views.ProductViewSet)
router.register(r"dimensions", views.DimensionsViewSet)
router.register(r"meta", views.MetaViewSet)
router.register(r"category", views.CategoryViewSet)
router.register(r"tag", views.TagViewSet)
router.register(r"review", views.ReviewViewSet)
router.register(r"image", views.ImageViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
