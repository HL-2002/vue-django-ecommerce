from django.db import models
from django.forms.models import model_to_dict
import simplejson as json

# Create your models here.
class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name')
        ]

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'name': self.name
        }, indent=4)
    

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discountPercentage = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    stock = models.IntegerField()
    brand = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    weight = models.FloatField()
    warrantyInformation = models.TextField()
    shippingInformation = models.TextField()
    availabilityStatus = models.CharField(max_length=100)
    returnPolicy = models.TextField()
    minimumOrderQuantity = models.IntegerField()
    thumbnail = models.ImageField(upload_to='images/')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_title_name')
        ]

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'categoryId': self.category.id,
            'price': self.price,
            'discountPercentage': self.discountPercentage,
            'rating': self.rating,
            'stock': self.stock,
            'brand': self.brand,
            'sku': self.sku,
            'weight': self.weight,
            'warrantyInformation': self.warrantyInformation,
            'shippingInformation': self.shippingInformation,
            'availabilityStatus': self.availabilityStatus,
            'returnPolicy': self.returnPolicy,
            'minimumOrderQuantity': self.minimumOrderQuantity,
            'thumbnail': self.thumbnail.url if self.thumbnail else None
        }, indent=4)


class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    comment = models.TextField()
    date = models.DateTimeField(null=False)
    reviewerName = models.CharField(max_length=100)
    reviewerEmail = models.EmailField()

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'productId': self.product.id,
            'rating': self.rating,
            'comment': self.comment,
            'date': self.date,
            'reviewerName': self.reviewerName,
            'reviewerEmail': self.reviewerEmail
        }, indent=4, default=str)

class Meta(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    barcode = models.CharField(max_length=100)
    qrCode = models.CharField(max_length=100)

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'productId': self.product.id,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt,
            'barcode': self.barcode,
            'qrCode': self.qrCode
        }, indent=4, default=str)

class Image(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return json.dumps({
            'id': self.id,
            'productId': self.product.id,
            'url': self.url.url if self.url else None
        }, indent=4)
    

class Dimensions(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    depth = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'productId': self.product.id,
            'depth': self.depth,
            'width': self.width,
            'height': self.height
        }, indent=4)
    

class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_tag_name')
        ]
    
    def __str__(self):
        return json.dumps({
            'id': self.id,
            'name': self.name
        }, indent=4)
    
class ProductTag(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'productId': self.product.id,
            'tagId': self.tag.id
        }, indent=4)