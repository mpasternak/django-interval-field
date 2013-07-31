from django.db.models import Avg as _Avg
from django.db.models.sql.aggregates import Avg as _AvgSQL

from interval.fields import IntervalField


class AvgSQL(_AvgSQL):
    is_computed = False


class Avg(_Avg):
    def add_to_query(self, query, alias, col, source, is_summary):
        aggregate = AvgSQL(col, source=IntervalField(), is_summary=is_summary,
                           **self.extra)
        query.aggregates[alias] = aggregate
