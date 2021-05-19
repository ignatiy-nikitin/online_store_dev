from django.core.mail import send_mail


# send_mail(
#     'Subject here',
#     'Here is the message.',
#     'from@example.com',
#     ['to@example.com'],
#     fail_silently=False,
# )

def send_email(final_order, user):
    subject = f'Номер заказа: {final_order.id}'
    message = f"""
    Клиент:
        id: {user.id}
        Имя: {user.username}
    
    Заказ:
        id: {final_order.id}
        Дата создания: {final_order.created_dt}
        Дата доставки: {final_order.delivery_dt}
        Адрес доставки: {final_order.address}
        Итоговая сумма заказа: {final_order.total_cost}


    Содержимое заказа:
    """
    for order_item in final_order.order.order_items.all():
        product_str = f"""
            Товар:
                Наименование: {order_item.product.name}
                Количество: {order_item.quantity}
                Итоговая цена: {order_item.total_price}

        """
        message += product_str

    send_mail(
        subject,
        message,
        'django.1c.mail.sender@gmail.com',
        ['ignat.no@yandex.ru'],
        fail_silently=False,
    )

#
#
# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
#     date_of_creation = models.DateTimeField(auto_now_add=True)
#     products = models.ManyToManyField(Product, through='OrderItem', blank=True)
#
#     @property
#     def total_cost(self):
#         return sum([order_item.total_price for order_item in self.order_items.all()])
#
#
# class OrderItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
#     quantity = models.PositiveIntegerField(default=0)
#     price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
#
#     # def __str__(self):
#     #     return f'CartItem {self.pk} of cart {self.cart.pk}'
#
#     @property
#     def total_price(self):
#         return self.quantity * self.price
#
#
# class OrderFinal(models.Model):
#     STATUS_CHOICES = [
#         ('created', 'создан'),
#         ('delivered', 'доставлен'),
#         ('processed', 'в процессе'),
#         ('cancelled', 'отменен'),
#     ]
#
#     created_dt = models.DateTimeField(auto_now_add=True)
#     delivery_dt = models.DateTimeField()
#     recipient = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders_final')
#     address = models.CharField(max_length=256)
#     order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='orders_final')
#     status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='orders_final')
#     total_cost = models.DecimalField(max_digits=8, decimal_places=2)