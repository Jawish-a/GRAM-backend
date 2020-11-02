from django.contrib import admin
from .models import Country, Category, Address, Product, Image, Order, OrderItem

admin.site.register(Country)
admin.site.register(Category)
admin.site.register(Address)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Order)
admin.site.register(OrderItem)
