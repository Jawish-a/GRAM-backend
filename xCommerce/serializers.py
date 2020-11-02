from xCommerce.models import Product ,Image
from rest_framework import serializers
from django.contrib.auth.models import User


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
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        return validated_data