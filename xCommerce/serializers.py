from xCommerce.models import Product, Image, Address, Country, Order, OrderItem
from rest_framework import serializers
from django.contrib.auth.models import User
# this is to genrate the token after the user signup
from rest_framework_simplejwt.tokens import RefreshToken


'''
Product serializers
'''

class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    images = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='url'
        )

    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'images', 'id','description' , 'stock']

    def get_image(self, obj):
        image = obj.get_featured_image()
        return image



'''
Auth serializers
'''


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email',
                  'first_name', 'last_name', 'token']

    def create(self, validated_data):
        # creates the user with all its details
        new_user = User(**validated_data)
        new_user.set_password(validated_data['password'])
        new_user.save()
        # generate the token for the user so that he can login
        token = RefreshToken.for_user(new_user)
        validated_data["token"] = str(token.access_token)
        return validated_data


"""
Order Item Serializer
"""


class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    featured_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product_id', 'name', 'featured_image', 'is_available',
        'price', 'qty', 'line_item_total']

    def get_name(self, obj):
        return obj.product.name

    def get_is_available(self, obj):
        return (obj.product.stock > 0)

    def get_price(self, obj):
        return (obj.product.price)

    def get_featured_image(self, obj):
        return obj.product.get_featured_image()


'''
Order serializers
'''


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['uuid', 'total', 'created_date', 'tax', 'address', 'items']


class OrderDetailsSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['uuid', 'total', 'created_date', 'tax', 'address', 'items']

    def get_items(self, obj):
        items = obj.items.all()
        return items


'''
checkout serializers
'''


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'qty']


class OrderCheckoutSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'total', 'tax', 'address', 'items']
    
    def create(self, validated_data):
        items = validated_data['items']
        # Check for out of stock items
        for item in items:
            product = item['product']
            qty = item['qty']
            if (product.stock - qty) < 0:
                raise serializers.ValidationError("Some items out of stock")

        total = validated_data['total']
        tax = validated_data['tax']
        address = validated_data['address']
        request = self.context.get("request")
        new_order = Order( total=total, tax=tax, address=address, user=request.user )
        new_order.save()
        
        for item in items:
            product = item['product']
            qty = item['qty']
            if (product.stock - qty) >= 0:
                new_item = OrderItem(order=new_order, qty=qty, product=product )
                new_item.save()
            
        return validated_data  


'''
Address serializers
'''

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name']


class AddressListSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'city',
                  'address_line_1', 'address_line_2', 'address_type', 'country']
        # exclude = ['user']

    def get_country(self, obj):
        return obj.country.name


class AddAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['user']
