from django.contrib import admin

from products.models import Product, Category


# class ProductAdmin(admin.ModelAdmin):


admin.site.register(Product)
admin.site.register(Category)




# from django.contrib import admin
#
# from shipments.models import Shipment
#
#
# class ShipmentAdmin(admin.ModelAdmin):
#     readonly_fields = ('id',)
#
#
# admin.site.register(Shipment, ShipmentAdmin)
