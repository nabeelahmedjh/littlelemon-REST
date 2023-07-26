import django_filters
from .models import MenuItem, Order

class MenuItemFilter(django_filters.FilterSet):

    price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__title', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = MenuItem
        fields = ('category', 'price', 'title')


class OrderFilter(django_filters.FilterSet):

    status = django_filters.BooleanFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = Order
        fields = ('status',)
