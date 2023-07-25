from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem, UserCart
# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(UserCart)
admin.site.register(Order)
admin.site.register(OrderItem)