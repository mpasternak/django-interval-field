import os

from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib import admin

from test_app.views import ModelListView, ModelCreateView, ModelDetailView, ModelEditView


admin.autodiscover()
urlpatterns = patterns('',

    url(r'^$', ModelListView.as_view(), name="list_models"),
    url(r"create.html", ModelCreateView.as_view(), name="create_model"),
    url(r'^detail/(?P<pk>[0-9]+)$', ModelDetailView.as_view(), name="detail_model"),
    url(r'^edit/(?P<pk>[0-9]+)$', ModelEditView.as_view(), name="edit_model"),
    url(r'^admin/', include(admin.site.urls)),
)

