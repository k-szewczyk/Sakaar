from rest_framework.viewsets import ModelViewSet

from django.db.models import Exists, OuterRef
from .filters import HeroFilterSet
from .models import Hero
from .serializers import HeroSerializer


class HeroViewSet(ModelViewSet):
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
    filter_class = HeroFilterSet

    def get_queryset(self):
        return Hero.objects.annotate(is_alive=~Exists(Hero.objects.filter(pk=OuterRef('pk'),
                                                                          loosed_battles__is_looser_dead=True)))

        # Hero.objects.annotate(death_date=Hero.objects.filter(pk=OuterRef('pk'), loosed_battles__is_looser_dead=True).first().loosed_battles) # TODO Make this work