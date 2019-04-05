from rest_framework import serializers
from .models import Hero


class HeroSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user', read_only=True)
    is_alive = serializers.BooleanField()
    class Meta:
        model = Hero
        fields = ('user_name', 'race', 'guild', 'level', 'is_alive', 'battles_won', 'battles_lost', 'death_date', 'is_alive')

