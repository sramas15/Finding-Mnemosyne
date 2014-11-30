from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict

from cards.models import Card, CardSet, AssignedCard

import json

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

@login_required
def get_study_queue(request):
    """Grab the cards in the study queue for the given user as
    a JSON array.
    """
    # TODO use request.user
    cards = CardSet.objects.get(id=1).card_set.all()
    cards_dicts = [model_to_dict(card) for card in cards];
    return JsonResponse(cards_dicts, safe=False)

@login_required
def update_logs(request):
    if request.is_ajax():
        # if logs valid
        pass # process the incoming logs
        return JsonResponse({"success": True})

    return JsonResponse(response_data)

@login_required
def add_card_set(request, card_set_id):
    for card in CardSet.objects.get(id=card_set_id).card_set.all():
        assigned_card = AssignedCard(card=card, user=request.user)
        assigned_card.save()
    return JsonResponse({"success": True})

