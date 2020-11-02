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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
# """""Auth""""""""

    #path('token/refresh/', TokenRefreshView.as_view(), name="token-refresh"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),

     path('list/', views.ListProductView.as_view(), name='list'),
     path('detail/<int:object_id>/', views.DetailView.as_view(), name='detail'),

]