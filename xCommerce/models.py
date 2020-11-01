from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.utils.timezone import timedelta, timezone
import uuid

#########################################################################
#       user address model                                               #
#########################################################################
class Country(models.Model):
    name = models.CharField(max_length=191)
    def __str__(self):
        return f'{self.name}'

# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=10)
#     #create_at = models.DateTimeField(auto_now_add=True)
#     country = models.OneToOneField(Country, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'

class Category(models.Model):
    title = models.CharField(max_length=191)
    # parent = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="sub_category")
    # more to be here
    def __str__(self):
        return f'{self.title}'

class Address(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=10)
    city = models.CharField(max_length=191)
    address_line_1 = models.CharField(max_length=191)
    address_line_2 = models.CharField(max_length=191)
    # is_default = models.BooleanField(default=False)
    address_type = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    counrty = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.city} {self.street} - {self.counrty}, {self.extra} '

class Product(models.Model):
    name = models.CharField(max_length=10)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    stock = models.PositiveIntegerField()
    # featured_img_id = models.OneToOneField(Image, on_delete=models.CASCADE)
    # more fields to be here
    def __str__(self):
        return f'{self.name}'

class Image(models.Model):
    url = models.CharField(max_length=191)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_featured = models.BooleanField(default=False)
    # more fields to be here
    def __str__(self):
        return f'{self.url}'

class Order(models.Model):
    uuid = models.CharField(max_length=191)
    total = models.DecimalField(decimal_places=2, max_digits=5)
    created_date = models.DateTimeField(auto_now_add=True)
    tax = models.DecimalField(decimal_places=2, max_digits=5)
    # more to be here
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    def __str__(self):
        return f'{self.title}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    subtotal = models.DecimalField(decimal_places=2, max_digits=5)
    # more to be here
    def __str__(self):
        return f'{self.order} {self.product}'
