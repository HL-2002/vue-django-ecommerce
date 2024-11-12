# DJANGO SETUP
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_unchained.settings")
import django

django.setup()

import requests
from API import models
from datetime import datetime, timezone
import re
import random

""" THis is throwing two errors on execution:
1. django.core.exceptions.ImproperlyConfigured: Requested setting INSTALLED_APPS, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.
This one happens when the code actually executes.
2. No module named 'API'
This one happens when the imports are wrong.
3. django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
THis happens when I run it wirhout pipenv shell activated, and imports are well done.

DONE damn...

Ok, here's the deal:
The env wasn't the problem, my code was (as usual).

The errors where actually quite clear, and the solutions too, but the order of writing them wasn't.

I was importing the models before setting up the django environment, so the models weren't being loaded, and the error was thrown.
So, before doing ANYTHING, we gotta set the django settings in the shell environment, then setup django, then do the rest.
"""


def main():
    clearDB()
    for i in range(1, 31):
        fetchProduct(i)

    checkProduct(random.randint(1, 30))


def clearDB() -> None:
    """Clears the each table in the DB based in the order of the models"""
    models.Category.objects.all().delete()
    models.Product.objects.all().delete()
    models.Review.objects.all().delete()
    models.Meta.objects.all().delete()
    models.Image.objects.all().delete()
    models.Dimensions.objects.all().delete()
    models.Tag.objects.all().delete()
    models.ProductTag.objects.all().delete()


def fetchProduct(id: int) -> None:
    """Fetches a product from the API and saves it to the DB"""
    # fetch data
    req = requests.get(f"https://dummyjson.com/products/{id}")
    product = req.json()

    # Separate JSON into different objects
    reviews = product.pop("reviews")
    dimensions = product.pop("dimensions")
    tags = product.pop("tags")
    images = product.pop("images")
    meta = product.pop("meta")
    category = product.pop("category")

    # Create objects with model
    # For each one, validate it, save it, then get it from the DB for each foreign key
    # Category
    if len(models.Category.objects.filter(name=category)) == 0:
        categoryObj = models.Category(name=category)
        categoryObj.save()
    categoryObj = models.Category.objects.get(name=category)

    # Product
    if len(models.Product.objects.filter(title=product["title"])) == 0:
        productObj = models.Product(**product, category=categoryObj)
        productObj.save()
    productObj = models.Product.objects.get(title=product["title"])

    # Reviews
    for review in reviews:
        # Get YYYY, MM, DD, HH, MM, SS, sss from the date string
        match = re.match(
            r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})T(?P<hour>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2}).(?P<ms>\d{3})Z",
            review["date"],
        )
        match = match.groupdict()
        # Then create a datetime object with it
        review["date"] = datetime(
            year=int(match["year"]),
            month=int(match["month"]),
            day=int(match["day"]),
            hour=int(match["hour"]),
            minute=int(match["min"]),
            second=int(match["sec"]),
            microsecond=int(match["ms"]),
            tzinfo=timezone.utc,
        )
        reviewObj = models.Review(**review, product=productObj)
        reviewObj.save()

    # Meta
    metaObj = models.Meta(**meta, product=productObj)
    metaObj.save()

    # Image
    for image in images:
        imageObj = models.Image(url=image, product=productObj)
        imageObj.save()

    # Dimensions
    dimensionsObj = models.Dimensions(**dimensions, product=productObj)
    dimensionsObj.save()

    # Tags
    # Get all tags
    dbTags = models.Tag.objects.all()
    for tag in tags:
        if len(dbTags.filter(name=tag)) == 0:
            tagObj = models.Tag(name=tag)
            tagObj.save()

    # Product tags
    for tag in tags:
        tagObj = models.Tag.objects.get(name=tag)
        productTag = models.ProductTag(tag=tagObj, product=productObj)
        productTag.save()


def checkProduct(id: int) -> None:
    """Check if the product is already in the DB"""
    print('Product: ', models.Product.objects.filter(id=id))
    print('Reviews: ', models.Review.objects.filter(product=id))
    print('Meta: ', models.Meta.objects.filter(product=id))
    print('Images: ', models.Image.objects.filter(product=id))
    print('Dimensions: ', models.Dimensions.objects.filter(product=id))
    print('Tags: ', models.ProductTag.objects.filter(product=id))


if __name__ == "__main__":
    main()
