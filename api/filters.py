import django_filters

from api.models import Product

# category
# name
# address
# price
# view_count
# description
# lat
# lng
# created
# updated

class ProductFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')
    # price = django_filters.NumberFilter()
    # price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    # price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    # lat = django_filters.NumberFilter()
    # lat__gt = django_filters.NumberFilter(field_name='lat', lookup_expr='gt')
    # lat__lt = django_filters.NumberFilter(field_name='lat', lookup_expr='lt')

    # lng = django_filters.NumberFilter()
    # lng__gt = django_filters.NumberFilter(field_name='lng', lookup_expr='gt')
    # lng__lt = django_filters.NumberFilter(field_name='lng', lookup_expr='lt')



    class Meta:
        model = Product
        fields = {
            'category': ['in'],
            'price': ['lte', 'gte'],
            'lat': ['lte', 'gte'],
            'lng': ['lte', 'gte'],
        }
