from django.urls import include, path
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
