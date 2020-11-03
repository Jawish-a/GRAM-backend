"""mystery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from xCommerce import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [

    path('admin/', admin.site.urls),
    # path('api/v1'),
    path('api/v1/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/v1/signup/', views.SignUp.as_view(), name='signup'),

    path('api/v1/products/', views.ProductListView.as_view(), name='product-list'),
    path('api/v1/products/<int:object_id>/',
         views.ProductDetailView.as_view(), name='product-detail'),

    path('api/v1/orders/', views.OrderListView.as_view(), name='order-list'),
    path('api/v1/orders/<int:object_id>/',
         views.OrderDetailView.as_view(), name='order-detail'),
    path('api/v1/order/checkout/', views.OrderCheckout.as_view(), name='order-checkout'),

    path('api/v1/country/list/', views.CountryList.as_view(), name='country-list'),

    path('api/v1/address/list/', views.AddressList.as_view(), name='address-list'),
    path('api/v1/address/add/', views.AddAddress.as_view(), name='address-add'),
    path('api/v1/address/<int:address_id>/update/',
         views.UpdateAddress.as_view(), name='address-update'),
    path('api/v1/address/<int:address_id>/delete/',
         views.DeleteAddress.as_view(), name='address-delete'),


]
