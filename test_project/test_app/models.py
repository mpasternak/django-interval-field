from django.db import models

from interval.fields import IntervalField

from datetime import timedelta


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

    def __unicode__(self):
        return ", ".join(
            [
                unicode(self.not_required_interval),
                unicode(self.required_interval),
                unicode(self.required_interval_with_limits)
            ])
