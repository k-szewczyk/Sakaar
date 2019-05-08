from rest_framework import serializers
from battles.services import Fight
from rest_framework.serializers import ValidationError
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

    def validate(self, attrs):
        attendees = attrs['attendees']
        if len(Battle.objects.filter(attendees__user=attendees[0]).filter(attendees__user=attendees[1])) > 0:
            raise ValidationError('Battle with those attendees already exists')
        return attrs
