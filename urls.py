from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^admin/', include(admin.site.urls)),
    ('^$', 'main.views.index'),
    ('^podkasto/(?P<podcast_name>.+)', 'main.views.view_podcast'),
    ('^cron/check_feeds', 'main.views.check_feeds'),
)
