from rest_framework.viewsets import ModelViewSet

from battles.models import Battle, Round
from battles.permissions import IsStaffOrReadOnly
from battles.serializers import BattleSerializer, RoundSerializer


class BattleViewSet(ModelViewSet):
    permission_classes = (IsStaffOrReadOnly,)
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer
    http_method_names = ['get', 'post', 'head']


class RoundViewSet(ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        return Round.objects.filter(battle=self.kwargs['battle_pk'])
