from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from models import Podcast, RssFeed, Episode, MultimediaFile


def index(request):
    return render_to_response('page.html', {}, RequestContext(request))

def podcast(request, podcast_name):
    podcast = Podcast.objects.get_by_slug(podcast_name)
    episodes = Episode.objects.filter(podcast=podcast)

    episodes_with_multimedia = []
    for episode in episodes:
        episodes_with_multimedia.append((episode,
                                         MultimediaFile.objects.filter(episode=episode)))

    template_vars = {'podcast': podcast, 'episodes': episodes_with_multimedia}

    return render_to_response('podcast.html', template_vars,
                              RequestContext(request))

def check_feeds(request):
    feeds = RssFeed.objects.all()

    for feed in feeds:
        feed.update_episodes()

    return HttpResponse('saved.')
