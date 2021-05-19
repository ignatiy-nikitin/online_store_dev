from django.conf import settings
from django.db import models

from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    date_of_creation = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderItem', blank=True)

    @property
    def total_cost(self):
        return sum([order_item.total_price for order_item in self.order_items.all()])


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # def __str__(self):
    #     return f'CartItem {self.pk} of cart {self.cart.pk}'

    @property
    def total_price(self):
        return self.quantity * self.price


class OrderFinal(models.Model):
    STATUS_CHOICES = [
        ('created', 'создан'),
        ('delivered', 'доставлен'),
        ('processed', 'в процессе'),
        ('cancelled', 'отменен'),
    ]

    created_dt = models.DateTimeField(auto_now_add=True)
    delivery_dt = models.DateTimeField()
    delivery_time_from = models.TimeField()
    delivery_time_to = models.TimeField()
    recipient = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders_final')
    address = models.CharField(max_length=256)
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='orders_final')
    extra_info = models.TextField()
    # status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='orders_final')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)

    # def __str__(self):
    #     return f'Order of user {self.recipient.username}'


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
