# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
#
# class User(AbstractUser):
#     company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='users', verbose_name='Компания')
#     blocked = models.BooleanField(default=False, verbose_name='Заблокирован администратором')
#     name = models.CharField(max_length=264, blank=True, verbose_name='ФИО пользователя')
#
#     first_name = None
#     last_name = None
