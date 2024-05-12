# serializers.py

from rest_framework import serializers
from .models import User, Team, Player, Game, Score, Tournament, TournamentRound, RoundTeam
# from djoser.serializers import UserSerializer as BaseUserSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin', 'is_coach', 'is_player']

class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    average_score = serializers.ReadOnlyField()

    class Meta:
        model = Player
        fields = ['id', 'user', 'team', 'name', 'height', 'games_participated', 'average_score']

class TeamSerializer(serializers.ModelSerializer):
    coach = UserSerializer(read_only=True)
    players = PlayerSerializer(many=True, read_only=True)
    average_score = serializers.ReadOnlyField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'coach', 'players', 'average_score']

class GameSerializer(serializers.ModelSerializer):
    team_a = TeamSerializer(read_only=True)
    team_b = TeamSerializer(read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'date', 'location', 'referee', 'team_a', 'team_b', 'team_a_score', 'team_b_score']

class ScoreSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    game = GameSerializer(read_only=True)

    class Meta:
        model = Score
        fields = ['id', 'player', 'game', 'score']

class SimplePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name']

class SimpleTeamSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source='coach.username')
    players = SimplePlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['name', 'coach_name', 'players']

class GameDetailsSerializer(serializers.ModelSerializer):
    team_a = SimpleTeamSerializer(read_only=True)
    team_b = SimpleTeamSerializer(read_only=True)
    winner = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ['date', 'location', 'team_a', 'team_b', 'team_a_score', 'team_b_score', 'winner']

    def get_winner(self, obj):
        if obj.team_a_score > obj.team_b_score:
            return obj.team_a.name
        elif obj.team_b_score > obj.team_a_score:
            return obj.team_b.name
        return "Draw"
    

class RoundTeamSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = RoundTeam
        fields = ['team', 'eliminated']

class TournamentRoundSerializer(serializers.ModelSerializer):
    teams = RoundTeamSerializer(source='roundteam_set', many=True)

    class Meta:
        model = TournamentRound
        fields = ['round_number', 'teams']

class TournamentSerializer(serializers.ModelSerializer):
    rounds = TournamentRoundSerializer(many=True)
    champion = TeamSerializer(read_only=True)

    class Meta:
        model = Tournament
        fields = ['id', 'name', 'start_date', 'end_date', 'champion', 'rounds']
    
class UserStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]

