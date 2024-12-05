from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    logo = models.URLField()
    rating = models.FloatField(default=0)
    description = models.TextField(blank=True, null=True)

class Product(models.Model):
    sku = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    supplier = models.ForeignKey(Supplier, related_name='products', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    image = models.URLField()
    delivery_time = models.CharField(max_length=255)
    description = models.TextField()
    retail_price = models.FloatField()
    wholesale_price = models.FloatField()
    min_order = models.IntegerField(default=1)

class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, related_name='characteristics', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

class Promotion(models.Model):
    title = models.CharField(max_length=255)
    image = models.URLField()
    link = models.URLField()

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='favorited_by', on_delete=models.CASCADE)

class CartItem(models.Model):
    user = models.ForeignKey(User, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('non-cash', 'Non-cash'),
        ('online', 'Online Payment'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_delivery', 'In Delivery'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    delivery_date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()