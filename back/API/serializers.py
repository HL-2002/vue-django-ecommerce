from API.models import *
from rest_framework import serializers
from rest_framework.fields import ImageField


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


class ReviewDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ["product"]


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.ImageField()
    class Meta:
        model = Image
        fields = ["url"]
        read_only_fields = ["product"]


class ImageDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["url"]


class ProductSerializer(serializers.ModelSerializer):
    dimensions = DimensionsSerializer()
    meta = MetaSerializer()
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    images = ImageSerializer(many=True, required=False)
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("id",)

    def create(self, validated_data):
        dimensions_data = validated_data.pop("dimensions")
        meta_data = validated_data.pop("meta")
        tags_data = validated_data.pop("tags")
        images_data = validated_data.pop("images",[])
        
        # Create the nested dimensions object first
        dimensions = Dimensions.objects.create(**dimensions_data)

        # # Create the nested meta object and initialize the createAt and updatedAt fields
        meta = Meta.objects.create(**meta_data)
        # create product
        product = Product.objects.create(dimensions=dimensions,meta=meta, **validated_data)
        product.tags.set(tags_data)
       
        for image_data in images_data:
            Image.objects.create(product=product, **image_data)     
        return product
    def update(self, instance, validated_data):
        dimensions_data = validated_data.pop("dimensions")
        meta_data = validated_data.pop("meta")
        tags_data = validated_data.pop("tags")
        images_data = validated_data.pop("images", [])

        # Update the nested dimensions object
        for attr, value in dimensions_data.items():
            setattr(instance.dimensions, attr, value)
        instance.dimensions.save()

        # Update the nested meta object
        for attr, value in meta_data.items():
            setattr(instance.meta, attr, value)
        instance.meta.save()

        # Update the product instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update tags
        instance.tags.set(tags_data)

        # Update images
        instance.images.all().delete()
        for image_data in images_data:
            Image.objects.create(product=instance, **image_data)
        return instance



class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    meta = MetaReadSerializer()
    dimensions = DimensionsSerializer()
    tags = TagSerializer(many=True, read_only=True)
    reviews = ReviewDisplaySerializer(many=True, read_only=True, required=False)
    images = ImageDisplaySerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Product
        fields = "__all__"

    depth = 2
