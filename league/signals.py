# signals.py

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
import datetime
from .models import User

@receiver(user_logged_in)
def user_logged_in_receiver(sender, request, user: User, **kwargs):
    user.is_online = True
    user.login_count += 1
    user.save(update_fields=['is_online', 'login_count'])

@receiver(user_logged_out)
def user_logged_out_receiver(sender, request, user: User, **kwargs):
    if user.last_login and user.last_login_end:
        duration = datetime.datetime.now(datetime.timezone.utc) - user.last_login_end
        user.total_login_time += duration
    user.last_login_end = datetime.datetime.now(datetime.timezone.utc)
    user.is_online = False
    user.save(update_fields=['last_login_end', 'total_login_time', 'is_online'])
