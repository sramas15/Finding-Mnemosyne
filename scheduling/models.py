from django.contrib.auth.models import User
from django.db import models
from cards.models import Card

class RepIntervalLog(models.Model):
    user = models.ForeignKey(User)
    card = models.ForeignKey(Card)
    grade = models.SmallIntegerField()
    new_grade = models.SmallIntegerField()
    easiness = models.FloatField()
    ret_reps = models.IntegerField()
    ret_reps_since_lapse = models.IntegerField()
    lapses = models.IntegerField()
    interval = models.IntegerField()

class RegressionWeights(models.Model):
    user = models.ForeignKey(User)
    grade = models.FloatField()
    new_grade = models.FloatField()
    easiness = models.FloatField()
    ret_reps = models.FloatField()
    ret_reps_since_lapse = models.FloatField()
    lapses = models.FloatField()
    interval = models.FloatField()

