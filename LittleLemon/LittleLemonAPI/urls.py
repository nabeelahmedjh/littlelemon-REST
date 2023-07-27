from django.urls import path
from . import views


urlpatterns = [

    path('categories/', views.CategoryView.as_view(), name='categories'),

    path('menu-items/', views.menuItemView, name='menu-items'),
    path('menu-items/<int:pk>/', views.menuItemDetailView, name='menu-item-detail'),

    path('groups/manager/users/', views.managerUserView, name='manager-users'),
    path('groups/manager/users/<int:pk>/', views.managerUserDetailView, name='manager-user-detail'),

    path('groups/delivery-crew/users/', views.deliveryCrewUserView, name='delivery-crew-users'),
    path('groups/delivery-crew/users/<int:pk>/', views.deliveryCrewUserDetialView, name='delivery-crew-user-detail'),

    path('cart/menu-items/', views.cartItemsView, name='cart'),


    path('orders/', views.ordersView, name='orders'),
    path('orders/<int:pk>/', views.orderDetailView, name='order-detail')



]
