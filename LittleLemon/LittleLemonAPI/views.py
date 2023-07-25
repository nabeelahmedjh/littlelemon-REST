from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer
from .models import MenuItem, UserCart, Order, OrderItem


from django.contrib.auth.models import User, Group
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager, IsManagerOnly

from django.urls import reverse
from decimal import Decimal


import requests

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsManager])
def menuItemView(request):

    if request.method == 'GET':
        menuItem = MenuItem.objects.all()
        serializer = MenuItemSerializer(menuItem, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    else:
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, IsManager])
def menuItemDetailView(request, pk):

    try:
        menuItem = MenuItem.objects.get(id=pk)
    except MenuItem.DoesNotExist:
        return Response({
            'message': '404 - Not Found'
        }, status=HTTP_404_NOT_FOUND)
    


    if request.method == 'GET':
            serializer = MenuItemSerializer(menuItem)
            return Response(serializer.data, status=HTTP_200_OK)
        
    elif request.method == 'DELETE':
            menuItem.delete()
            return Response({
                'message': 'Item deleted successfully'
            }, HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = MenuItemSerializer(menuItem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
    elif request.method == 'PATCH':
        serializer = MenuItemSerializer(menuItem, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsManagerOnly])
def managerUserView(request):

    if request.method == 'GET':
        manager_users = User.objects.filter(groups__name='Manager')
        serializer = UserSerializer(manager_users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    

    elif request.method == 'POST':


        if 'username' not in request.data:
            return Response({
                'message': 'Username is required'
            }, status=HTTP_400_BAD_REQUEST)
        

        try:
            user = User.objects.get(username=request.data['username'])
            manager_group = Group.objects.get(name='Manager')
            manager_group.user_set.add(user)

        except User.DoesNotExist:
            return Response({
                'message': 'User not found'
            }, status=HTTP_404_NOT_FOUND)
        
        return Response({
            'message': 'User Added to the Manager group'
        }, status=HTTP_201_CREATED)
        

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsManagerOnly])
def managerUserDetailView(request, pk):

    try:
        user = User.objects.get(id=pk)
        user_group = user.groups.get(name='Manager')
        user_group.user_set.remove(user)
        return Response({
            'message': f'{user} removed from the Manager group'
        }, status=HTTP_200_OK)
    except User.DoesNotExist:
        return Response({
            'message': 'User not found'
        }, status=HTTP_404_NOT_FOUND)
    except Group.DoesNotExist:
        return Response({
            'message': 'User is not a Manager'
        }, status=HTTP_400_BAD_REQUEST)
    



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsManagerOnly])
def deliveryCrewUserView(request):

    if request.method == 'GET':
        delivery_crew = User.objects.filter(groups__name='delivery_crew')
        serializer = UserSerializer(delivery_crew, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    

    elif request.method == 'POST':

        if 'username' not in request.data:
            return Response({
                'message': 'Username is required'
            }, status=HTTP_400_BAD_REQUEST)
        

        try:
            user = User.objects.get(username=request.data['username'])
            manager_group = Group.objects.get(name='delivery_crew')
            manager_group.user_set.add(user)

        except User.DoesNotExist:
            return Response({
                'message': 'User not found'
            }, status=HTTP_404_NOT_FOUND)
        
        return Response({
            'message': 'User Added to the Delivery crew group'
        }, status=HTTP_201_CREATED)
        

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsManagerOnly])
def deliveryCrewUserDetialView(request, pk):

    try:
        user = User.objects.get(id=pk)
        user_group = user.groups.get(name='delivery_crew')
        user_group.user_set.remove(user)
        return Response({
            'message': f'{user} removed from the delivery crew group'
        }, status=HTTP_200_OK)
    except User.DoesNotExist:
        return Response({
            'message': 'User not found'
        }, status=HTTP_404_NOT_FOUND)
    except Group.DoesNotExist:
        return Response({
            'message': 'User is not a in the delivery crew group'
        }, status=HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cartItemsView(request):

    if request.method == 'GET':
        cart_items = UserCart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = CartSerializer(data=request.data)

        itemAlreadyExist = UserCart.objects.filter(user=request.user, menu_item=request.data['menu_item'])
        if itemAlreadyExist:
            return Response({
                'message': 'Item already exist in the cart'
            }, status=HTTP_400_BAD_REQUEST)


        if serializer.is_valid():
            unit_price = MenuItem.objects.get(id=request.data['menu_item']).price
            total_price = serializer.validated_data['item_quantity'] * unit_price
            serializer.save(user=request.user, unit_price=unit_price, price=total_price)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST) 
        
        
    elif request.method == 'DELETE':
            cart_items = UserCart.objects.filter(user=request.user)
            cart_items.delete()
            return Response({
                'message': 'Cart items deleted successfully'
            }, status=HTTP_200_OK)
        

@api_view(['GET', 'POST'])
def ordersView(request):
    
    if request.method == "GET":
        if request.user.groups.filter(name='Manager').exists():
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    elif request.method == "POST":
        order = Order.objects.create(user=request.user, total=0)

        request._request.method = 'GET'
        response = cartItemsView(request._request)
        items = response.data
        # add all the items into order items
        for item in items:
            OrderItem.objects.create(
            order=order,
            menuItem_id=item['menu_item'],
            quantity=item['item_quantity'],
            unit_price=item['unit_price'], 
            price=item['price']
            )

            order.total += Decimal(item['price'])
        order.save()
        # delete all the items from the cart
        request._request.method = 'DELETE'
        cartItemsView(request._request)

        return Response({
            'message': 'Order placed successfully'
        }, status=HTTP_201_CREATED)