from xCommerce.models import Product ,Image
from rest_framework import serializers
from django.contrib.auth.models import User

class ListProductSerializer(serializers.ModelSerializer):
    images=serializers.SerializerMethodField()
    class Meta:
        model = Product
        #fields = '__all__'
        fields = ['name','price' ,'images']
    def get_images(self, obj):
      images = Image.objects.filter(product=obj.id)
      return ImageSerializer(images, many=True).data


class DetaileProductSerializer(serializers.ModelSerializer):
    images=serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['name','price' ,'images' ,'description' , 'stock']

    def get_images(self, obj):
      images = Image.objects.filter(product=obj.id)
      return ImageSerializer(images, many=True).data
#    fields = ['name']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']



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