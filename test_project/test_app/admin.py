from django.contrib.admin import site
from test_app.models import TestModel

site.register(TestModel)
