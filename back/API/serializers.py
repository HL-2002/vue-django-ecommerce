from API.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class DimensionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimensions
        fields = "__all__"

class MetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meta
        fields = "__all__"

class QrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields = "__all__"

class QrCodeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields = ['url']

class MetaReadSerializer(serializers.ModelSerializer):
    qrCode = QrCodeReadSerializer()
    class Meta:
        model = Meta
        fields = "__all__"
    depth = 2


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    dimensions = DimensionsSerializer()
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("id",)
    
    def create(self, validated_data):
        dimensions_data = validated_data.pop('dimensions')
        dimensions = Dimensions.objects.create(**dimensions_data)
        product = Product.objects.create(dimensions=dimensions, **validated_data)
        return product


class ProductReadSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True, required=False)
    images = ImageSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Product
        fields = "__all__"

    depth = 2

