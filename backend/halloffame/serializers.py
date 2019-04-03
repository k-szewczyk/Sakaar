from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Hero


class HeroesRankingSerializer(ModelSerializer):
    user_name = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Hero
        fields = ('user_name', 'race', 'guild', 'level',
                  'death_date', 'battles_won', 'battles_lost', 'death_date')
