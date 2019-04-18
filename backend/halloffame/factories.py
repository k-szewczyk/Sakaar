import factory

from halloffame import models
from django.contrib.auth.models import User


class GuildFactory(factory.DjangoModelFactory):
    id = factory.Faker('random_number')
    name = factory.Faker('word')

    class Meta:
        model = models.Guild


class RaceFactory(factory.DjangoModelFactory):
    id = factory.Faker('random_number')
    name = factory.Faker('word')

    class Meta:
        model = models.Race
