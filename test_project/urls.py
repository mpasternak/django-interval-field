from django.conf.urls.defaults import patterns, include, url
import settings
import os

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$',
        'django.views.generic.simple.direct_to_template',
        {'template': 'index.html'}
        ),

    url(r'^test/', 'test_app.views.test_index'),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': os.path.join(
            os.path.dirname(settings.__file__),
            'static')}))
