from django.test import TestCase
from halloffame.factories import HeroFactory
from halloffame.models import Hero
from battles.services import Fight


class BattleSystemTest(TestCase):
    def setUp(self):
        self.hero1 = HeroFactory()
        self.hero2 = HeroFactory()

    def test_battle_creates_associated_rounds(self):
        fight = Fight([self.hero1, self.hero2])
        fight.battle_loop()

        self.assertGreater(fight.battle.rounds.count(), 0)

    def test_battle_ends_when_hp_is_lt_zero(self):
        fight = Fight([self.hero1, self.hero2])
        fight.battle_loop()

        self.assertLessEqual(0, fight.battle.rounds.last().hp_dealt)

    def test_one_hero_loses_battle(self):
        fight = Fight([self.hero1, self.hero2])
        fight.battle_loop()

        queryset = Hero.objects.get_annotations()

        won_counter = queryset.first().battles_won + queryset.last().battles_won
        lost_counter = queryset.first().battles_lost + queryset.last().battles_lost

        self.assertEqual(True, (won_counter == 1) & (lost_counter == 1))
