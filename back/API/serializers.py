from API.models import *
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class DimensionsSerializer(serializers.HyperlinkedModelSerializer):
    lookup_field = "id"

    class Meta:
        model = Dimensions
        fields = ["width", "height", "depth"]


class MetaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Meta
        fields = ["createdAt", "updatedAt", "barcode", "qrCode"]


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = ["rating", "comment", "date", "reviewerName", "reviewerEmail"]


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ["url"]


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        depth = 2
