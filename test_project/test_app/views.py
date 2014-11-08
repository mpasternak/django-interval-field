from django.shortcuts import render_to_response

from test_app.models import TestModel

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView


class ModelListView(ListView):
    model = TestModel
    template_name = "list.html"


class ModelCreateView(CreateView):
    model = TestModel
    template_name = "form.html"
    fields = "__all__"


class ModelDetailView(DetailView):
    model = TestModel
    template_name = "detail.html"
    fields = "__all__"


class ModelEditView(UpdateView):
    model = TestModel
    template_name = "form.html"
    fields = "__all__"
