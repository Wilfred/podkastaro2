from main.models import Podcast, RssFeed, Episode, MultimediaFile
from django.contrib import admin

for cls in [Podcast, MultimediaFile]:
    admin.site.register(cls)

class EpisodeAdmin(admin.ModelAdmin):
    list_filter = ('podcast',)
    list_display = ('title', 'podcast', 'time')

admin.site.register(Episode, EpisodeAdmin)

class RssFeedAdmin(admin.ModelAdmin):
    list_display = ('podcast', 'url')

admin.site.register(RssFeed, RssFeedAdmin)
