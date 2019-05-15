from django_filters import FilterSet
from django_filters import filters

from .models import Hero


class HeroFilterSet(FilterSet):
    user_name = filters.CharFilter(field_name='user__username')
    is_alive = filters.BooleanFilter()

    class Meta:
        model = Hero
        fields = ('user_name', 'level', 'race', 'guild', 'is_alive')
