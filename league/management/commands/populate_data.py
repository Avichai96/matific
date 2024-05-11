# populate_data.py

from datetime import timedelta, date
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from league.models import Team, Player, Game, Score, PlayerGameParticipation
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with fake users, teams, players, games, and scores'

    def handle(self, *args, **options):
        self.stdout.write("Starting to populate the database...")

        # Clear existing data
        User.objects.filter(is_superuser=False).delete()
        Team.objects.all().delete()
        Player.objects.all().delete()
        Game.objects.all().delete()
        Score.objects.all().delete()

        # Create users and teams
        manager = User.objects.create_user(username='manager', email='manager@example.com', password='pass1234', is_staff=True, is_admin=True)
        coaches = [User.objects.create_user(username=f'coach{i+1}', email=f'coach{i+1}@example.com', password='pass1234', is_coach=True) for i in range(16)]
        teams = [Team.objects.create(name=f"Team {i+1}", coach=coaches[i]) for i in range(16)]
        
        # Create players
        players = []
        for team in teams:
            for j in range(10):  # Ensuring not to exceed 10 players per team
                player_user = User.objects.create_user(username=f'player_{team.name}_{j+1}', email=f'player_{team.name}_{j+1}@example.com', password='pass1234', is_player=True)
                players.append(Player.objects.create(user=player_user, team=team, name=f'Player {j+1} of {team.name}', height=random.uniform(1.75, 2.10), games_participated=0))
        
        # Create games
        start_date = date.today()
        games = []
        for i in range(0, len(teams), 2):
            game_date = start_date + timedelta(days=i)
            for j in range(1, len(teams), 2):
                if i != j:
                    game = Game.objects.create(
                        date=game_date,
                        location='Stadium A',
                        referee=f'Referee {i+j}',
                        team_a=teams[i],
                        team_b=teams[j],
                        team_a_score=random.randint(50, 120),
                        team_b_score=random.randint(50, 120),
                    )
                    games.append(game)
        
        # Create scores and player game participations
        for game in games:
            participants = list(game.team_a.players.all()) + list(game.team_b.players.all())
            for player in participants:
                points_scored = random.randint(10, 30)
                Score.objects.create(player=player, game=game, score=points_scored)
                PlayerGameParticipation.objects.create(player=player, game=game, team=player.team, points_scored=points_scored)
                player.games_participated += 1
                player.save()

        self.stdout.write(self.style.SUCCESS('Database has been populated with fake data.'))

