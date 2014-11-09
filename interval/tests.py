# -*- encoding: utf-8 -*-

from datetime import timedelta

from django.test import TestCase

from django.conf import settings
from django.core.exceptions import ValidationError

from interval.fields import timedelta_topgsqlstring
from interval.fields import timedelta_tobigint
from interval.fields import range_check
from interval.fields import microseconds
from interval.fields import IntervalField

from interval.forms import IntervalFormField
from interval.forms import IntervalWidget


class FakeConnection:
    def __init__(self, engine):
        self.settings_dict = dict(ENGINE=engine)


class TestIntervalFields(TestCase):
    def test_timedelta_topgsqlstring(self):
        for input, should_be in [
            (timedelta(1, 1, 1), '1 DAYS 1 SECONDS 1 MICROSECONDS'),
            (timedelta(0, 1, 0), '1 SECONDS'),
            (timedelta(0, 0, 0), '0')]:
            v = timedelta_topgsqlstring(input)
            self.assertEqual(v, should_be)

    def test_timedelta_tobigint(self):
        for input, should_be in [
            (timedelta(1, 1, 1),
             1 * 3600 * 24 * microseconds + 1 * microseconds + 1),
            (timedelta(0, 0, 0), 0)]:
            v = timedelta_tobigint(input)
            self.assertEqual(v, should_be)

    def test_range_check(self):
        self.assertEqual(range_check('5', 'foo'), 5)

        for args in [
            ('xx', 'foo'),
            (None, 'foo'),
            ('5', 'foo', 0, 1),
            ('5', 'foo', 6, 7)]:
            self.assertRaises(
                ValueError, range_check, *args)

    def test_IntervalField_init(self):

        self.assertRaises(
            ValueError,
            IntervalField,
            min_value=timedelta(5),
            max_value=timedelta(4)
        )

    def test_IntervalField_db_type(self):

        f = IntervalField()
        self.assertEqual(
            f.db_type(connection=FakeConnection('postgresql')),
            'INTERVAL')
        self.assertEqual(
            f.db_type(connection=FakeConnection('mysql')),
            'BIGINT')

    def test_IntervalField_to_python(self):
        """Test functions of IntervalField without using any
        specific database backend."""

        def do_some_tests():

            valid_strings = ["00:00:00", "00:00:00.0",
                             "10:10:10", "10:10:10.10",
                             "5 days, 22:22:22.22",
                             "5 days, 22:22:22",
                             "1 day, 0:00:00",
                             "00:00:00.22",
                             "00:00:00.222",
                             "00:00:00.2222",
                             "00:00:00.22222",
                             "00:00:00.22222",
                             "00:00:00.222222"]

            invalid_strings = ["10:-10:10", "10:10:-10",
                               "00:00:00.-100", "00:62:00",
                               "00:00:61",
                               "xx days, 12:12:12.123",
                               "12 dayz, 00:00:00",
                               "00:00:00.12345672930923890"]

            a = IntervalField()

            for s in valid_strings:
                a.to_python(s)

            for s in invalid_strings:
                self.assertRaises(ValueError, a.to_python, s)

            for value, should_be in [
                (timedelta(seconds=5),
                 timedelta(seconds=5)),

                ("00:00:05.1",
                 timedelta(seconds=5, microseconds=100000)),

                ("2 days, 00:00:05.1",
                 timedelta(days=2, seconds=5, microseconds=100000)),

                ("2 days, 00:00:05.01",
                 timedelta(days=2, seconds=5, microseconds=10000)),

                ("2 days, 00:00:05.001",
                 timedelta(days=2, seconds=5, microseconds=1000)),

                ("2 days, 00:00:05.0001",
                 timedelta(days=2, seconds=5, microseconds=100)),

                ("2 days, 00:00:05.00001",
                 timedelta(days=2, seconds=5, microseconds=10)),

                ("2 days, 00:00:05.000001",
                 timedelta(days=2, seconds=5, microseconds=1)),
                ]:
                self.assertEqual(a.to_python(value), should_be)

        # "path" the settings rather than changing them because it might
        # effect other tests if do_some_tests raises an exception.
        # See: https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.SimpleTestCase.settings
        with self.settings(DATABASES={"default": {"ENGINE": "postgresql_psycopg2"}}):
            do_some_tests()

        with self.settings(DATABASES={"default": {"ENGINE": "something_else_than_pgsql"}}):
            do_some_tests()

    def test_IntervalField_get_db_prep_value(self):
        f = IntervalField()

        for value, should_be in [
            (f.get_db_prep_value(None,
                                 connection=FakeConnection('none')),
             None),

            (f.get_db_prep_value(timedelta(1),
                                 connection=FakeConnection('postgresql')),
             '1 DAYS'),

            (f.get_db_prep_value(timedelta(1),
                                 connection=FakeConnection('mysql')),
             1 * 3600 * 24 * microseconds)
            ]:
            self.assertEqual(value, should_be)

    def test_IntervalField_formfield(self):
        f = IntervalField()
        f.formfield()


def widgetParams(**kw):
    d = dict(days=0, hours=0, minutes=0, seconds=0, microseconds=0)
    d.update(kw)
    return d


def prepend(prefix, dct):
    ret = {}
    for key, value in dct.items():
        ret[prefix + key] = value
    return ret


class TestIntervalForms(TestCase):
    def test_IntervalWidget_init(self):
        self.assertRaises(
            ValueError,
            IntervalWidget,
            format='Z'
        )

    def test_IntervalWidget_render(self):
        for format in ['DHMSX', 'DHMS', 'D', 'DH', 'DS', 'DX',
                        'HS', 'HX', 'HM', 'MS', 'MX', 'S', 'SX', 'D',
                        'H', 'M']:
            for value in [
                None,
                widgetParams(days=5),
                widgetParams(minutes=10, seconds=50),
                widgetParams(days=5, microseconds=5)]:
                w = IntervalWidget(format=format)
                w.render('foo', value)

    def test_IntervalWidget_render_incomplete(self):
        w = IntervalWidget(format='D')
        w.render('foo', timedelta(days=5))

    def test_IntervalWidget_value_from_datadict(self):
        w = IntervalWidget()
        v = w.value_from_datadict(
            prepend("foo_", widgetParams()), [], 'foo'
        )
        self.assertEqual(v, widgetParams())

        w = IntervalWidget('D')
        v = w.value_from_datadict(
            dict(foo_days='1'), [], 'foo'
        )
        self.assertEqual(v, dict(days=1))

        w = IntervalWidget('D')
        v = w.value_from_datadict(
            dict(foo_days='X'), [], 'foo'
        )
        self.assertEqual(v, dict(days='X', BAD='days'))

    def test_IntervalFormField_clean(self):
        a = IntervalFormField(format='DHMSX', required=True)

        self.assertRaises(ValidationError, a.clean, widgetParams())
        self.assertRaises(ValidationError, a.clean, widgetParams(minutes='xx'))
        a.clean(widgetParams(hours='5'))

        a = IntervalFormField(format='DHMSX', required=False)
        a.clean(widgetParams())
