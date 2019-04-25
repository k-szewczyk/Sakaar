from django.urls import reverse
from rest_framework import test, status

from halloffame.models import Hero
from . import factories


class HallOfFamePermissionsTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.race1 = factories.RaceFactory()
        cls.race2 = factories.RaceFactory()
        cls.guild1 = factories.GuildFactory()
        cls.guild2 = factories.GuildFactory()
        cls.hero_list_url = reverse('hero-list')

    def setUp(self):
        self.user1 = factories.UserFactory()
        self.user2 = factories.UserFactory()
        self.client.force_login(self.user1)

    def test_create_new_hero(self):
        response = self.client.post(self.hero_list_url,
                                    {'user': self.user1.id, 'race': self.race1.id, 'guild': self.guild1.id})

        self.assertEqual(Hero.objects.count(), 1)

    def test_user_can_not_create_second_hero(self):
        factories.HeroFactory(user=self.user1)
        response = self.client.post(self.hero_list_url,
                                    {'user': self.user1.id, 'race': self.race1.id, 'guild': self.guild1.id})

        self.assertEqual(Hero.objects.count(), 1)

    def test_create_new_hero_assigned_to_someone_else(self):
        response = self.client.post(self.hero_list_url,
                                    {'user': self.user2.id, 'race': self.race1.id, 'guild': self.guild1.id})

        self.assertEqual(Hero.objects.count(), 0)

    def test_delete_someone_elses_hero(self):
        factories.HeroFactory(user=self.user2)
        response = self.client.delete(self.hero_list_url + f'{self.user2.id}/')

        self.assertEqual(Hero.objects.count(), 1)

    def test_user_can_change_guild(self):
        factories.HeroFactory(user=self.user1)
        response = self.client.patch(self.hero_list_url + f'{self.user1.id}/', {'user': self.user1.id,
                                                                                'guild': self.guild2.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_change_someone_elses_guild(self):
        factories.HeroFactory(user=self.user2)
        response = self.client.patch(self.hero_list_url + f'{self.user2.id}/', {'user': self.user2.id,
                                                                                'guild': self.guild2.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
