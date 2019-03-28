from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import HeroSerializer, BattleSerializer
from .models import Hero, Battle
from .filters import HeroFilterSet


class HeroViewSet(ModelViewSet):
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
    filter_class = HeroFilterSet

class BattleViewSet(ModelViewSet):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer

