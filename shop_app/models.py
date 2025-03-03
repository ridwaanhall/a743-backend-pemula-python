from django.db import models
import uuid

class Product(models.Model):
    """Model to store product data with soft delete functionality."""
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=False)
    description = models.TextField()
    shop = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    category = models.CharField(max_length=50)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    picture = models.URLField()
    is_delete = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name