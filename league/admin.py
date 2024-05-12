from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Team, Player, Game, PlayerGameParticipation, Score, Tournament, TournamentRound, RoundTeam

# User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_coach', 'is_player')
    list_filter = ('is_admin', 'is_coach', 'is_player')
    search_fields = ('username', 'email')

# Team Admin
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach', 'average_score')
    search_fields = ('name',)
    list_select_related = ('coach',)

# Player Admin
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'name', 'height', 'average_score')
    list_filter = ('team',)
    search_fields = ('name', 'user__username')
    list_select_related = ('team',)  # Optimizes query to fetch related team objects

# Game Admin
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('date', 'location', 'referee', 'team_a', 'team_b', 'team_a_score', 'team_b_score')
    list_filter = ('date', 'location')
    search_fields = ('team_a__name', 'team_b__name')

# PlayerGameParticipation Admin
@admin.register(PlayerGameParticipation)
class PlayerGameParticipationAdmin(admin.ModelAdmin):
    list_display = ('player', 'game', 'team', 'points_scored')
    list_filter = ('game', 'team')
    search_fields = ('player__name', 'team__name')

# Score Admin
@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('player', 'game', 'score')
    list_filter = ('game', 'player')
    search_fields = ('player__name', 'game__date')

class ScoreInline(admin.TabularInline):
    model = Score
    extra = 1

class PlayerGameParticipationInline(admin.TabularInline):
    model = PlayerGameParticipation
    extra = 1

# class GameAdmin(admin.ModelAdmin):
#     inlines = [PlayerGameParticipationInline, ScoreInline]

class GameAdmin(admin.ModelAdmin):
    list_display = ('date', 'location', 'referee', 'team_a', 'team_b', 'team_a_score', 'team_b_score')
    list_filter = ('date', 'location')
    search_fields = ('team_a__name', 'team_b__name')
    inlines = [PlayerGameParticipationInline, ScoreInline]

admin.site.unregister(Game)
admin.site.register(Game, GameAdmin)

class TournamentRoundInline(admin.TabularInline):
    model = TournamentRound
    extra = 1 

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'champion')
    list_filter = ('start_date', 'end_date', 'champion')
    search_fields = ('name',)
    inlines = [TournamentRoundInline]

class RoundTeamInline(admin.TabularInline):
    model = RoundTeam
    extra = 0 

@admin.register(TournamentRound)
class TournamentRoundAdmin(admin.ModelAdmin):
    list_display = ('id', 'tournament', 'round_number')
    list_filter = ('tournament', 'round_number')
    inlines = [RoundTeamInline]

@admin.register(RoundTeam)
class RoundTeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'round', 'team', 'eliminated')
    list_filter = ('round', 'eliminated')
    search_fields = ('round__tournament__name', 'team__name')