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

    # TODO: additional metadata
