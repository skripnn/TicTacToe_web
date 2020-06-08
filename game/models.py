from django.db import models


class Steps(models.Model):
    size = models.IntegerField()
    field = models.CharField(max_length=512)
    score = models.IntegerField()
    steps = models.IntegerField()
