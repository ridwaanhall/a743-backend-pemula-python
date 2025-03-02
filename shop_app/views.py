from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import ProductSerializer, ProductResponseSerializer
from .models import Product
from django.db.models import Q

class ProductList(GenericAPIView):
    """View to handle product creation and listing/searching."""
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_delete=False)

    def post(self, request, *args, **kwargs):
        """Create a new product with the provided data."""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_serializer = ProductResponseSerializer(
            serializer.instance, context={'request': request}
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        """Retrieve a list of products based on name or location."""
        name = request.query_params.get('name', None)
        location = request.query_params.get('location', None)
        products = self.get_queryset()

        if name:
            products = products.filter(
                Q(name__icontains=name) | Q(location__icontains=name)
            )
        if location:
            products = products.filter(
                Q(location__icontains=location) | Q(shop__icontains=location)
            )

        serializer = ProductResponseSerializer(
            products, many=True, context={'request': request}
        )
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)

class ProductDetail(GenericAPIView):
    """View to handle product details, updates, and deletion."""
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get_object(self):
        """Retrieve a product object or return 404 if not found."""
        try:
            return Product.objects.get(pk=self.kwargs['pk'], is_delete=False)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, pk, *args, **kwargs):
        """Retrieve product details by ID."""
        product = self.get_object()
        if isinstance(product, Response):
            return product
        serializer = ProductResponseSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """Update a product by ID."""
        product = self.get_object()
        if isinstance(product, Response):
            return product
        serializer = self.get_serializer(
            product, data=request.data, context={'request': request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_serializer = ProductResponseSerializer(
            serializer.instance, context={'request': request}
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        """Perform a soft delete on a product by ID."""
        product = self.get_object()
        if isinstance(product, Response):
            return product
        product.is_delete = True
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)