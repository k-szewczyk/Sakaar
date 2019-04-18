from django.db import models
from random import randint, choice

class Battle(models.Model):
    attendees = models.ManyToManyField('halloffame.Hero', related_name='battles')
    looser = models.ForeignKey('halloffame.Hero', blank=True, null=True, default=None, related_name='lost_battles',
                               on_delete=models.SET_NULL)
    is_looser_dead = models.BooleanField(default=False)
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.attendees.all().first()} vs {self.attendees.all().last()}'

    def chose_attacker(self):
        pass


class Round(models.Model):
    battle = models.ForeignKey(Battle, related_name='round', on_delete=models.CASCADE)
    attacker = models.ForeignKey('halloffame.Hero', related_name='round_attacker', null=True,
                                 on_delete=models.SET_NULL)
    defender = models.ForeignKey('halloffame.Hero', related_name='round_defender', null=True,
                                 on_delete=models.SET_NULL)
    hp_dealt = models.PositiveSmallIntegerField()

    def calculate_damage(self):
        difference = self.attacker.atk_points - self.defender.def_points
        if difference > 0:
            self.hp_dealt = randint(difference, 21 + difference)
        elif difference < 0:
            self.hp_dealt = randint(0, 21 + difference)
        else:
            self.hp_dealt = randint(0, 21)

