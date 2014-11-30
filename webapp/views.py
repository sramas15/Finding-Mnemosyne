from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.forms.models import model_to_dict

from webapp.forms import UploadCardSetForm
from cards.file_formats import Mnemosyne2Cards
from cards.models import Card, CardSet, AssignedCard

import sys
import json

@login_required
def home(request):
    # The user's cards
    user_cards = AssignedCard.objects.filter(user=request.user)

    card_set_info = [{
            'name': card_set.name,
            'id': card_set.id,
            'added': bool(AssignedCard.objects.filter(user=request.user, card__card_set=card_set))
        } for card_set in CardSet.objects.all()]

    return render_to_response('home.html', {
            'card_sets': card_set_info,
            'num_cards': len(user_cards)
        }, context_instance=RequestContext(request))

@login_required
def study(request):
    return render_to_response('study.html', context_instance=RequestContext(request))

@login_required
def upload_card_set(request):
    if request.method == 'POST':
        form = UploadCardSetForm(request.POST, request.FILES)
        if form.is_valid():
            # Read cards file
            try:
                cards = Mnemosyne2Cards.read(request.FILES['file'])
            except Exception:
                # FIXME be more specific about what to catch
                cards = None

            #print >>sys.stderr, cards
            if cards:
                # Create new card set
                card_set = CardSet(name=form.cleaned_data['name'])
                card_set.save()

                # Create cards
                for question, answer in cards:
                    card = Card(card_set=card_set, question=question, answer=answer)
                    card.save()

        # TODO: provide feedback for invalid uploads
    else:
        form = UploadCardSetForm()
    return render_to_response('upload.html',
            {'form': form},
            context_instance=RequestContext(request))

