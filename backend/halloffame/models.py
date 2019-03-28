from django.db.models import Model, IntegerField, ForeignKey, BooleanField, OneToOneField
from django.db.models import SET_NULL, CASCADE, CharField, SET_DEFAULT, DateTimeField
from django.contrib.auth.models import User


class Race(Model):
    name = CharField(max_length=25)


class Fraction(Model):
    name = CharField(max_length=25)


class Guild(Model):
    name = CharField(max_length=25)


class Weapon(Model):
    name = CharField(max_length=25)
    bonus_atk = IntegerField()


class Armor(Model):
    name = CharField(max_length=25)
    bonus_def = IntegerField()


class Hero(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    race = ForeignKey(Race, default=0, on_delete=SET_DEFAULT)
    fraction = ForeignKey(Fraction, default=0, on_delete=SET_DEFAULT)
    guild = ForeignKey(Guild, null=True, on_delete=SET_NULL)
    level = IntegerField(default=1)
    atk_points = IntegerField(default=1)
    def_points = IntegerField(default=1)
    equipped_weapon = ForeignKey(Weapon, blank=True, null=True, on_delete=SET_NULL)
    equipped_armor = ForeignKey(Armor, blank=True, null=True, on_delete=SET_NULL)
    is_alive = BooleanField(default=True)
    battles_won = IntegerField(default=0)
    battles_lost = IntegerField(default=0)


class Battle(Model):
    winner = ForeignKey(Hero, related_name='winner', null=True, on_delete=SET_NULL)
    looser = ForeignKey(Hero, related_name='looser', null=True, on_delete=SET_NULL)
    looser_died = BooleanField()
    date = DateTimeField()
