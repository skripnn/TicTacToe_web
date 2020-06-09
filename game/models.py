from django.db import models


class Steps(models.Model):
    size = models.IntegerField()
    field = models.CharField(max_length=128)
    score = models.IntegerField()
    steps = models.IntegerField()


class Game(models.Model):
    size = models.IntegerField()
    field = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    player_x = models.CharField(max_length=64)
    player_o = models.CharField(max_length=64)

    # class Meta:
    #     db_table = 'game_game'
