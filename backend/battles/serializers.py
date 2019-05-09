from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from battles.models import Battle, Round
from battles.services import Fight
from halloffame.models import Hero


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
        annotated_attendees = Hero.objects.get_annotations().filter(Q(user=attendees[0]) | Q(user=attendees[1]))
        for attendee in annotated_attendees:
            if not attendee.is_alive:
                raise ValidationError(f'Couldn\'t create fight player {attendee} is dead')

        races = [hero.race for hero in annotated_attendees]
        if not races[0] in races[1].can_fight_with.all():
            raise ValidationError(f'Heroes of races {races[0]} and {races[1]}')

        if len(Battle.objects.filter(attendees__user=attendees[0]).filter(attendees__user=attendees[1])) > 0:
            raise ValidationError('Battle with those attendees already exists')
        return attrs
