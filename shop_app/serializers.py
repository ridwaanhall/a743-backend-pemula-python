from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for validating and saving product data."""
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'description', 'shop', 'location',
            'price', 'discount', 'category', 'stock', 'is_available',
            'picture', 'is_delete'
        ]

    def validate(self, data):
        """Custom validation to ensure price and stock are not negative."""
        if 'price' in data and data['price'] < 0:
            raise serializers.ValidationError("Price cannot be negative")
        if 'stock' in data and data['stock'] < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return data

class ProductResponseSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for product response with HATEOAS links."""
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'description', 'shop', 'location',
            'price', 'discount', 'category', 'stock', 'is_available',
            'picture', 'is_delete', 'createdAt', 'updatedAt', '_links'
        ]

    def get__links(self, obj):
        """Generate HATEOAS links for the product resource."""
        request = self.context.get('request')
        return [
            {
                "rel": "self",
                "href": reverse('product-list', request=request),
                "action": "POST",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": reverse('product-detail', kwargs={'pk': obj.pk}, request=request),
                "action": "GET",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": reverse('product-detail', kwargs={'pk': obj.pk}, request=request),
                "action": "PUT",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": reverse('product-detail', kwargs={'pk': obj.pk}, request=request),
                "action": "DELETE",
                "types": ["application/json"]
            }
        ]