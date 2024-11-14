from API.models import *
from rest_framework import serializers


"""
Each model has its own serializer, which is used to convert the model to JSON and vice versa.

However, some models have a different serializer for reading and writing, as the data is structured differently.
For writing, the usual serializer is used, as it doesn't include the nested data.
For reading, a different serializer is used, as it includes the nested data.
For displaying FKs, another serializer is used, as it includes only a distilled version of the object.

"""


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class DimensionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimensions
        fields = "__all__"


class DimensionDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimensions
        exclude = ["id"]


class QrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields = "__all__"


class QrCodeDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields = ["url"]


class MetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meta
        fields = "__all__"


class MetaReadSerializer(serializers.ModelSerializer):
    qrCode = QrCodeDisplaySerializer()

    class Meta:
        model = Meta
        fields = "__all__"

    depth = 2


class MetaDisplaySerializer(serializers.ModelSerializer):
    qrCode = QrCodeDisplaySerializer()

    class Meta:
        model = Meta
        exclude = ["id"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TagDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ["id"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ReviewDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ["product", "id"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ImageDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["url"]


class ProductSerializer(serializers.ModelSerializer):
    dimensions = DimensionsSerializer()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("id",)

    def create(self, validated_data):
        dimensions_data = validated_data.pop("dimensions")
        dimensions = Dimensions.objects.create(**dimensions_data)
        product = Product.objects.create(dimensions=dimensions, **validated_data)
        return product


class ProductReadSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    meta = MetaDisplaySerializer()
    dimensions = DimensionDisplaySerializer()
    tags = serializers.StringRelatedField(many=True)
    reviews = ReviewDisplaySerializer(many=True, read_only=True, required=False)
    images = ImageDisplaySerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Product
        fields = "__all__"

    depth = 2
