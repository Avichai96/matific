# Generated by Django 5.0.6 on 2024-05-09 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0001_initial'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='player',
            new_name='league_play_team_id_eae027_idx',
            old_name='legue_playe_team_id_13f5ff_idx',
        ),
        migrations.AlterModelTable(
            name='game',
            table='league_game',
        ),
        migrations.AlterModelTable(
            name='player',
            table='league_player',
        ),
        migrations.AlterModelTable(
            name='score',
            table='league_score',
        ),
        migrations.AlterModelTable(
            name='team',
            table='league_team',
        ),
        migrations.AlterModelTable(
            name='user',
            table='league_user',
        ),
    ]
