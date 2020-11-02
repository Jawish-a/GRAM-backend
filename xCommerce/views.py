from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import SignUpSerializer, ProductListSerializer, ProductDetailsSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .models import Product
from xCommerce.models import Order
from xCommerce.serializers import OrderDetailsSerializer, OrderListSerializer

"""
Auth Views
"""


class SignUp(CreateAPIView):
    serializer_class = SignUpSerializer


"""
Product Views
"""


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'object_id'


""" 
Order Views
"""


class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'object_id'
