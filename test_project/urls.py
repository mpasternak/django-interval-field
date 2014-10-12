from django.views.generic.base import TemplateView

from django.conf.urls import patterns, url, include

import settings
import os

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', TemplateView.as_view(template_name="index.html")),

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
