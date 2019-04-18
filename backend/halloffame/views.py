from rest_framework.viewsets import ModelViewSet

from .filters import HeroFilterSet
from .models import Hero
from .serializers import HeroSerializer
from django.http import HttpResponse


class HeroViewSet(ModelViewSet):
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
    filter_class = HeroFilterSet

    def get_queryset(self):
        return Hero.objects.get_annotations()

    def destroy(self, request, *args, **kwargs):
        if int(kwargs['pk']) == self.request.user.id:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)
