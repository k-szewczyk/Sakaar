from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import HeroSerializer
from .models import Hero
from .filters import HeroFilterSet


class HeroViewSet(ModelViewSet):
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
    filter_class = HeroFilterSet
