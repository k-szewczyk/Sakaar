from rest_framework.viewsets import ModelViewSet

from halloffame.filters import HeroFilterSet
from halloffame.models import Hero
from halloffame.permissions import IsOwnerOrReadOnly
from halloffame.serializers import HeroSerializer


class HeroViewSet(ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
    filter_class = HeroFilterSet

    def get_queryset(self):
        return Hero.objects.get_annotations()
