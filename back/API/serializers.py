from API.models import *
from rest_framework import serializers


"""
Each model has its own serializer, which is used to convert the model to JSON and vice versa.

However, some models have a different serializer for reading and writing, as the data is structured differently.
For writing, the usual serializer is used, as it doesn't include the nested data.
For reading, a different serializer is used, as it includes the nested data.
For displaying FKs, another serializer is used, as it includes only a distilled version of the object without fk.

"""


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class DimensionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimensions
        fields = "__all__"


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
        fields = '__all__'

class MetaReadSerializer(serializers.ModelSerializer):
    qrCode = QrCodeDisplaySerializer()

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

    def create(self, validated_data):
        # Create and save review object
        review = Review(**validated_data)
        review.save()

        # Get the product id from the validated data
        product = Product.objects.get(id=validated_data["product"].id)

        # Get all reviews related to the product
        reviews = Review.objects.filter(product=product)

        # Average the reviews' ratings and save them in the product
        product.rating = sum([review.rating for review in reviews]) / len(reviews)
        product.save()

        return review


class ReviewDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ["product"]


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
    meta = MetaSerializer()
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("id",)

    def create(self, validated_data):
        dimensions_data = validated_data.pop("dimensions")
        meta_data = validated_data.pop("meta")
        tags_data = validated_data.pop("tags")
        
        
        # Create the nested dimensions object first
        dimensions = Dimensions.objects.create(**dimensions_data)

        # # Create the nested meta object and initialize the createAt and updatedAt fields
        meta = Meta.objects.create(**meta_data)



        product = Product.objects.create(dimensions=dimensions,meta=meta, **validated_data)
        product.tags.set(tags_data)
        return product
    def update(self,instance,validated_data):
        meta_data = validated_data.pop("meta",None)
        if meta_data:
            meta_serializer = self.fields['meta']
            meta_instance = instance.meta
            meta_serializer.update(meta_instance,meta_data)


class ProductReadSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    meta = MetaReadSerializer()
    dimensions = DimensionsSerializer()
    tags = serializers.StringRelatedField(many=True)
    reviews = ReviewDisplaySerializer(many=True, read_only=True, required=False)
    images = ImageDisplaySerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Product
        fields = "__all__"

    depth = 2
