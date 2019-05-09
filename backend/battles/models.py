from django.db import models


class Battle(models.Model):
    attendees = models.ManyToManyField('halloffame.Hero', related_name='battles')
    looser = models.ForeignKey('halloffame.Hero', blank=True, null=True, default=None, related_name='lost_battles',
                               on_delete=models.SET_NULL)
    is_looser_dead = models.BooleanField(default=False)
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.attendees.first()} vs {self.attendees.last()}'


class Round(models.Model):
    battle = models.ForeignKey(Battle, related_name='rounds', on_delete=models.CASCADE)
    attacker = models.ForeignKey('halloffame.Hero', related_name='round_attackers', null=True,
                                 on_delete=models.SET_NULL)
    defender = models.ForeignKey('halloffame.Hero', related_name='round_defenders', null=True,
                                 on_delete=models.SET_NULL)
    hp_dealt = models.PositiveSmallIntegerField(default=0)
