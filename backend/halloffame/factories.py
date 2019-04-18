import factory

from halloffame import models
from django.contrib.auth.models import User


class GuildFactory(factory.DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = models.Guild


class RaceFactory(factory.DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = models.Race


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('word')
    password = factory.Faker('password')


class HeroFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Hero

    id = factory.SubFactory(UserFactory)
    race = factory.SubFactory(RaceFactory)
    guild = factory.SubFactory(GuildFactory)
