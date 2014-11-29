from django.contrib.auth.models import User
from django.db import models
from cards.models import Card

class RepLog(models.Model):
    user = models.ForeignKey(User)
    card = models.ForeignKey(Card)
    
    # TODO: add the rest of the fields!

