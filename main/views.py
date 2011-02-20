from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from models import Podcast, RssFeed, Episode
import libs.feedparser

def index(request):
    return render_to_response('page.html', {}, RequestContext(request))

def podcast(request, podcast_name):
    podcast = Podcast.objects.get_by_slug(podcast_name)
    template_vars = {'podcast': podcast}

    return render_to_response('podcast.html', template_vars,
                              RequestContext(request))

def check_feeds(request):
    feeds = RssFeed.objects.all()

    for feed in feeds:
        for episode in get_episodes_from_feed(feed):
            episode.save()

    return HttpResponse('saved.')

def get_episodes_from_feed(feed):
    rss_feed = libs.feedparser.parse(feed.url)

    episodes = []
    for entry in rss_feed['entries']:
        title = entry['title']
        summary = entry['summary']

        episodes.append(Episode(podcast=feed.podcast, title=title,
                                raw_description=summary))
        
    return episodes
