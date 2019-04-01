from django.db import models
from django.contrib.auth.models import User
import json


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


class Fraction(models.Model):
    name = models.CharField(max_length=25)

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


class ItemType(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=25)
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    min_level = models.IntegerField()
    bonus_atk = models.IntegerField()
    bonus_def = models.IntegerField()

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
    fraction = models.ForeignKey(Fraction, default=0, on_delete=models.SET_DEFAULT)
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


class Equipment(models.Model):
    hero = models.OneToOneField(Hero, on_delete=models.CASCADE)
    helmet = models.ForeignKey(Item, null=True, blank=True, related_name='helmet', on_delete=models.SET_NULL)
    armor = models.ForeignKey(Item, null=True, blank=True, related_name='armor', on_delete=models.SET_NULL)
    weapon = models.ForeignKey(Item, null=True, blank=True, related_name='weapon', on_delete=models.SET_NULL)


class Inventory(models.Model):
    """
        Fields:
            - hero - One to one relationship with hero
            - items - JSON which contains inventory field number as key and Item_id as value
    """
    hero = models.OneToOneField(Hero, on_delete=models.CASCADE)
    items = models.TextField()

    @property
    def item_count(self):
        return len(json.loads(self.items))


class Battle(models.Model):
    winner = models.ForeignKey(Hero, related_name='winner', null=True, on_delete=models.SET_NULL)
    looser = models.ForeignKey(Hero, related_name='looser', null=True, on_delete=models.SET_NULL)
    looser_died = models.BooleanField()
    date = models.DateTimeField()
