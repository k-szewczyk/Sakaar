from rest_framework import serializers
from battles.services import Fight

from battles.models import Battle, Round


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ('attacker', 'defender', 'hp_dealt')


class BattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ('attendees', 'looser', 'is_looser_dead', 'rounds', 'date')
        read_only_fields = ('looser', 'is_looser_dead', 'rounds', 'date')

    def create(self, validated_data):
        fight = Fight(validated_data['attendees'])
        fight.battle_loop()
        return fight.battle


