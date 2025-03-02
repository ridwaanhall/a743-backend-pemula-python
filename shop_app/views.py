from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer, ProductResponseSerializer
from django.db.models import Q

class ProductListView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_serializer = ProductResponseSerializer(
                serializer.instance, context={'request': request}
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        name = request.query_params.get('name', None)
        products = Product.objects.filter(is_delete=False)
        
        if name:
            products = products.filter(
                Q(name__icontains=name) | Q(location__icontains=name)
            )
        
        serializer = ProductResponseSerializer(
            products, many=True, context={'request': request}
        )
        return Response({"products": serializer.data})

class ProductDetailView(APIView):
    def get_object(self, product_id):
        try:
            return Product.objects.get(id=product_id, is_delete=False)
        except Product.DoesNotExist:
            return None

    def get(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response({"message": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductResponseSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response({"message": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = ProductResponseSerializer(
                serializer.instance, context={'request': request}
            )
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = self.get_object(product_id)
        if not product:
            return Response({"message": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        product.is_delete = True
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
