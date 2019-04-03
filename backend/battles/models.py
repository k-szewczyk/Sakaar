from django.db import models


class Battle(models.Model):
    attendees = models.ManyToManyField('halloffame.Hero', related_name='battles')
    looser = models.ForeignKey('halloffame.Hero', blank=True, null=True, default=None, related_name='loosed_battles',
                               on_delete=models.SET_NULL)
    is_looser_dead = models.BooleanField(default=False)
    date = models.DateTimeField()


class BattleLog(models.Model):
    battle = models.ForeignKey(Battle, related_name='battle_log', on_delete=models.CASCADE)
    attacker = models.ForeignKey('halloffame.Hero', related_name='battle_log_attacker', null=True,
                                 on_delete=models.SET_NULL)
    defender = models.ForeignKey('halloffame.Hero', related_name='battle_log_defender', null=True,
                                 on_delete=models.SET_NULL)
    hp_dealt = models.PositiveSmallIntegerField()
