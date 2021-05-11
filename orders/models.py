from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    date_of_creation = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderItem', blank=True)

    # @property
    # def total_cost(self):
    #     return sum([cart_item.total_price for cart_item in self.cart_items.all()])


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # def __str__(self):
    #     return f'CartItem {self.pk} of cart {self.cart.pk}'

    @property
    def total_price(self):
        return self.quantity * self.price


# class Category(models.Model):
#     ref = models.CharField(max_length=64)
#     # parent = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='categories')
#     name = models.CharField(max_length=64)
#
#
# class Vendor(models.Model):
#     ref = models.CharField(max_length=64)
#     name = models.CharField(max_length=128)
#
#
# class Product(models.Model):
#     ref = models.CharField(max_length=64)
#     name = models.CharField(max_length=64)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
#     description = models.TextField(blank=True)
#     vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products', null=True)
