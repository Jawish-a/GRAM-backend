from xCommerce.models import Product ,Image
from rest_framework import serializers
from django.contrib.auth.models import User
# this is to genrate the token after the user signup
from rest_framework_simplejwt.tokens import RefreshToken


class ListProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['name','price' ,'image']
    
    def get_image(self, obj):
      image = obj.images.filter(is_featured=True).first().url
      return image


class DetaileProductSerializer(serializers.ModelSerializer):
    images = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='url'
    )
    class Meta:
        model = Product
        fields = ['name','price' ,'images' ,'description' , 'stock']


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True, allow_blank=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'token']

    def create(self, validated_data):
        # creates the user with all its details
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        new_user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        # generate the token for the user so that he can login
        token = RefreshToken.for_user(new_user)
        validated_data["token"] = token
        return validated_data
