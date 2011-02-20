from django.db import models

from utils import eo_slugify

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

class Episode(models.Model):
    podcast = models.ForeignKey(Podcast)
    raw_description = models.TextField()

class MultimediaFile(models.Model):
    pass
