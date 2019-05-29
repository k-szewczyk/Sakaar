from django.utils import timezone
from rest_framework import test, status
from rest_framework.reverse import reverse

from battles.models import Battle
from halloffame.factories import HeroFactory, UserFactory, RaceFactory, GuildFactory
from halloffame.models import Hero


class HallOfFamePermissionsTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.race1 = RaceFactory()
        cls.race2 = RaceFactory()
        cls.guild1 = GuildFactory()
        cls.guild2 = GuildFactory()
        cls.hero_list_url = reverse('hero-list')

    def setUp(self):
        self.user1 = UserFactory()
        self.user1_url = reverse("hero-detail", args=(self.user1.id,))
        self.user2 = UserFactory()
        self.user2_url = reverse("hero-detail", args=(self.user2.id,))
        self.client.force_login(self.user1)

    def test_create_new_hero(self):
        response = self.client.post(self.hero_list_url,
                         {'user': self.user1.id, 'race': self.race1.id, 'guild': self.guild1.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hero.objects.count(), 1)

    def test_user_can_not_create_second_hero(self):
        HeroFactory(user=self.user1)
        response = self.client.post(self.hero_list_url,
                         {'user': self.user1.id, 'race': self.race1.id, 'guild': self.guild1.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Hero.objects.count(), 1)

    def test_create_new_hero_assigned_to_someone_else(self):
        response = self.client.post(self.hero_list_url,
                         {'user': self.user2.id, 'race': self.race1.id, 'guild': self.guild1.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Hero.objects.count(), 0)

    def test_delete_someone_elses_hero(self):
        HeroFactory(user=self.user2)
        response = self.client.delete(self.user2_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Hero.objects.count(), 1)

    def test_user_can_change_guild(self):
        HeroFactory(user=self.user1)
        response = self.client.patch(self.user1_url, {'user': self.user1.id, 'guild': self.guild2.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_change_someone_elses_guild(self):
        HeroFactory(user=self.user2)
        response = self.client.patch(self.user2_url, {'user': self.user2.id, 'guild': self.guild2.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class HallOfFameFilteringTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hero_list_url = reverse('hero-list')
        cls.hero1 = HeroFactory()
        cls.hero2 = HeroFactory()
        cls.hero3 = HeroFactory()

        cls.battle1 = Battle.objects.create(date=timezone.now())
        cls.battle1.attendees.set([cls.hero1, cls.hero2])
        cls.battle1.looser = cls.hero1
        cls.battle1.save()

        cls.battle2 = Battle.objects.create(date=timezone.now())
        cls.battle2.attendees.set([cls.hero1, cls.hero3])
        cls.battle2.looser = cls.hero1
        cls.battle2.save()

        cls.battle3 = Battle.objects.create(date=timezone.now(), is_looser_dead=True)
        cls.battle3.attendees.set([cls.hero2, cls.hero3])
        cls.battle3.looser = cls.hero3
        cls.battle3.save()

    def test_alive_heroes_filtering(self):
        response = self.client.get(self.hero_list_url, kwargs={'is_alive': True})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_dead_heroes_filtering(self):
        response = self.client.get(self.hero_list_url, kwargs={'is_alive': False})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_available_opponents_for_specified_hero_filtering(self):
        self.hero1.race.can_fight_with.set([self.hero1.race, self.hero2.race, self.hero3.race])
        self.hero1.race.save()
        hero4 = HeroFactory(race=self.hero1.race)
        new_battle = Battle.objects.create(date=timezone.now())
        new_battle.attendees.set([hero4, self.hero3])
        new_battle.save()

        response = self.client.get(self.hero_list_url, kwargs={'find_opponents_for': hero4.user_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
