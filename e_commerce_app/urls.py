from rest_framework import routers
from e_commerce_app import views
from django.urls import path
from .views import BuyViewSet, BuyCartItemsViewSet


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'cart', views.CartViewSet)
# router.register(r'buy', views.BuyViewSet)

urlpatterns = [
    path('buy/', BuyViewSet.as_view()),
    path('buy/<int:id>/', BuyViewSet.as_view()),
    path('buycartitems/', BuyCartItemsViewSet.as_view()),
]