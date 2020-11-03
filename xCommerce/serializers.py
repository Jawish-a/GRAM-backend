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

    class Meta:
        model = Product
        fields = ['name', 'price', 'image']

    def get_image(self, obj):
        image = obj.images.filter(is_featured=True).first().url
        return image


class ProductDetailsSerializer(serializers.ModelSerializer):
    images = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='url'
    )

    class Meta:
        model = Product
        fields = ['name', 'price', 'images', 'description', 'stock']


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
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        new_user = User(username=username, email=email,
                        first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        # generate the token for the user so that he can login
        token = RefreshToken.for_user(new_user)
        validated_data["token"] = token
        return validated_data


"""
Order Item Serializer
"""


class OrderItemListSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.SerializerMethodField()
    featured_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product', 'name', 'featured_image']

    def get_name(self, obj):
        return obj.product.name

    def get_featured_image(self, obj):
        return obj.product.images.filter(is_featured=True).first().url


class OrderItemDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    featured_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product_id', 'name', 'featured_image', 'is_available',
                  'featured_image', 'price', 'qty', 'line_item_total']

    def get_name(self, obj):
        return obj.product.name

    def get_is_available(self, obj):
        return (obj.product.stock > 0)

    def get_price(self, obj):
        return (obj.product.price)

    def get_featured_image(self, obj):
        return obj.product.images.filter(is_featured=True).first().url


'''
Order serializers
'''


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemListSerializer(many=True)

    class Meta:
        model = Order
        fields = ['uuid', 'total', 'created_date', 'tax', 'address', 'items']


class OrderDetailsSerializer(serializers.ModelSerializer):
    items = OrderItemDetailSerializer(many=True)

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
            total = validated_data['total']
            tax = validated_data['tax']
            address = validated_data['address']
            request = self.context.get("request")
            new_order = Order( total=total, tax=tax, address=address, user=request.user )
            new_order.save()
            
            items = validated_data['items']
            for item in items:
                product = item['product']
                qty = item['qty']
                # subtotal = 50
                # subtotal = item['subtotal']
                subtotal = float(product.price * qty)
                new_item = OrderItem(order=new_order, subtotal=subtotal, qty=qty, product=product )
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
