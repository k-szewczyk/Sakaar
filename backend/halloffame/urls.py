from django.urls import include, path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from . import views

schema_view = get_swagger_view(title='Sakaar')

router = routers.DefaultRouter()
router.register('heroes', views.HeroViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', schema_view),
    path('', include(router.urls)),
]
