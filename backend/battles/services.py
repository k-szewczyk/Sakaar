from datetime import datetime

import numpy as np
from battles.models import Battle, Round


class Fight:
    def __init__(self, attendees):
        self.attendees = attendees
        self.battle = Battle.objects.create(date=datetime.now())
        self.battle.attendees.set(self.attendees)
        self.attendees_hit_points = {attendee: attendee.hit_points for attendee in self.attendees}
        print(self.attendees_hit_points)

    def battle_loop(self):
        while any(hp > 0 for hp in self.attendees_hit_points.values()):
            self.create_round()
        self.battle.is_looser_dead = np.random.choice([True, False], p=self.death_probability())

    def death_probability(self):
        guilds = [attendee.guild for attendee in self.attendees]
        races = [attendee.race for attendee in self.attendees]
        if len(set(guilds)) == 1 or len(set(races)) == 1:
            return [0.05, 0.95]
        return [0.5, 0.5]

    def calculate_damage(self, attacker, defender):
        difference = attacker.atk_points - defender.def_points
        if difference > 0:
            return np.random.randint(difference, 21 + difference)
        elif difference < 0:
            return np.random.randint(0, 21 + difference)
        return np.random.randint(0, 21)

    def create_round(self):
        if np.random.randint(0, 1):
            attacker = self.attendees[0]
            defender = self.attendees[1]
        else:
            attacker = self.attendees[1]
            defender = self.attendees[0]

        hp_dealt = self.calculate_damage(attacker, defender)
        Round.objects.create(battle=self.battle,
                             attacker=attacker,
                             defender=defender,
                             hp_dealt=hp_dealt)

        self.attendees_hit_points[defender] -= hp_dealt
