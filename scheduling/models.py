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
    interval_bucket = models.SmallIntegerField()

class RegressionWeights(models.Model):
    user = models.ForeignKey(User)
    grade = models.FloatField()
    new_grade = models.FloatField()
    easiness = models.FloatField()
    ret_reps = models.FloatField()
    ret_reps_since_lapse = models.FloatField()
    lapses = models.FloatField()
    intercept = models.FloatField()

INTERVAL_BUCKETS = [
        60*60,
        60*60*4,
        60*60*12,
        60*60*24,
        60*60*24*2,
        60*60*24*4,
        60*60*24*8,
        60*60*24*16,
        60*60*24*64
    ]

import bisect

def get_interval_bucket(interval):
    return bisect.bisect_right(INTERVAL_BUCKETS, interval)

