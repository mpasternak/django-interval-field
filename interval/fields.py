# -*- encoding: utf-8 -*-

from django.db import models
from django.db.models.fields.subclassing import SubfieldBase
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from datetime import timedelta
import six

from interval.forms import IntervalFormField

day_seconds = 24 * 60 * 60
microseconds = 1000000


def formatError(value):
    raise ValueError(
        "please use [[DD]D days,]HH:MM:SS[.ms] instead of %r" % value)


def timedelta_topgsqlstring(value):
    buf = []
    for attr in ['days', 'seconds', 'microseconds']:
        v = getattr(value, attr)
        if v:
            buf.append('%i %s' % (v, attr.upper()))
    if not buf:
        return '0'
    return " ".join(buf)


def timedelta_tobigint(value):
    return (
        value.days * day_seconds * microseconds
        + value.seconds * microseconds
        + value.microseconds
        )


def range_check(value, name, min=None, max=None):
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValueError("%s is not an integer" % value)

    if min is not None:
        if value < min:
            raise ValueError("%s is less than %s" % (value, min))

    if max is not None:
        if value > max:
            raise ValueError("%s is more than %s" % (value, max))

    return value


class IntervalField(six.with_metaclass(SubfieldBase, models.Field)):
    """This is a field, which maps to Python's datetime.timedelta.

    For PostgreSQL, its type is INTERVAL - a native interval type.
    - http://www.postgresql.org/docs/8.4/static/datatype-datetime.html

    For other databases, its type is BIGINT and timedelta value is stored
    as number of seconds * 1000000 .
    """

    description = _("interval")

    def __init__(
        self, verbose_name=None, min_value=None, max_value=None, format=None,
        *args, **kw):

        models.Field.__init__(
            self, verbose_name=verbose_name, *args, **kw)

        self.min_value = min_value
        self.max_value = max_value
        self.format = format

        if self.min_value is not None and self.max_value is not None:
            if self.min_value >= self.max_value:
                raise ValueError('min_value >= max_value')

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'].find('postgresql') >= 0 or \
                connection.settings_dict['ENGINE'].find('postgis') >= 0:
            return 'INTERVAL'
        return 'BIGINT'

    def to_python(self, value):
        if isinstance(value, timedelta):
            # psycopg2 will return a timedelta() for INTERVAL type column
            # in database
            return value

        if value is None or value is '' or value is u'':
            return None

        # string forms: in form like "X days, HH:MM:SS.ms" (can be used in
        # fixture files)
        if isinstance(value, six.string_types) and value.find(":") >= 0:
            days = 0

            if value.find("days,") >= 0 or value.find("day,") >= 0:
                if value.find("days,") >= 0:
                    days, value = value.split("days,")
                else:
                    days, value = value.split("day,")
                value = value.strip()
                try:
                    days = int(days.strip())
                except ValueError:
                    formatError(value)

                days = range_check(days, "days", 0)

            try:
                h, m, s = value.split(":")
            except ValueError:
                formatError(value)

            h = range_check(h, "hours", 0)
            m = range_check(m, "minutes", 0, 59)

            if s.find(".") >= 0:
                s, ms = s.split(".")
            else:
                ms = "0"

            s = range_check(s, "seconds", 0, 59)

            l = len(ms)
            ms = range_check(ms, "microseconds", 0, microseconds)
            ms = ms * (microseconds / (10 ** l))

            return timedelta(
                days=days, hours=h, minutes=m,
                seconds=s, microseconds=ms)

        # other database backends:
        return timedelta(seconds=float(value) / microseconds)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None or value is '':
            return None

        if connection.settings_dict['ENGINE'].find('postgresql') >= 0 or \
                connection.settings_dict['ENGINE'].find('postgis') >= 0:
            if isinstance(value, six.string_types):
                # Can happen, when using south migrations
                return value
            return timedelta_topgsqlstring(value)

        return timedelta_tobigint(value)

    def formfield(self, form_class=IntervalFormField, **kwargs):
        defaults = {'min_value': self.min_value,
                    'max_value': self.max_value,
                    'format': self.format or 'DHMS',
                    'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text}

        if self.has_default():
            defaults['initial'] = self.default

        defaults.update(kwargs)
        return form_class(**defaults)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^interval\.fields\.IntervalField"])
except ImportError:
    pass
