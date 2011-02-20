from django.db import models
from datetime import datetime
import calendar

import libs.feedparser
from templatetags.eo_slugify import eo_slugify

class PodcastManager(models.Manager):
    def get_by_slug(self, slug):
        all_podcasts = self.all() # we will never have many podcasts

        for podcast in all_podcasts:
            if eo_slugify(podcast.name) == slug:
                return podcast

        raise self.model.DoesNotExist()

class Podcast(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()

    objects = PodcastManager()

    def __unicode__(self):
        return self.name

class RssFeed(models.Model):
    # one podcast can have several RSS Feeds
    podcast = models.ForeignKey(Podcast)
    url = models.URLField()

    def __unicode__(self):
        return "%s %s" % (self.podcast.name, self.url)

    def update_episodes(self):
        rss_feed = libs.feedparser.parse(self.url)

        for entry in rss_feed['entries']:
            title = entry['title']
            summary = entry['summary']
            time = datetime.fromtimestamp(calendar.timegm(entry['updated_parsed']))

            # create or update episode
            try:
                # if already exists, update
                episode = Episode.objects.get(title=title)
                episode.podcast = self.podcast
                episode.raw_description = summary
                episode.time = time
            except Episode.DoesNotExist:
                # create new
                episode = Episode(podcast=self.podcast, title=title,
                                  raw_description=summary,
                                  time=time)
            episode.save()

            # create or update attachments
            for attachment in entry.get('links', []):
                if attachment['type'] == 'audio/mpeg':
                    url = attachment['url']
                    MultimediaFile.objects.get_or_create(episode=episode,
                                                         url=url)


class Episode(models.Model):
    podcast = models.ForeignKey(Podcast)

    title = models.CharField(max_length=400)
    raw_description = models.TextField()
    time = models.DateTimeField()

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.podcast.name)

    
class MultimediaFile(models.Model):
    # one episode can have several files
    episode = models.ForeignKey(Episode)
    url = models.URLField()

    def __unicode__(self):
        return "%s: %s" % (self.episode.title, self.url)
