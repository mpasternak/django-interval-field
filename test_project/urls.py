from django.contrib import admin
from django.urls import path, re_path

from test_app.views import (
    ModelCreateView,
    ModelDetailView,
    ModelEditView,
    ModelListView,
)

urlpatterns = [
    path("", ModelListView.as_view(), name="list_models"),
    re_path(r"create\.html", ModelCreateView.as_view(), name="create_model"),
    path(
        "detail/<int:pk>",
        ModelDetailView.as_view(),
        name="detail_model",
    ),
    path(
        "edit/<int:pk>",
        ModelEditView.as_view(),
        name="edit_model",
    ),
    path("admin/", admin.site.urls),
]
