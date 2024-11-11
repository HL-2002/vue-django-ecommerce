from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    stock = models.IntegerField()
    brand = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    weight = models.FloatField()
    warranty_information = models.TextField()
    shipping_information = models.TextField()
    availability_status = models.CharField(max_length=100)
    return_policy = models.TextField()
    minimum_order_quantity = models.IntegerField()
    thumbnail = models.ImageField(upload_to='images/')

class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    comment = models.TextField()
    date = models.DateField()
    reviewer_name = models.CharField(max_length=100)
    reviewer_email = models.EmailField()

class Meta(models.Model):
    id = models.IntegerField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    barcode = models.CharField(max_length=100)
    qrCode = models.CharField(max_length=100)

class Image(models.Model):
    id = models.IntegerField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.ImageField(upload_to='images/')

class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Dimension(models.Model):
    id = models.IntegerField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()