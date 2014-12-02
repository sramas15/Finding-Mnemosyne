from django.db import models
from django.contrib.auth.models import User

class CardSet(models.Model):
    name = models.CharField(max_length=80)

class Card(models.Model):
    card_set = models.ForeignKey(CardSet)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

class AssignedCard(models.Model):
    card = models.ForeignKey(Card)
    user = models.ForeignKey(User)
    last_shown = models.DateTimeField(null=True)
    last_grade = models.SmallIntegerField(default=0)
    easiness = models.FloatField(default=2.5)
    acq_reps = models.IntegerField(default=0)
    ret_reps = models.IntegerField(default=0)
    ret_reps_since_lapse = models.IntegerField(default=0)
    lapses = models.IntegerField(default=0)
    scheduled_rep = models.DateTimeField(null=True)

