from django.db import models

class Podcast(models.Model):
    name = models.CharField(max_lenth=400)
    description = models.TextField()

class Episode(models.Model):
    podcast = models.ForeignKey(Podcast)
    raw_description = models.TextField()

class MultimediaFile(models.Model):
    pass
