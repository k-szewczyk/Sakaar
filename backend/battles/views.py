from rest_framework.viewsets import ModelViewSet

from battles.models import Battle
from battles.permissions import IsStaffOrReadOnly
from battles.serializers import BattleSerializer


class BattleViewSet(ModelViewSet):
    permission_classes = (IsStaffOrReadOnly,)
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer

