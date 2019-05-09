from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import test, status
from rest_framework.reverse import reverse
from django.test import TestCase

from battles.models import Battle
from battles.services import Fight
from halloffame import factories
from halloffame.factories import HeroFactory
from halloffame.models import Hero


class HallOfFamePermissionsTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.grand_master = User.objects.create(username='admin', password='admin', is_staff=True)
        cls.battle_list_url = reverse('battle-list')

    def setUp(self):
        self.hero1 = factories.HeroFactory()
        self.hero1_url = reverse("hero-detail", args=(self.hero1.user_id,))
        self.hero2 = factories.HeroFactory()
        self.hero2_url = reverse("hero-detail", args=(self.hero2.user_id,))
        self.hero1.race.can_fight_with.set([self.hero2.race])
        self.hero2.race.can_fight_with.set([self.hero1.race])
        self.hero1.save()
        self.hero2.save()
        self.client.force_login(self.grand_master)

    def test_gm_can_create_battle(self):
        self.client.post(self.battle_list_url, {'attendees': [self.hero1.user_id, self.hero2.user_id]})
        self.assertEqual(Battle.objects.count(), 1)

    def test_heroes_can_fight_once_with_the_same_opponent(self):
        self.client.post(self.battle_list_url, {'attendees': [self.hero1.user_id, self.hero2.user_id]})
        response = self.client.post(self.battle_list_url, {'attendees': [self.hero1.user_id, self.hero2.user_id]})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Battle.objects.count(), 1)

    def test_user_can_not_create_battle(self):
        self.client.force_login(self.hero1.user)
        response = self.client.post(self.battle_list_url, {'attendees': [self.hero1.user_id, self.hero2.user_id]})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Battle.objects.count(), 0)

    def test_user_can_not_fight_with_dead_hero(self):
        dead_hero = factories.HeroFactory()
        dead_hero.race = self.hero1.race
        dead_hero.save()

        battle = Battle.objects.create(looser=dead_hero, is_looser_dead=True, date=timezone.now())
        battle.attendees.set([dead_hero, self.hero1])
        battle.save()
        response = self.client.post(self.battle_list_url, {'attendees': [dead_hero.user_id, self.hero2.user_id]})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Battle.objects.count(), 1)

    def test_can_fight_with_different_races(self):
        hero3 = factories.HeroFactory()

        response = self.client.post(self.battle_list_url, {'attendees': [hero3.user_id, self.hero2.user_id]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Battle.objects.count(), 0)


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
