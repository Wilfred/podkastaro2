from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Podcast

def index(request):
    return render_to_response('page.html', {}, RequestContext(request))

def podcast(request, podcast_name):
    podcast = Podcast.objects.get_by_slug(podcast_name)
    template_vars = {'podcast': podcast}

    return render_to_response('podcast.html', template_vars,
                              RequestContext(request))
