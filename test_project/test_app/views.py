from django.shortcuts import render_to_response

from test_app.models import TestModel

from django.forms.models import ModelForm


class TestForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = TestModel


def test_index(request):
    return render_to_response(
        'form.html', dict(form=TestForm())
    )
