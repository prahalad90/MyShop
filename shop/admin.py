from django.contrib import admin
from shop.models import *

# Register your models here.
admin.site.register(Brand)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
@admin.register(Cart)
class cartAdmin(admin.ModelAdmin):
    list_display=['trackingcode','product']
@admin.register(Order)
class orderAdmin(admin.ModelAdmin):
    list_display=['order_no','trackingcode','orderValue','status']
@admin.register(Shipping)
class shippingAdmin(admin.ModelAdmin):
    list_display=['trackingcode','F_name']
