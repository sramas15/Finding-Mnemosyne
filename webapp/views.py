from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.forms.models import model_to_dict

from webapp.forms import UploadCardSetForm
from cards.file_formats import Mnemosyne2Cards
from cards.models import Card, CardSet

import sys
import json

@login_required
def home(request):
    return render_to_response('home.html',
            {'card_sets': CardSet.objects.all()},
            context_instance=RequestContext(request))

@login_required
def study(request):
    cards = CardSet.objects.get(id=1).card_set.all()
    cards_dict = [model_to_dict(card) for card in cards];
    return render_to_response('study.html',
            {'cards_json': json.dumps(cards_dict)},
            context_instance=RequestContext(request))

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
