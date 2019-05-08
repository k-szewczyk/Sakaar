import typing
from datetime import datetime
from django.utils import timezone
import numpy as np

from battles.models import Battle, Round


class Fight:
    def __init__(self, attendees: typing.List):
        self.attendees = attendees
        self.battle = Battle.objects.create(date=timezone.now())
        self.battle.attendees.set(self.attendees)
        self.attendees_hit_points = {attendee: attendee.hit_points for attendee in self.attendees}
        if self.attendees[0].race == self.attendees[1].race or self.attendees[0].guild == self.attendees[1].guild:
            self.death_probability = 0.05
        else:
            self.death_probability = 0.5

    def battle_loop(self):
        while all(hp > 0 for hp in self.attendees_hit_points.values()):
            self.create_round()

        self.battle.looser = [attendee for attendee in self.attendees_hit_points
                              if self.attendees_hit_points[attendee] <= 0][0]

        self.battle.is_looser_dead = np.random.choice([True, False],
                                                      p=[self.death_probability, 1-self.death_probability])
        self.battle.save()

    def calculate_damage(self, attacker, defender):
        difference = attacker.atk_points - defender.def_points
        if difference > 0:
            return np.random.randint(difference, 21 + difference)
        else:
            return np.random.randint(0, 21 + difference)

    def create_round(self):
        attacker, defender = self.attendees[::np.random.choice([1, -1])]
        hp_dealt = self.calculate_damage(attacker, defender)
        Round.objects.create(battle=self.battle,
                             attacker=attacker,
                             defender=defender,
                             hp_dealt=hp_dealt)

        self.attendees_hit_points[defender] -= hp_dealt
