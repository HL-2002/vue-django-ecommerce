from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from API.serializers import *
from API.models import *
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
import os

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
    def update(self, request, *args, **kwargs):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            files = []
            images_files = request.FILES.getlist("images")
            for value in images_files:
                files.append({"url": value})

            request_data = request.data.copy()
            request_data.pop("images", None)
            serializer = self.get_serializer(instance, data=request_data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save(images=files)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Get the product id from the instance
        product = Product.objects.get(id=instance.product.id)
        instance.delete()

        # Get all reviews related to the product, average the ratings then save the product
        reviews = Review.objects.filter(product=product)
        product.rating = sum([review.rating for review in reviews]) / len(reviews)
        product.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
