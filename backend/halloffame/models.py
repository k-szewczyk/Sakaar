from django.db.models import Model
from django.db import models
from django.contrib.auth.models import User


class Race(Model):
    name = models.CharField(max_length=25)


class Fraction(Model):
    name = models.CharField(max_length=25)


class Guild(Model):
    name = models.CharField(max_length=25)


class Weapon(Model):
    name = models.CharField()
    bonus_atk = models.IntegerField()

class Armor(Model):
    name = models.CharField()
    bonus_def = models.IntegerField()


class Hero(Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.SET_DEFAULT)
    fraction = models.ForeignKey(Fraction, on_delete=models.SET_DEFAULT)
    guild = models.ForeignKey(Guild, null=True, on_delete=models.SET_NULL)
    level = models.IntegerField()
    atk_points = models.IntegerField()
    def_points = models.IntegerField()
    equipped_weapon = models.ForeignKey(Weapon, null=True, on_delete=models.SET_NULL)
    equipped_armor = models.ForeignKey(Armor, null=True, on_delete=models.SET_NULL)
    is_alive = models.BooleanField(default=True)