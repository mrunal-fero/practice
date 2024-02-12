from django.contrib import admin
from .models import Order, OrderItems, Item
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Item)
