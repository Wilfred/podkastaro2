from main.models import Podcast, RssFeed, Episode, MultimediaFile
from django.contrib import admin

for cls in [Podcast, RssFeed, Episode, MultimediaFile]:
    admin.site.register(cls)
