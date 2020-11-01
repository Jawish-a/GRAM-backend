from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import SignUpSerializer, ListProductSerializer ,DetaileProductSerializer
from rest_framework.generics import  CreateAPIView, ListAPIView ,RetrieveAPIView
from .models import Product

# Create your views here.
class SignUp(CreateAPIView):
	serializer_class = SignUpSerializer

class ListProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer


class DetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = DetaileProductSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'object_id'
