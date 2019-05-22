from django_filters import FilterSet
from django_filters import filters

from .models import Hero, Guild


class HeroFilterSet(FilterSet):
    user_name = filters.CharFilter(field_name='user__username')

    class Meta:
        model = Hero
        fields = ('level', 'race', 'guild', 'user_name')


class GuildFilterSet(FilterSet):
    class Meta:
        model = Guild
        fields = ('name', 'heroes')
