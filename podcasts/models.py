# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
import calendar
import logging
import re

import feedparser
from templatetags.eo_slugify import eo_slugify
from BeautifulSoup import BeautifulSoup

class Podcast(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    website = models.URLField()

    class Meta:
        ordering = ['name']

    @property
    def slug_name(self):
        return eo_slugify(self.name)

    def __unicode__(self):
        return self.name


class RssFeed(models.Model):
    # one podcast can have several RSS Feeds
    podcast = models.ForeignKey(Podcast)
    url = models.URLField(unique=True)

    def __unicode__(self):
        return "%s %s" % (self.podcast.name, self.url)

    def update_episodes(self):
        rss_feed = feedparser.parse(self.url)

        for entry in rss_feed['entries']:
            title = entry['title']

            summary = entry['summary']

            if summary.endswith('[...]'):
                # if summary has been truncated
                # there is probably a full html description as <content> instead
                summary = entry['content'][0]['value']

            time_struct = entry['updated_parsed']
            if time_struct:
                time = datetime.fromtimestamp(calendar.timegm(time_struct))
            else:
                logging.error('Episode %s (from %s) had no time, skipping as we probably already have it.' \
                                  % (title, self.podcast.name))
                continue

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

    def get_pretty_title(self):
        if self.title == 'Untitled':
            return 'Sentitolo'
        else:
            return self.title

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

            # remove feedburner tracker images
            for node in soup.findAll('img'):
                node.extract()

        def remove_varsovia_junk(soup):
            for node in soup.findAll('a', text=re.compile(u'Elŝutu')):
                node.parent.extract()
            for node in soup.findAll('a', text=re.compile(u'Download audio file')):
                node.parent.extract()

        soup = BeautifulSoup(self.raw_description)

        strip_inline_styles(soup)

        if self.podcast.name in [u'Voĉoj el Japanio', 'Pola Radio']:
            remove_posterous_junk(soup)
        elif self.podcast.name == 'Varsovia Vento':
            remove_varsovia_junk(soup)
        elif self.podcast.name in ['Radio Vatikana', 'Junula Radio Internacia'] \
                or not self.raw_description:
            # no content in the description
            return 'Neniu priskribo.'

        return str(soup)

    
class MultimediaFile(models.Model):
    # one episode can have several files
    episode = models.ForeignKey(Episode)
    url = models.URLField()

    def __unicode__(self):
        return "%s: %s" % (self.episode.title, self.url)
