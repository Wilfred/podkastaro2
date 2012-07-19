from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ('^admin/', include(admin.site.urls)),

    url('^$', 'podcasts.views.index', name='index'),
    url('^pri-podkastaro$', 'podcasts.views.about', name='about'),
    url('^p/(?P<podcast_id>\d+)/(?P<podcast_name>.+)', 'podcasts.views.view_podcast', name="view_podcast"),

    ('^cron/check_feeds', 'podcasts.views.check_feeds'),
)
