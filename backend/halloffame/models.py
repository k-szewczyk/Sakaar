from django.contrib.auth.models import User
from django.db import models


class HeroSet(models.QuerySet):
    def get_annotations(self):
        return self.annotate(
            is_alive=~models.Exists(Hero.objects.filter(pk=models.OuterRef('pk'), loosed_battles__is_looser_dead=True)),
            battles_lost=models.Count('loosed_battles'),
            battles_won=models.Count('battles') - models.Count('loosed_battles'),
            last_battle_date=models.Max('battles__date'))


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

    objects = HeroSet.as_manager()

    def __str__(self):
        return self.user.username
