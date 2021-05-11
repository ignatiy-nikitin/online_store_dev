from django.db import models

from online_store_dev.settings import MEDIA_PRODUCT_IMAGE_DIR


class Category(models.Model):
    ref = models.CharField(max_length=64)
    # parent = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=64)


class Vendor(models.Model):
    ref = models.CharField(max_length=64)
    name = models.CharField(max_length=128)


class Product(models.Model):
    ref = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products', null=True)
    image = models.ImageField(upload_to=MEDIA_PRODUCT_IMAGE_DIR, default=MEDIA_PRODUCT_IMAGE_DIR + '/no_image.png')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=0)
