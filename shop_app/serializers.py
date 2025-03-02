from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'description', 'shop', 'location',
            'price', 'discount', 'category', 'stock', 'is_available',
            'picture', 'is_delete'
        ]
    
    def validate(self, data):
        if data['price'] < 0:
            raise serializers.ValidationError("Price cannot be negative")
        if data['stock'] < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return data

class ProductResponseSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'description', 'shop', 'location',
            'price', 'discount', 'category', 'stock', 'is_available',
            'picture', 'is_delete', '_links'
        ]

    def get__links(self, obj):
        request = self.context['request']
        base_url = request.build_absolute_uri('/products')
        return [
            {"rel": "self", "href": f"{base_url}", "action": "POST", "types": ["application/json"]},
            {"rel": "self", "href": f"{base_url}/{obj.id}/", "action": "GET", "types": ["application/json"]},
            {"rel": "self", "href": f"{base_url}/{obj.id}/", "action": "PUT", "types": ["application/json"]},
            {"rel": "self", "href": f"{base_url}/{obj.id}/", "action": "DELETE", "types": ["application/json"]}
        ]
