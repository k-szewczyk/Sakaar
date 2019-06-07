from django_filters import FilterSet
from django_filters import filters

from halloffame.models import Hero
from halloffame.models import Hero, Guild



class HeroFilterSet(FilterSet):
    user_name = filters.CharFilter(field_name='user__username')
    find_opponents_for = filters.ModelChoiceFilter(method='get_available_opponents', label="find opponents for",
                         queryset=Hero.objects.all())
    is_alive = filters.BooleanFilter(label='is alive')

    class Meta:
        model = Hero
        fields = ('user_name', 'race', 'guild', 'is_alive', 'find_opponents_for')

    def get_available_opponents(self, queryset, name, value: Hero):
        available_heroes = Hero.objects.get_annotations().filter(
            is_alive=True, race__in=value.race.can_fight_with.all()
            ).exclude(user=value.user).exclude(battles__in=value.battles.all())

        return available_heroes

        fields = ('level', 'race', 'guild', 'user_name')


class GuildFilterSet(FilterSet):
    class Meta:
        model = Guild

