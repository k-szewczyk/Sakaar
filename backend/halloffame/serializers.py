from rest_framework import serializers

from .models import Hero


class HeroSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user', read_only=True)
    is_alive = serializers.BooleanField(read_only=True)
    battles_won = serializers.IntegerField(read_only=True)
    battles_lost = serializers.IntegerField(read_only=True)
    last_battle_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Hero
        fields = ('user_name', 'race', 'guild', 'level', 'is_alive', 'battles_won', 'battles_lost', 'last_battle_date')
