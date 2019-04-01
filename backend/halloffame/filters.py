from django_filters import FilterSet
from django_filters import filters
from .models import Hero


class HeroFilterSet(FilterSet):
    user_name = filters.CharFilter(field_name='user__username')

    class Meta:
        model = Hero
        fields = ('level', 'race', 'fraction', 'guild', 'user_name')
