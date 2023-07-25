from .models import MenuItem, Category, Order, OrderItem, UserCart
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from decimal import Decimal

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):

    # category = CategorySerializer()
    # title = serializers.CharField(max_length=255, validators=[
    #     UniqueValidator(queryset=MenuItem.objects.all())
    #     ])

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CartSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = UserCart
        fields = ['id', 'user', 'menu_item', 'item_quantity', 'unit_price', 'price']

        read_only_fields = ['user','price',]

        extra_kwargs = {
            'item_quantity': {
                'required': True,
                'min_value': 1,
                }
        }

class OrderSerializer(serializers.ModelSerializer):


    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
