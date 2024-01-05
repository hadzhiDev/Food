from django_filters import rest_framework as filters

from .models import Food


class FoodFilter(filters.FilterSet):
    created_at = filters.DateRangeFilter()

    class Meta:
        model = Food
        fields = ['category',]