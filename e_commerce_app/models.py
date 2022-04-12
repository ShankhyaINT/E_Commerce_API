from django.db import models
from django.contrib.auth.models import User

# Product model
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    inventory = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()

# Cart model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()

# Buy model
class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=100)