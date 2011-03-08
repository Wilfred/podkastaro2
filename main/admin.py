from main.models import Podcast, RssFeed, Episode, MultimediaFile
from django.contrib import admin

for cls in [Podcast, RssFeed, MultimediaFile]:
    admin.site.register(cls)

class EpisodeAdmin(admin.ModelAdmin):
    list_filter = ('podcast',)
    list_display = ('title', 'podcast', 'time')

admin.site.register(Episode, EpisodeAdmin)
