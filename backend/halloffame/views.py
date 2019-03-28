from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import HeroSerializer
from .models import Hero


class HeroViewSet(ModelViewSet):
    serializer_class = HeroSerializer
    queryset = Hero.objects.all()