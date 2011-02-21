# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from models import Podcast, RssFeed, Episode, MultimediaFile


def index(request):
    episodes = Episode.objects.all()

    episodes_with_multimedia = []
    for episode in episodes:
        episodes_with_multimedia.append((episode,
                                         MultimediaFile.objects.filter(episode=episode)))

    paginator = Paginator(episodes_with_multimedia, 6)

    try:
        page_number = int(request.GET.get(u'paĝo', 1))
    except ValueErorr:
        # invalid number
        page_number = 1

    try:
        page_of_episodes = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        # number is out of range, show last page
        page_of_episodes = paginator.page(paginator.num_pages)

    template_vars = {'episodes': page_of_episodes}
    
    return render_to_response('index.html', template_vars,
                              RequestContext(request))

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
