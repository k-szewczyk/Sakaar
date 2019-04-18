from django.contrib.auth.models import User
from django.db import models


class Race(models.Model):
    """
    Fields:
        - name - contains name
        - can_fight_with - contains information about races we can fight with
        - allies - It's less probable to kill someone who is from allied race
        - enemies - It's more probable to kill someone who is from hostile race
    """
    name = models.CharField(max_length=25)
    can_fight_with = models.ManyToManyField("Race", blank=True, related_name='can_fight')
    allies = models.ManyToManyField("Race", blank=True, related_name='ally')
    enemies = models.ManyToManyField("Race", blank=True, related_name='enemy')

    def __str__(self):
        return self.name


class Guild(models.Model):
    """
    Fields:
        - name - contains name
        - allies - It's less probable to kill someone who is from allied race
        - enemies - It's more probable to kill someone who is from hostile race
    """
    name = models.CharField(max_length=25)
    allies = models.ManyToManyField("Guild", blank=True, related_name='ally')
    enemies = models.ManyToManyField("Guild", blank=True, related_name='enemy')

    def __str__(self):
        return self.name


class ExperienceTable(models.Model):
    """
    This table contains information about experience required to level up
    """
    level = models.IntegerField(primary_key=True)
    required_exp = models.IntegerField()


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
    def is_alive(self):
        return self.hit_points > 0

    @property
    def death_date(self):
        hero_died = self.looser.filter(looser_died=True)
        if hero_died:
            return hero_died[0].date
        else:
            return None

    @property
    def battles_lost(self):
        return self.looser.count()

    @property
    def battles_won(self):
        return self.winner.count()

    def __str__(self):
        return self.user.username
