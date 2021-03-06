from django.shortcuts import render
from django.contrib.auth.models import User

from .serializers import (
    SignUpSerializer,
    AddressListSerializer, AddAddressSerializer, CountrySerializer,
    ProductListSerializer, OrderListSerializer,
    OrderCheckoutSerializer, MyTokenObtainPairSerializer
)


from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner

from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView,
    RetrieveUpdateAPIView
)
from .models import Product, Address, Country, Order
from rest_framework_simplejwt.views import TokenObtainPairView



"""
Auth Views
"""

class SignUp(CreateAPIView):
    serializer_class = SignUpSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


"""
Product Views
"""

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


""" 
Order Views
"""

class OrderListView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(user)
        return user.orders.all()


class OrderCheckout(CreateAPIView):
    serializer_class = OrderCheckoutSerializer



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

