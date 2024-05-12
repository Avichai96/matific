# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, PlayerViewSet, GameViewSet, GameDetailsViewSet, UserStatisticsViewSet, TournamentViewSet, TournamentRoundViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'games', GameViewSet)
router.register(r'tournaments', TournamentViewSet)
router.register(r'tournament_rounds', TournamentRoundViewSet)
router.register(r'game-details', GameDetailsViewSet, basename='game-details')
router.register(r'user-stats', UserStatisticsViewSet, basename='user-stats')

# from pprint import pprint
# pprint(router.urls)

urlpatterns = [
    path('', include(router.urls)),
]
