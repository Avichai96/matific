from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Team, Player, Game, PlayerGameParticipation, Score

# User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_coach', 'is_player')
    list_filter = ('is_admin', 'is_coach', 'is_player')
    search_fields = ('username', 'email')
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'is_admin', 'is_coach', 'is_player')
#     list_filter = ('is_admin', 'is_coach', 'is_player')
#     search_fields = ('username', 'email')

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

class GameAdmin(admin.ModelAdmin):
    inlines = [PlayerGameParticipationInline, ScoreInline]

admin.site.unregister(Game)
admin.site.register(Game, GameAdmin)


# from django.contrib import admin
# from .models import User, Team, Player, Game


# class TeamAdmin(admin.ModelAdmin):
#     list_display = ('name', 'coach', 'average_score')

# class PlayerAdmin(admin.ModelAdmin):
#     list_display = ('name', 'team', 'height', 'average_score', 'games_participated')

# class GameAdmin(admin.ModelAdmin):
#     list_display = ('date', 'team_a', 'team_b', 'team_a_score', 'team_b_score')

# admin.site.register(User)
# admin.site.register(Team, TeamAdmin)
# admin.site.register(Player, PlayerAdmin)
# admin.site.register(Game, GameAdmin)

# from django.contrib import admin
# from .models import User, Team, Player

# class TeamAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_admin:
#             return qs
#         elif request.user.is_coach:
#             return qs.filter(coach=request.user)
#         return qs.none()

#     def has_change_permission(self, request, obj=None):
#         if not obj:
#             return True  # So they can see the change list page
#         return request.user.is_admin or (request.user.is_coach and obj.coach == request.user)

#     def has_delete_permission(self, request, obj=None):
#         return request.user.is_admin

# class PlayerAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_admin:
#             return qs
#         elif request.user.is_coach:
#             return qs.filter(team__coach=request.user)
#         return qs.none()

#     def has_module_permission(self, request):
#         return request.user.is_admin or request.user.is_coach

# admin.site.register(User)
# admin.site.register(Team, TeamAdmin)
# admin.site.register(Player, PlayerAdmin)
