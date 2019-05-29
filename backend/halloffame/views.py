from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from halloffame.filters import HeroFilterSet
from halloffame.models import Hero
from halloffame.permissions import IsOwnerOrReadOnly
from halloffame.serializers import HeroSerializer
from battles.models import Battle


class HeroViewSet(ModelViewSet):
    """This endpoint allows you to retrieve information about heroes

     user_name -- returns hero filtered by username
     """
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_class = HeroFilterSet
    ordering_fields = ('user__username', 'battles_won', 'battles_lost')
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer

    def get_queryset(self):
        return Hero.objects.get_annotations()
