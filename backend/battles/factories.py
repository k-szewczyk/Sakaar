import factory
from django.contrib.auth.models import User

from battles import models


class BattleFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Battle

    @factory.post_generation
    def attendees(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for attendee in extracted:
                self.attendees.add(attendee)
