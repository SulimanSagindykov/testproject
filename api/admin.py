from django.contrib import admin
from .models import (
    Category, Subcategory, Supplier, Product,
    Promotion, Favorite, CartItem, Order, OrderItem
)
# Register your models here.

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Promotion)
admin.site.register(Favorite)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)