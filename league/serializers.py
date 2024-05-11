# serializers.py

from rest_framework import serializers
from .models import User, Team, Player, Game, Score
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
