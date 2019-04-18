from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import test, status

from . import factories


class HallOfFamePermissionsTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hero_list_url = reverse('hero-list')

        cls.Race1 = factories.RaceFactory()
        cls.Race2 = factories.RaceFactory()
        cls.Guild1 = factories.GuildFactory()
        cls.Guild2 = factories.GuildFactory()

        cls.user1 = User.objects.create_user(
            username='username1',
            password='passwd')

        cls.user2 = User.objects.create_user(
            username='username2',
            password='passwd')

    def setUp(self):
        self.client.force_login(self.user1)

    def test_create_new_hero(self):
        response = self.client.post(self.hero_list_url,
                                    {'id': self.user1.id, 'race': self.Race1.id, 'guild': self.Guild1.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_second_hero(self):
        self.client.post(self.hero_list_url, {'id': self.user1.id, 'race': self.Race2.id, 'guild': self.Guild2.id})
        response = self.client.post(self.hero_list_url,
                                    {'id': self.user1.id, 'race': self.Race1.id, 'guild': self.Guild1.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_new_hero_assigned_to_someone_else(self):
        response = self.client.post(self.hero_list_url,
                                    {'id': self.user2.id, 'race': self.Race1.id, 'guild': self.Guild1.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_hero(self):
        response = self.client.delete(self.hero_list_url + f'{self.user1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_someone_elses_hero(self):
        self.client.force_login(self.user2)
        self.client.post(self.hero_list_url, {'id': self.user2.id, 'race': self.Race1.id, 'guild': self.Guild1.id})
        self.client.logout()
        self.client.force_login(self.user1)

        response = self.client.delete(self.hero_list_url + f'{self.user2.id}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_change_guild(self):
        self.client.post(self.hero_list_url, {'id': self.user1.id, 'race': self.Race1.id, 'guild': self.Guild1.id})
        response = self.client.patch(self.hero_list_url + f'{self.user1.id}/', {'id': self.user1.id,
                                                                                'guild': self.Guild2.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_change_someone_elses_guild(self):
        self.client.force_login(self.user2)
        self.client.post(self.hero_list_url, {'id': self.user2.id, 'race': self.Race1.id, 'guild': self.Guild1.id})
        self.client.logout()
        self.client.force_login(self.user1)

        response = self.client.patch(self.hero_list_url + f'{self.user2.id}/', {'id': self.user2.id,
                                                                                'guild': self.Guild2.id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
