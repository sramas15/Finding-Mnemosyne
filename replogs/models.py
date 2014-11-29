from django.contrib.auth.models import User
from django.db import models
from cards.models import Card

class RepLog(models.Model):
    card = models.ForeignKey(Card)
    user = models.ForeignKey(User)
    # TODO: add the rest of the fields!

