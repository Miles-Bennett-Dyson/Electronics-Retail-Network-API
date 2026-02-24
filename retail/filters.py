from django_filters import rest_framework as filters

from retail.models import Retail


class CountryFilter(filters.FilterSet):
    country = filters.CharFilter(lookup_expr='iexact', field_name='country')

    class Meta:
        model = Retail
        fields = ['country']
