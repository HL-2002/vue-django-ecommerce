from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from API.serializers import *
from API.models import *
from rest_framework import viewsets


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DimensionsViewSet(viewsets.ModelViewSet):
    queryset = Dimensions.objects.all()
    serializer_class = DimensionsSerializer


class MetaViewSet(viewsets.ModelViewSet):
    queryset = Meta.objects.all()
    serializer_class = MetaSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("reviews", "images").all()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductReadSerializer
        return ProductSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


def get_product_by_id(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello Django!")


def post_product(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello Django!")
