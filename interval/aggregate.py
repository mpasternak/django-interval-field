from django.db.models import Avg as _Avg

from interval.fields import IntervalField


class Avg(_Avg):
    """Average an IntervalField and return the result as a timedelta.

    ``django.db.models.sql.aggregates`` (used by the previous implementation)
    was removed in Django 1.8. The modern aggregation API only needs the
    output field declared so the averaged value is coerced back to an
    interval.
    """

    def __init__(self, *expressions, **extra):
        extra.setdefault("output_field", IntervalField())
        super().__init__(*expressions, **extra)
