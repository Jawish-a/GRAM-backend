from django.shortcuts import render
from django.contrib.auth.models import User

from .serializers import (
    SignUpSerializer,
    AddressListSerializer, AddAddressSerializer, CountrySerializer,
    ProductListSerializer, ProductDetailsSerializer,
    OrderDetailsSerializer, OrderListSerializer
)


from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner

from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView,
    RetrieveUpdateAPIView
)
from .models import Product, Address, Country, Order

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
    permission_classes = [IsAuthenticated]


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'object_id'



""" 
Address Views
"""

class CountryList(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class AddressList(ListAPIView):
    serializer_class = AddressListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.addresses.all()


class AddAddress(CreateAPIView):
    serializer_class = AddAddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteAddress(DestroyAPIView):
    queryset = Address.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'address_id'
    permission_classes = [IsAuthenticated, IsOwner]


class UpdateAddress(RetrieveUpdateAPIView):
    serializer_class = AddAddressSerializer
    queryset = Address.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'address_id'
    permission_classes = [IsAuthenticated, IsOwner]

