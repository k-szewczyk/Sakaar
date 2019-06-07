from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User

from halloffame.filters import HeroFilterSet, GuildFilterSet
from halloffame.models import Hero, Guild
from halloffame.permissions import IsOwnerOrReadOnly, UserPermissions
from halloffame.serializers import HeroSerializer, UserSerializer, GuildSerializer


class HeroViewSet(ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_class = HeroFilterSet
    ordering_fields = ('user__username', 'battles_won', 'battles_lost')
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer

    def get_queryset(self):
        return Hero.objects.get_annotations()


class UserViewSet(ModelViewSet):
    permission_classes = (UserPermissions,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GuildViewSet(ModelViewSet):
    queryset = Guild.objects.all()
    serializer_class = GuildSerializer
    filter_class = GuildFilterSet
