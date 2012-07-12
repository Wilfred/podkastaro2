# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.decorators.cache import cache_page


from models import Podcast, RssFeed, Episode, MultimediaFile

SIX_HOURS = 60 * 60 * 6
ONE_WEEK = 60 * 60 * 24 * 7


def get_paginated_content(request, content):
    paginator = Paginator(content, 6) # why six? It looked good.

    try:
        page_number = int(request.GET.get(u'paĝo', 1))
    except ValueError:
        # invalid number
        page_number = 1

    try:
        page_of_content = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        # number is out of range, show last page
        page_of_content = paginator.page(paginator.num_pages)

    return page_of_content


@cache_page(SIX_HOURS)
def index(request):
    episodes = Episode.objects.all()

    episodes_with_multimedia = []
    for episode in episodes:
        episodes_with_multimedia.append((episode,
                                         MultimediaFile.objects.filter(episode=episode)))

    page_of_episodes = get_paginated_content(request,
                                             episodes_with_multimedia)

    template_vars = {'episodes': page_of_episodes}
    
    return render_to_response('index.html', template_vars,
                              RequestContext(request))


@cache_page(ONE_WEEK)
def about(request):
    return render_to_response('about.html', {}, RequestContext(request))


@cache_page(SIX_HOURS)
def view_podcast(request, podcast_name):
    podcast = Podcast.objects.get_by_slug(podcast_name)
    episodes = Episode.objects.filter(podcast=podcast)

    episodes_with_multimedia = []
    for episode in episodes:
        episodes_with_multimedia.append((episode,
                                         MultimediaFile.objects.filter(episode=episode)))

    page_of_episodes = get_paginated_content(request,
                                             episodes_with_multimedia)

    template_vars = {'podcast': podcast, 'episodes': page_of_episodes}

    return render_to_response('podcast.html', template_vars,
                              RequestContext(request))

def check_feeds(request):
    for feed in RssFeed.objects.all():
        # FIXME: we are hitting the DB twice for no good reason
        check_feed(request, feed.id)

    return HttpResponse('Checked all feeds.')

def check_feed(request, feed_id):
    feed = RssFeed.objects.get(id=feed_id)
    feed.update_episodes()

    return HttpResponse('Updated one RSS feed.')
