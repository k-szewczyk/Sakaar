from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from halloffame.filters import HeroFilterSet
from halloffame.models import Hero
from halloffame.permissions import IsOwnerOrReadOnly
from halloffame.serializers import HeroSerializer


class HeroViewSet(ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_class = HeroFilterSet
    ordering_fields = ('user__username', 'battles_won', 'battles_lost')
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer

    def get_queryset(self):
        return Hero.objects.get_annotations()
