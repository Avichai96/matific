from datetime import timedelta, date
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from league.models import Team, Player, Game, Score, Tournament, TournamentRound, RoundTeam
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with fake users, teams, players, games, scores, and tournaments'

    def handle(self, *args, **options):
        self.stdout.write("Starting to populate the database...")

        # Clear existing data
        User.objects.filter(is_superuser=False).delete()
        Team.objects.all().delete()
        Player.objects.all().delete()
        Game.objects.all().delete()
        Score.objects.all().delete()
        Tournament.objects.all().delete()
        TournamentRound.objects.all().delete()
        RoundTeam.objects.all().delete()

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
        
        # Create tournaments
        for tournament_index in range(4):  # Creating 4 tournaments
            tournament = Tournament.objects.create(name=f"Tournament {tournament_index + 1}", start_date=date.today(), end_date=date.today() + timedelta(days=30))
            current_teams = teams[:]
            random.shuffle(current_teams)  # Shuffle teams for varied matchups

            # Create rounds
            for round_number in range(1, 6):  # There should be 5 rounds to end with a single champion
                round = TournamentRound.objects.create(tournament=tournament, round_number=round_number)
                next_round_teams = []

                # Create matches for each round
                match_count = len(current_teams) // 2
                for i in range(match_count):
                    team_a = current_teams[2 * i]
                    team_b = current_teams[2 * i + 1]
                    winner = random.choice([team_a, team_b])
                    next_round_teams.append(winner)
                    RoundTeam.objects.create(round=round, team=team_a, eliminated=(winner != team_a))
                    RoundTeam.objects.create(round=round, team=team_b, eliminated=(winner != team_b))

                current_teams = next_round_teams
                if len(current_teams) == 1:  # Final champion determined
                    tournament.champion = current_teams[0]
                    tournament.save()
                    break

        self.stdout.write(self.style.SUCCESS('Database has been populated with fake data.'))