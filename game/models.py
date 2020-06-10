from django.db import models


class Steps(models.Model):
    size = models.IntegerField()
    field = models.CharField(max_length=128)
    steps = models.CharField(max_length=128)


class Game(models.Model):
    size = models.IntegerField()
    field = models.CharField(max_length=128)
    state = models.CharField(max_length=24)
    player_x = models.CharField(max_length=6)
    player_o = models.CharField(max_length=6)
    player = models.CharField(max_length=1)
    counts = models.IntegerField()
    red_line = models.CharField(max_length=48, default='')
