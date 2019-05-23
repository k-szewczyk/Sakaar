from django_filters import FilterSet
from django_filters import filters

from halloffame.models import Hero


class HeroFilterSet(FilterSet):
    user_name = filters.CharFilter(field_name='user__username')
    find_opponents_for = filters.ModelChoiceFilter(method='available_opponents', label="find opponents for",
                         queryset=Hero.objects.all())
    is_alive = filters.BooleanFilter(label='is alive')

    class Meta:
        model = Hero
        fields = ('user_name', 'level', 'race', 'guild', 'is_alive', 'find_opponents_for')

    def available_opponents(self, queryset, name, value: Hero):
        hero_1 = value
        available_heroes = Hero.objects.get_annotations().filter(
            is_alive=True, race__in=hero_1.race.can_fight_with.all()).exclude(user=hero_1.user).exclude(
            battles__in=hero_1.battles.all()
        )
        return available_heroes
