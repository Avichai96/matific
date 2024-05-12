# models.py

import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Avg

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)
    is_player = models.BooleanField(default=False)
    login_count = models.IntegerField(default=0)
    total_login_time = models.DurationField(default=datetime.timedelta())
    last_login_end = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)

    class Meta:
        db_table = 'league_user'

class Team(models.Model):
    name = models.CharField(max_length=100)
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coached_teams')

    class Meta:
        db_table = 'league_team'

    @property
    def average_score(self):
        from django.db.models import Q

        home_avg = self.home_games.aggregate(avg_score=Avg('team_a_score'))['avg_score'] or 0
        away_avg = self.away_games.aggregate(avg_score=Avg('team_b_score'))['avg_score'] or 0
        total_games = self.home_games.count() + self.away_games.count()

        if total_games == 0:
            return 0
        else:
            total_avg_score = (home_avg * self.home_games.count() + away_avg * self.away_games.count()) / total_games
            return total_avg_score


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player')
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    height = models.FloatField()
    games_participated = models.IntegerField()

    class Meta:
        db_table = 'league_player'
        indexes = [
            models.Index(fields=['team', 'name'])
        ]

    @property
    def average_score(self):
        total_score = self.scores.aggregate(avg_score=Avg('score'))['avg_score']
        return total_score if total_score is not None else 0 


class Game(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=255)
    referee = models.CharField(max_length=100)
    team_a = models.ForeignKey(Team, related_name='home_games', on_delete=models.CASCADE)
    team_b = models.ForeignKey(Team, related_name='away_games', on_delete=models.CASCADE)
    team_a_score = models.IntegerField()
    team_b_score = models.IntegerField()


    class Meta:
        db_table = 'league_game'


class PlayerGameParticipation(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='game_participations')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='player_participations')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    points_scored = models.IntegerField(default=0)

    class Meta:
        db_table = 'player_game_participation'
        unique_together = ('player', 'game')

    def save(self, *args, **kwargs):
        if self.player.team != self.team:
            raise ValidationError("Player's team must match the participating team in the game.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player.name} in game {self.game.id}"


class Score(models.Model):
    player = models.ForeignKey(Player, related_name='scores', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name='scores', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'league_score'

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    champion = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='championships_won')

    class Meta:
        db_table = 'league_tournament'


class TournamentRound(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='rounds')
    round_number = models.IntegerField()
    teams = models.ManyToManyField(Team, through='RoundTeam')

    class Meta:
        db_table = 'league_tournament_round'

class RoundTeam(models.Model):
    round = models.ForeignKey(TournamentRound, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    eliminated = models.BooleanField(default=False)

    class Meta:
        db_table = 'league_round_team'
