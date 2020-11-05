from django.urls import path
from xCommerce import views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),

    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:object_id>/',
         views.ProductListView.as_view(), name='product-detail'),

    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('order/checkout/', views.OrderCheckout.as_view(), name='order-checkout'),

    path('country/list/', views.CountryList.as_view(), name='country-list'),

    path('address/list/', views.AddressList.as_view(), name='address-list'),
    path('address/add/', views.AddAddress.as_view(), name='address-add'),
    path('address/<int:address_id>/update/',
         views.UpdateAddress.as_view(), name='address-update'),
    path('address/<int:address_id>/delete/',
         views.DeleteAddress.as_view(), name='address-delete'),
]
