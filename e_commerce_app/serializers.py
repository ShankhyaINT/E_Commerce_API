from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'date_joined']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'product_name', 'manufacturer', 'inventory', 'amount')

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ('id', 'user', 'product', 'quantity', 'amount')

class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Buy
        fields = ('id', 'user', 'product', 'quantity', 'amount', 'payment_method', 'datetime')