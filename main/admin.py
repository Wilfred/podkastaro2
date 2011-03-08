from main.models import Podcast, RssFeed, Episode, MultimediaFile
from django.contrib import admin

for cls in [MultimediaFile]:
    admin.site.register(cls)

class EpisodeAdmin(admin.ModelAdmin):
    list_filter = ('podcast',)
    list_display = ('title', 'podcast', 'time')

admin.site.register(Episode, EpisodeAdmin)

class RssFeedAdmin(admin.ModelAdmin):
    list_display = ('podcast', 'url')

admin.site.register(RssFeed, RssFeedAdmin)

class PodcastAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'short_description')

    def short_description(self, obj):
        return ' '.join(obj.description.split(' ')[:20])

admin.site.register(Podcast, PodcastAdmin)


