from django.contrib.auth.models import User
from . import models
from rest_framework import viewsets, status
from e_commerce_app.serializers import UserSerializer
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer

# class BuyViewSet(viewsets.ModelViewSet):
#     queryset = models.Buy.objects.all()
#     print(queryset)
#     serializer_class = serializers.BuySerializer

# Direct Buy product
class BuyViewSet(APIView): 
    def post(self, request):
        serializer = serializers.BuySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            item = models.Product.objects.get(id=request.data.get('product'))
            updated_inventory = item.inventory - int(request.data['quantity'])
            data = {
                'inventory': updated_inventory
            }
            product_serializer = serializers.ProductSerializer(item, data=data, partial=True)

            if product_serializer.is_valid():
                product_serializer.save()
            else:
                return Response({"status": "error", "data": product_serializer.errors})

            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def get(self, request, id=None):
        if id:
            item = models.Buy.objects.get(id=id)
            serializer = serializers.BuySerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = models.Buy.objects.all()
        serializer = serializers.BuySerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

# Buy from cart
class BuyCartItemsViewSet(APIView): 
    def post(self, request):
        for item in request.data.get('product'):
            data = {
                'user': request.data.get('user'),
                'product': item['id'],
                'quantity': item['quantity'],
                'amount': item['amount'],
                'payment_method': request.data.get('payment_method')
            }

            serializer = serializers.BuySerializer(data=data)
        
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({"status": "error", "data": serializer.errors})

            # Updating product table inventory
            prod = models.Product.objects.get(id=item['id'])
            updated_inventory = prod.inventory - int(item['quantity'])
            data = {
                'inventory': updated_inventory
            }

            product_serializer = serializers.ProductSerializer(prod, data=data, partial=True)

            if product_serializer.is_valid():
                product_serializer.save()
            else:
                return Response({"status": "error", "data": product_serializer.errors})

            # Delete items from cart after user bought it
            cart_id = models.Cart.objects.filter(user=request.data.get('user')).values_list('id', flat=True).first()
            print(cart_id)
            item = get_object_or_404(models.Cart, id=cart_id)
            item.delete()
        # cart_id = models.Cart.objects.filter(user=request.data.get('user')).values_list('id', flat=True).first()
        # print(cart_id)
        return Response({"status": "success", "data": request.data})
        