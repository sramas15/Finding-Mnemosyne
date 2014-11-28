from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext

def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request))

def study(request):
    return render_to_response('study.html', context_instance=RequestContext(request))
