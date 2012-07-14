from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^admin/', include(admin.site.urls)),

    ('^$', 'podcasts.views.index'),
    ('^pri-podkastaro$', 'podcasts.views.about'),
    ('^podkasto/(?P<podcast_name>.+)', 'podcasts.views.view_podcast'),

    ('^cron/check_feeds', 'podcasts.views.check_feeds'),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': 'static/'}),
)
