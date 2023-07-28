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

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source='category', 
        write_only=True
        )
    # title = serializers.CharField(max_length=255, validators=[
    #     UniqueValidator(queryset=MenuItem.objects.all())
    #     ])

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category_id', 'category']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserCart
        fields = ['id', 'user', 'menu_item', 'item_quantity', 'unit_price', 'price']

        read_only_fields = ['user','price','unit_price']

        extra_kwargs = {
            'item_quantity': {
                'required': True,
                'min_value': 1,
                }
        }

        # set value of price and unit_price

    def create(self, validated_data):
        
        validated_data['unit_price'] = validated_data['menu_item'].price
        validated_data['price'] = validated_data['menu_item'].price * validated_data['item_quantity']
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_menu_item(self, value):
        if UserCart.objects.filter(user=self.context['request'].user, menu_item=value).exists():
            raise serializers.ValidationError("Item already exists in cart")
        return value
    


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuItem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):

    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items']

        read_only_fields = ['user', 'total', 'date', 'order_items']
        required_fields = ['status', 'delivery_crew']
    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        order_item_serializer = OrderItemSerializer(order_items, many=True)
        return order_item_serializer.data
    

class OrderStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        read_only_fields = ['user', 'total', 'date']


class statusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['status']