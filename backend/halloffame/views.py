from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User

from halloffame.filters import HeroFilterSet
from halloffame.models import Hero
from halloffame.permissions import IsOwnerOrReadOnly, UserPermissions
from halloffame.serializers import HeroSerializer, UserSerializer


class HeroViewSet(ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
    filter_class = HeroFilterSet

    def get_queryset(self):
        return Hero.objects.get_annotations()


class UserViewSet(ModelViewSet):
    permission_classes = (UserPermissions,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

