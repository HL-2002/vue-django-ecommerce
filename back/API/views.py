from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from API.serializers import *
from API.models import *
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DimensionsViewSet(viewsets.ModelViewSet):
    queryset = Dimensions.objects.all()
    serializer_class = DimensionsSerializer


class MetaViewSet(viewsets.ModelViewSet):
    queryset = Meta.objects.prefetch_related("qrCode").all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MetaReadSerializer
        return MetaSerializer


class QrCodeViewSet(viewsets.ModelViewSet):
    queryset = QrCode.objects.all()
    serializer_class = QrCodeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductReadSerializer
        return ProductSerializer
    parser_classes = (MultiPartParser, FormParser)
    def create(self, request, *args, **kwargs):
        
        files = []
        images_files = request.FILES.getlist("images")
        for value in images_files:
            files.append({"url": value})

        request_data = request.data.copy()
        request_data.pop("images", None)

        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(images=files)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
