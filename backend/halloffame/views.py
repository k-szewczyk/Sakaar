from rest_framework.viewsets import ModelViewSet

from .filters import HeroFilterSet
from .models import Hero
from .serializers import HeroSerializer
from .permissions import IsOwnerOrReadOnly


class HeroViewSet(ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
    filter_class = HeroFilterSet

    def get_queryset(self):
        return Hero.objects.get_annotations()
