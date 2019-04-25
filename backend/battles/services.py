import typing
from datetime import datetime

import numpy as np

from battles.models import Battle, Round


class Fight:
    def __init__(self, attendees: typing.List):
        self.attendees = attendees
        self.battle = Battle.objects.create(date=datetime.now())
        self.battle.attendees.set(self.attendees)
        self.attendees_hit_points = {attendee: attendee.hit_points for attendee in self.attendees}

    def battle_loop(self):
        while all(hp > 0 for hp in self.attendees_hit_points.values()):
            self.create_round()

        self.battle.looser = [attendee for attendee in self.attendees_hit_points
                              if self.attendees_hit_points[attendee] <= 0][0]

        death_probability = self.get_death_probability()
        self.battle.is_looser_dead = np.random.choice([True, False], p=[death_probability, 1-death_probability])
        self.battle.save()

    def get_death_probability(self):
        if self.attendees[0].race == self.attendees[1].race or self.attendees[0].guild == self.attendees[1].guild:
            return 0.05
        return 0.5

    def calculate_damage(self, attacker, defender):
        difference = attacker.atk_points - defender.def_points
        if difference > 0:
            return np.random.randint(difference, 21 + difference)
        elif difference < 0:
            return np.random.randint(0, 21 + difference)
        return np.random.randint(0, 21)

    def create_round(self):
        attacker, defender = self.attendees[::np.random.choice([1, -1])]
        hp_dealt = self.calculate_damage(attacker, defender)
        Round.objects.create(battle=self.battle,
                             attacker=attacker,
                             defender=defender,
                             hp_dealt=hp_dealt)

        self.attendees_hit_points[defender] -= hp_dealt
