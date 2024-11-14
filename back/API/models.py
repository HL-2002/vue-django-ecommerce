from django.db import models
from django.forms.models import model_to_dict
import simplejson as json


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_category_name")
        ]

    def __str__(self):
        return self.name


class Meta(models.Model):
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    barcode = models.CharField(max_length=100)

    def __str__(self):
        return json.dumps(
            {
                "createdAt": self.createdAt,
                "updatedAt": self.updatedAt,
                "barcode": self.barcode,
                "qrCode": self.qrCode,
            },
            indent=4,
            default=str,
        )


class QrCode(models.Model):
    meta = models.OneToOneField(Meta, related_name="qrCode", on_delete=models.CASCADE)
    url = models.ImageField(upload_to="qr/")


class Dimensions(models.Model):
    depth = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        return json.dumps(
            {
                "depth": self.depth,
                "width": self.width,
                "height": self.height,
            },
            indent=4,
        )


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_tag_name")]

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discountPercentage = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    stock = models.IntegerField()
    tags = models.ManyToManyField(Tag)
    brand = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    weight = models.FloatField()
    dimensions = models.OneToOneField(Dimensions, on_delete=models.CASCADE)
    warrantyInformation = models.TextField()
    shippingInformation = models.TextField()
    availabilityStatus = models.CharField(max_length=100)
    returnPolicy = models.TextField()
    minimumOrderQuantity = models.IntegerField()
    meta = models.OneToOneField(Meta, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to="images/")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title"], name="unique_title_name")
        ]

    def __str__(self):
        return json.dumps(
            {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "category": self.category.name,
                "price": self.price,
                "discountPercentage": self.discountPercentage,
                "rating": self.rating,
                "stock": self.stock,
                "brand": self.brand,
                "tags": self.tags.values_list("name", flat=True),
                "sku": self.sku,
                "weight": self.weight,
                "dimensions": model_to_dict(self.dimensions),
                "warrantyInformation": self.warrantyInformation,
                "shippingInformation": self.shippingInformation,
                "availabilityStatus": self.availabilityStatus,
                "returnPolicy": self.returnPolicy,
                "minimumOrderQuantity": self.minimumOrderQuantity,
                "thumbnail": self.thumbnail.url if self.thumbnail else None,
            },
            indent=4,
            default=str,
        )


class Review(models.Model):
    product = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    comment = models.TextField()
    date = models.DateTimeField(null=False)
    reviewerName = models.CharField(max_length=100)
    reviewerEmail = models.EmailField()

    def __str__(self):
        return json.dumps(
            {
                "productId": self.product.id,
                "rating": self.rating,
                "comment": self.comment,
                "date": self.date,
                "reviewerName": self.reviewerName,
                "reviewerEmail": self.reviewerEmail,
            },
            indent=4,
            default=str,
        )


class Image(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    url = models.ImageField(upload_to="images/")

    def __str__(self):
        return json.dumps(
            {
                "productId": self.product.id,
                "url": self.url.url if self.url else None,
            },
            indent=4,
        )
