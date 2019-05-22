from django.urls import include, path
from rest_framework_nested import routers
from rest_framework_swagger.views import get_swagger_view

from battles import views

schema_view = get_swagger_view(title='Sakaar')

router = routers.SimpleRouter()
router.register('battles', views.BattleViewSet)

battles_router = routers.NestedSimpleRouter(router, 'battles', lookup='battle')
battles_router.register('rounds', views.RoundViewSet)

urlpatterns = [
    path('', schema_view),
    path('', include(router.urls)),
    path('', include(battles_router.urls)),
]
