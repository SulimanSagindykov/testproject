from rest_framework import serializers
from .models import (Supplier, Product, ProductCharacteristic)

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'logo', 'rating', 'description']

class ProductCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCharacteristic
        fields = ['name', 'value']

class ProductSerializer(serializers.ModelSerializer):
    characteristics = ProductCharacteristicSerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()
    suppliers = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'min_order', 'delivery_time',
            'city', 'description', 'characteristics', 'suppliers'
        ]