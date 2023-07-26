from rest_framework import permissions


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user.groups.filter(name='Manager').exists()
        

class IsManagerOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()
    

class IsDeliveryCrewOrManager(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user.groups.filter(name='delivery_crew').exists() or request.user.groups.filter(name='Manager').exists()