from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import ProductSerializer, ProductResponseSerializer
from .models import Product
from django.db.models import Q

class ProductList(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
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
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)

class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk, is_delete=False)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductResponseSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_serializer = ProductResponseSerializer(
                serializer.instance, context={'request': request}
            )
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.is_delete = True
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)