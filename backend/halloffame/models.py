from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Count


class HeroSet(models.QuerySet):
    def get_annotations(self):
        return self.annotate(
            is_alive=~models.Exists(Hero.objects.filter(pk=models.OuterRef('pk'), lost_battles__is_looser_dead=True)),
            battles_lost=Count('lost_battles'),
            battles_won=Count(F('battles')) - Count(F('lost_battles')),
            last_battle_date=models.Max('battles__date'))


class Race(models.Model):
    name = models.CharField(max_length=25)
    can_fight_with = models.ManyToManyField("self")

    def __str__(self):
        return self.name


class Guild(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Hero(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    guild = models.ForeignKey(Guild, related_name='heroes', null=True, on_delete=models.SET_NULL)
    hit_points = models.PositiveSmallIntegerField(default=100)

    level = models.PositiveSmallIntegerField(default=1)
    exp = models.PositiveIntegerField(default=0)
    atk_points = models.PositiveSmallIntegerField(default=1)
    def_points = models.PositiveSmallIntegerField(default=1)

    objects = HeroSet.as_manager()

    def __str__(self):
        return self.user.username
