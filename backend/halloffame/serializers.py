from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import Hero


class HeroSerializer(serializers.ModelSerializer):
    is_alive = serializers.BooleanField(read_only=True)
    level = serializers.IntegerField(read_only=True)
    battles_won = serializers.IntegerField(read_only=True)
    battles_lost = serializers.IntegerField(read_only=True)
    last_battle_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Hero
        fields = ('id', 'race', 'guild', 'level', 'is_alive', 'battles_won', 'battles_lost', 'last_battle_date')

    def validate(self, attrs):
        user = self.context['request'].user
        if attrs['id'] == user:
            return attrs

        raise ValidationError("You don't have permissions to do that.")
