# admin_site.py

from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = 'Basketball League Management'

    def has_permission(self, request):
        return request.user.is_active and (request.user.is_manager or request.user.is_coach)

my_admin_site = MyAdminSite(name='myadmin')

my_admin_site.register(User)
my_admin_site.register(Team, TeamAdmin)
my_admin_site.register(Player, PlayerAdmin)
