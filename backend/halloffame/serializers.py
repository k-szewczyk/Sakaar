from django.core.exceptions import ValidationError
from rest_framework import serializers

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers


from halloffame.models import Hero, Guild


class HeroSerializer(serializers.ModelSerializer):
    is_alive = serializers.BooleanField(read_only=True)
    battles_won = serializers.IntegerField(read_only=True)
    battles_lost = serializers.IntegerField(read_only=True)
    last_battle_date = serializers.DateTimeField(read_only=True)
    level = serializers.IntegerField(read_only=True)

    class Meta:
        model = Hero
        fields = ('user', 'race', 'guild', 'is_alive', 'battles_won', 'battles_lost', 'last_battle_date')

    def validate(self, attrs):
        user = self.context['request'].user
        if attrs['user'] == user:
            return attrs

        raise ValidationError("You don't have permissions to do that.")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'},
                                     write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['username'],
                                   email=validated_data['email'],
                                   password=validated_data['password'])


class GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = ('name', 'heroes')
