from datetime import timedelta

from django.db import models
from django.urls import reverse

from interval.fields import IntervalField


class TestModel(models.Model):
    # Not a pytest test class despite the name.
    __test__ = False

    not_required_interval = IntervalField(
        "I am not required", null=True, blank=True, format="DH"
    )

    required_interval = IntervalField(format="H", default=timedelta(hours=3))

    required_interval_with_limits = IntervalField(
        min_value=timedelta(hours=1), max_value=timedelta(days=5), format="DHMSX"
    )

    def __str__(self):
        return ", ".join(
            [
                str(self.not_required_interval),
                str(self.required_interval),
                str(self.required_interval_with_limits),
            ]
        )

    def get_absolute_url(self):
        return reverse("detail_model", args=[str(self.pk)])
