from django.contrib import admin

from products.models import Product, Category


# class ProductAdmin(admin.ModelAdmin):


admin.site.register(Product)
admin.site.register(Category)
