# views.py

from .models import Team, Player, Game
from .serializers import TeamSerializer, PlayerSerializer, GameSerializer
from .permissions import IsAdminOrReadOnly, IsAdminStaff, IsAdminOrCoach, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAdminOrCoach]
    
    @action(detail=False, methods=['get'], url_path='all-team-details', permission_classes=[IsAdminStaff])
    def all_team_details(self, request):
        """
        Custom endpoint for managers to view all teams with player details and average scores.
        """
        teams = self.get_queryset()
        serializer = self.get_serializer(teams, many=True)
        return Response(serializer.data)


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=['get'], url_path='my-info', permission_classes=[IsAuthenticated])
    def get_my_info(self, request):
        """
        Endpoint for a player to view their own details.
        """
        player = self.queryset.filter(user=request.user).first()
        if not player:
            return Response({'error': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(player)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='my-players')
    def get_coach_players(self, request):
        teams = request.user.coached_teams.all()
        if not teams.exists():
            return Response({'error': 'No teams found for this coach'}, status=status.HTTP_404_NOT_FOUND)
        players = Player.objects.filter(team__in=teams).select_related('user')
        serializer = self.get_serializer(players, many=True)
        return Response(serializer.data)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAdminOrReadOnly]
