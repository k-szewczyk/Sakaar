from rest_framework import serializers
from django.core.exceptions import ValidationError

from battles.models import Battle, Round


class BattleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Battle
        fields = ('attendees', 'looser', 'is_looser_dead', 'rounds')

    def validate(self, attrs):
        user = self.context['request'].user
        if attrs['user'] == user:
            return attrs

        raise ValidationError("You don't have permissions to do that.")
