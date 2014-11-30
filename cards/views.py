from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.utils import timezone

from cards.models import Card, CardSet, AssignedCard
from scheduling.scheduling import log_rep, get_scheduled_cards, add_unseen_cards, update_card
from scheduling.models import RepIntervalLog

import json, datetime

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@login_required
def get_study_queue(request, add_new=False):
    """Grab the cards in the study queue for the given user as
    a JSON array.
    """
    cards = get_scheduled_cards(request.user)
    cards_dicts = [model_to_dict(card) for card in cards];

    if add_new:
        new_cards = add_unseen_cards(request.user)
        cards_dicts.extend([model_to_dict(card) for card in new_cards])

    return JsonResponse(cards_dicts, safe=False)

@login_required
def new_log(request, card_id, grade):
    card_id = int(card_id)
    grade = int(grade)

    card = Card.objects.get(id=card_id)
    assigned_card = AssignedCard.objects.get(user=request.user, card=card)

    now = timezone.now()
    log_rep(assigned_card, grade, now)
    update_card(assigned_card, grade, now)

    return JsonResponse({"success": True})

@login_required
def add_card_set(request, card_set_id):
    for card in CardSet.objects.get(id=card_set_id).card_set.all():
        assigned_card = AssignedCard(card=card, user=request.user)
        assigned_card.save()
    return JsonResponse({"success": True})

