from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Hero, Battle


class HeroSerializer(ModelSerializer):
    user_name = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Hero
        fields = ('user_name', 'race', 'fraction', 'guild', 'level', 'is_alive')


class BattleSerializer(ModelSerializer):
    class Meta:
        model = Battle
        fields = ('winner', 'looser', 'date', 'looser_died')
