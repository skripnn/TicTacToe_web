# Generated by Django 3.0.7 on 2020-06-10 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_remove_steps_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='player_o',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='game',
            name='player_x',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='game',
            name='state',
            field=models.CharField(max_length=24),
        ),
    ]