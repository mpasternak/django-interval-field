from django.core.urlresolvers import reverse
from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible

from interval.fields import IntervalField

from datetime import timedelta

@python_2_unicode_compatible
class TestModel(models.Model):

    not_required_interval = IntervalField(
        'I am not required',
        null=True, blank=True,
        format='DH'
    )

    required_interval = IntervalField(
        format='H',
        default=timedelta(hours=3)
    )

    required_interval_with_limits = IntervalField(
        min_value=timedelta(hours=1),
        max_value=timedelta(days=5),
        format='DHMSX'
    )

    def __str__(self):
        return ", ".join(
            [
                six.text_type(self.not_required_interval),
                six.text_type(self.required_interval),
                six.text_type(self.required_interval_with_limits)
            ])

    def get_absolute_url(self):
        return reverse("detail_model", args=[str(self.pk)])