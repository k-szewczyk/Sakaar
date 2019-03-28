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
    name = models.CharField(max_length=25)
    bonus_atk = models.IntegerField()


class Armor(Model):
    name = models.CharField(max_length=25)
    bonus_def = models.IntegerField()


class Hero(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, default=0, on_delete=models.SET_DEFAULT)
    fraction = models.ForeignKey(Fraction, default=0, on_delete=models.SET_DEFAULT)
    guild = models.ForeignKey(Guild, null=True, on_delete=models.SET_NULL)
    level = models.IntegerField(default=1)
    atk_points = models.IntegerField(default=1)
    def_points = models.IntegerField(default=1)
    equipped_weapon = models.ForeignKey(Weapon, blank=True, null=True, on_delete=models.SET_NULL)
    equipped_armor = models.ForeignKey(Armor, blank=True, null=True, on_delete=models.SET_NULL)
    is_alive = models.BooleanField(default=True)
