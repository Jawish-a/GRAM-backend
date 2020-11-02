from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.utils.timezone import timedelta, timezone
import uuid


'''
Models for Address
'''

class Country(models.Model):
    name = models.CharField(max_length=191)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=191)

    def __str__(self):
        return self.title


class Address(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=191)
    address_line_1 = models.CharField(max_length=191)
    address_line_2 = models.CharField(max_length=191, blank=True, null=True)
    address_type = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    counrty = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.city} {self.address_line_1} - {self.counrty}'


'''
Models for Product
'''
class Product(models.Model):
    name = models.CharField(max_length=191)
    description = models.TextField()
    # price can be up to 99999.99
    price = models.DecimalField(decimal_places=2, max_digits=7)
    stock = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.name}'

class Image(models.Model):
    url = models.CharField(max_length=191)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.url}'


'''
Models for Order
'''
class Order(models.Model):
    uuid = models.CharField(max_length=191)
    # Increase max digits to match or exceed product decimal field
    # Recommendation: Switch DecimalField to FloatField
    total = models.DecimalField(decimal_places=2, max_digits=5)
    created_date = models.DateTimeField(auto_now_add=True)
    tax = models.DecimalField(decimal_places=2, max_digits=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.uuid} - {self.user.first_name} {self.user.last_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    # so that 2 or more orders can have the same item
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    # fix the price subtotal no more than 3 places
    line_item_total = models.DecimalField(decimal_places=2, max_digits=10)
    
    def __str__(self):
        return f'{self.order} {self.product}'
