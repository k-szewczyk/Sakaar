from django.contrib.auth.models import User
from django.db import models
from django.db.models import Exists, OuterRef

class Race(models.Model):
    name = models.CharField(max_length=25)
    can_fight_with = models.ManyToManyField("Race", blank=True, related_name='can_fight')

    def __str__(self):
        return self.name


class Guild(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Hero(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, default=0, on_delete=models.SET_DEFAULT)
    guild = models.ForeignKey(Guild, null=True, on_delete=models.SET_NULL)

    hit_points = models.PositiveIntegerField(default=100)
    level = models.PositiveIntegerField(default=1)
    exp = models.PositiveIntegerField(default=0)
    atk_points = models.IntegerField(default=1)
    def_points = models.PositiveIntegerField(default=1)

    @property
    def death_date(self):
        if self.loosed_battles.filter(is_looser_dead=True).exists():
            return self.loosed_battles.filter(is_looser_dead=True).first().date

    @property
    def battles_lost(self):
        return self.loosed_battles.count()

    @property
    def battles_won(self):
        return self.battles.count() - self.loosed_battles.count()

    def __str__(self):
        return self.user.username
