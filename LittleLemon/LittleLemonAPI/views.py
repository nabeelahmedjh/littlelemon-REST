from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response


from .serializers import CategorySerializer, MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer, OrderStatusSerializer, statusSerializer
from .models import MenuItem, UserCart, Order, OrderItem, Category
from .filters import MenuItemFilter, OrderFilter
from .permissions import IsManager, IsManagerOnly, IsDeliveryCrewOrManager
from .throttles import GroupSpecificThrottle

from django.contrib.auth.models import User, Group
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView
from django.urls import reverse
from decimal import Decimal


import requests

# Create your views here.


class CategoryView(APIView):

    permission_classes = [IsAuthenticated, IsManager]



    def get(self, request):

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


    def post(self, request):

        serilaizer = CategorySerializer(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response(serilaizer.data, status=HTTP_201_CREATED)
        return Response(serilaizer.errors, status=HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAuthenticated, IsManager])
def menuItemView(request):

    if request.method == 'GET':

        paginator = PageNumberPagination()
        paginator.page_size = 2

        queryset = MenuItem.objects.all()
        filter = MenuItemFilter(request.GET, queryset=queryset)

        ordering = request.GET.get('ordering', None)
        if filter.is_valid():
            menuItem = filter.qs
        
        if ordering:
            ordering = ordering.split(',')
            menuItem = menuItem.order_by(*ordering)

        result_page = paginator.paginate_queryset(menuItem, request)
        serializer = MenuItemSerializer(result_page, many=True)
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


        serializer = CartSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
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
@throttle_classes([AnonRateThrottle, UserRateThrottle])
@permission_classes([IsAuthenticated])
def ordersView(request):
    
    if request.method == "GET":
        
        paginator = PageNumberPagination()
        paginator.page_size = 2
        if request.user.groups.filter(name='Manager').exists():
            queryset = Order.objects.all()
        elif request.user.groups.filter(name='delivery_crew').exists():
            queryset = Order.objects.filter(delivery_crew=request.user)
        else:
            queryset = Order.objects.filter(user=request.user)

        filter = OrderFilter(request.GET, queryset=queryset)
        if filter.is_valid():
            orders = filter.qs

        result_page = paginator.paginate_queryset(orders, request)

        serializer = OrderSerializer(result_page, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    

    elif request.method == "POST":

        request._request.method = 'GET'
        response = cartItemsView(request._request)

        items = response.data
        if not items:
            return Response({
                'message': 'Cart is empty'
            }, status=HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user, total=0)



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
    

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, IsDeliveryCrewOrManager])
def orderDetailView(request, pk):

    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({
            'message': 'Order not found'
        }, status=HTTP_404_NOT_FOUND)
            
    if request.method == 'GET':
            
            if order.user != request.user:
                return Response({
                    'message': 'You are not allowed to view this order'
                }, status=HTTP_403_FORBIDDEN)
            # orderItems = OrderItem.objects.filter(order=order)

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=HTTP_200_OK)
    

    elif request.method == 'DELETE':
        
        if User.objects.filter(groups__name='Manager').exists():
            order.delete()
            return Response({
                'message': 'Order deleted successfully'
            }, status=HTTP_200_OK) 
    
    elif request.method == 'PUT':


        if request.user.groups.filter(name='delivery_crew').exists():

            serializer = statusSerializer(order, request.data)
            # update status of the order
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


        if request.user.groups.filter(name='Manager').exists():

            serializer = OrderSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

    elif request.method == 'PATCH':
        
        if request.user.groups.filter(name='delivery_crew').exists():

            serializer = statusSerializer(order, request.data, partial=True)
            # update status of the order
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


        if request.user.groups.filter(name='Manager').exists():

            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    
