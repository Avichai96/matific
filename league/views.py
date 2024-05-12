# views.py

from django.db.models import Avg, Window, F, Prefetch
from django.db.models.functions import PercentRank
from .models import User, Team, Player, Game, Tournament, TournamentRound, RoundTeam
from .serializers import TeamSerializer, PlayerSerializer, GameSerializer, \
        GameDetailsSerializer, UserStatisticsSerializer, TournamentSerializer, \
        TournamentRoundSerializer
from .permissions import IsAdminOrReadOnly, IsAdminStaff, IsAdminOrCoach, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAdminStaff]
    
    @action(detail=False, methods=['get'], url_path='my-team-details', permission_classes=[IsAdminOrCoach])
    def all_team_details(self, request):
        """
        Custom endpoint for managers to view all teams with player details and average scores.
        For coaches, it shows only the teams they coach.
        """
        if request.user.is_admin:
            teams = self.get_queryset()  # Admins can see all teams
        else:
            teams = request.user.coached_teams.all()  # Coaches can see only their teams

        serializer = self.get_serializer(teams, many=True)
        return Response(serializer.data)


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAdminStaff]

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
    
    @action(detail=False, methods=['get'], url_path='high-scorers', permission_classes=[IsAdminOrCoach])
    def get_high_scorers(self, request):
        """
        Endpoint for a coach to view players whose average scores are in the 90th percentile or higher within their teams.
        """

        # Assuming a coach might have multiple teams, this endpoint now fetches high scorers for all their teams.
        coached_teams = request.user.coached_teams.all()
        if not coached_teams:
            return Response({'error': 'No teams found for this coach'}, status=status.HTTP_404_NOT_FOUND)

        high_scorers_list = []
        for team in coached_teams:
            players = Player.objects.filter(team=team).annotate(
                avg_score=Avg('scores__score'),
                percentile=Window(
                    expression=PercentRank(),
                    order_by=F('avg_score').desc()
                )
            )
            high_scorers = players.filter(percentile__lt=0.1)  # get top 10%
            high_scorers_data = PlayerSerializer(high_scorers, many=True).data
            high_scorers_list.append({
                'team_id': team.id,
                'team_name': team.name,
                'high_scorers': high_scorers_data
            })

        return Response(high_scorers_list)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAdminOrCoach]


class GameDetailsViewSet(ReadOnlyModelViewSet):
    queryset = Game.objects.all().select_related('team_a', 'team_b').prefetch_related('team_a__players', 'team_b__players')
    serializer_class = GameDetailsSerializer
    permission_classes = [IsAdminOrReadOnly]


class TournamentRoundViewSet(viewsets.ModelViewSet):
    queryset = TournamentRound.objects.all().prefetch_related('roundteam_set__team')
    serializer_class = TournamentRoundSerializer
    permission_classes = [IsAdminOrReadOnly]


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all().prefetch_related(
        Prefetch('rounds', queryset=TournamentRound.objects.order_by('round_number')),
        'rounds__roundteam_set__team'
    )
    serializer_class = TournamentSerializer
    permission_classes = [IsAdminStaff]

    @action(detail=False, methods=['get'], url_path='list-ids')
    def list_tournament_ids(self, request):
        tournament_ids = list(Tournament.objects.values_list('id', flat=True))
        return Response(tournament_ids)
    
    @action(detail=True, methods=['get'], url_path='tournament-structure', permission_classes=[IsAuthenticated])
    def tournament_structure(self, request, pk=None):
        """
        Custom endpoint to view the structure of a tournament including rounds, teams, and players without details.
        """
        tournament = self.get_object()
        rounds = tournament.rounds.all()
        serializer = TournamentRoundSerializer(rounds, many=True)
        return Response(serializer.data)



class UserStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserStatisticsSerializer
    permission_classes = [IsAdminStaff]

    def get_queryset(self):
        return User.objects.all()