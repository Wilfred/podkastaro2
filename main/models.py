from django.db import models
from datetime import datetime
import calendar
import logging

import libs.feedparser
from templatetags.eo_slugify import eo_slugify
from libs.BeautifulSoup import BeautifulSoup

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
    website = models.URLField()

    objects = PodcastManager()

    class Meta:
        ordering = ['name']

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

            time_struct = entry['updated_parsed']
            if time_struct:
                time = datetime.fromtimestamp(calendar.timegm(time_struct))
            else:
                # fortunately very rare that podcasts don't have dates, but can happen
                # we choose today, but log the error for the admin check
                logging.error('Episode %s (from %s) had no time, assuming today.' \
                                  % (title, self.podcast.name))
                time = datetime.now()

            # create or update episode
            try:
                # if already exists, update
                episode = Episode.objects.get(title=title,
                                              podcast=self.podcast, time=time)
                episode.raw_description = summary
            except Episode.DoesNotExist:
                # create new
                episode = Episode(podcast=self.podcast, title=title,
                                  raw_description=summary,
                                  time=time)
            episode.save()

            # create or update attachments
            for attachment in entry.get('links', []):
                if attachment.get('type', 'unknown') == 'audio/mpeg':
                    url = attachment['url']
                    MultimediaFile.objects.get_or_create(episode=episode,
                                                         url=url)
                elif attachment.get('href', '').endswith('.mp3'):
                    url = attachment['href']
                    MultimediaFile.objects.get_or_create(episode=episode,
                                                         url=url)


class Episode(models.Model):
    podcast = models.ForeignKey(Podcast)

    title = models.CharField(max_length=400)
    raw_description = models.TextField()
    time = models.DateTimeField()

    class Meta:
        ordering = ['-time']

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.podcast.name)

    def get_pretty_description(self):
        # already sanitised by feedparser, but we want to do some beautifying
        def strip_inline_styles(soup):
            for node in soup.findAll():
                del node['style']

        def remove_posterous_junk(soup):
            # remove mp3 image which is in div.p_audio_embed
            for node in soup.findAll('div', 'p_audio_embed'):
                node.extract()

            # remove 'permalink' etc trailer
            for node in soup.findAll(text='Permalink'):
                node.parent.parent.extract()

        soup = BeautifulSoup(self.raw_description)

        strip_inline_styles(soup)
        remove_posterous_junk(soup)

        return str(soup)

    
class MultimediaFile(models.Model):
    # one episode can have several files
    episode = models.ForeignKey(Episode)
    url = models.URLField()

    def __unicode__(self):
        return "%s: %s" % (self.episode.title, self.url)
