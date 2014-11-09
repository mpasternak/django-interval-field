"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import timedelta
from time import sleep

from django.test import TestCase
from django.test import Client

from django.contrib.auth.models import User
from test_app.models import TestModel

MICSEC = 10**6

class TestTestApp(TestCase):
    def test_list_empty(self):
        request = self.client.get("/")
        self.assertContains(request, "There are no models, yet.")

    def test_list(self):
        delta = 2 * 24 * 60 * 60 + 30 * 24 * 60 * 60  # 2 days and 3 months
        TestModel.objects.create(
            not_required_interval=12 * MICSEC,  # 12 secs
            required_interval=60 * MICSEC,  # one hour
            required_interval_with_limits=delta * MICSEC
        )

        TestModel.objects.create(
            not_required_interval=timedelta(days=1),
            required_interval=timedelta(weeks=2),
            required_interval_with_limits=timedelta(days=3),
        )

        response = self.client.get("/")
        objs = response.context["object_list"]
        self.assertEqual(2, len(objs))
        self.assertEqual(200, response.status_code)

    def test_create(self):
        response = self.client.post(
            "/create.html", {
                "required_interval_with_limits_hours": 0,
                "required_interval_with_limits_days": 2,
                "required_interval_with_limits_minutes": 70,
                "required_interval_with_limits_seconds": 4,
                "required_interval_with_limits_microseconds": 0,
                "required_interval_hours": 1,
                "not_required_interval_days": 1,
                "not_required_interval_hours": 3
            }, follow=True
        )

        self.assertRedirects(response, "/detail/{}".format(TestModel.objects.get().pk))

        allObjects = TestModel.objects.all()
        self.assertEqual(1, len(allObjects))

        obj = allObjects[0]
        self.assertEqual("1 day, 3:00:00, 1:00:00, 2 days, 1:10:04", str(obj))
        exp = timedelta(days=2, hours=1, minutes=10, seconds=4)
        self.assertEqual(exp, obj.required_interval_with_limits)
        self.assertEqual(timedelta(hours=1), obj.required_interval)
        self.assertEqual(timedelta(days=1, hours=3), obj.not_required_interval)

    def test_detail(self):
        TestModel.objects.create(
            not_required_interval=timedelta(days=1),
            required_interval=timedelta(weeks=2),
            required_interval_with_limits=timedelta(days=3),
            )

        response = self.client.get("/detail/{}".format(TestModel.objects.get().pk))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "1 day, 0:00:00, 14 days, 0:00:00, 3 days, 0:00:00")

    def test_edit(self):
        TestModel.objects.create(
            not_required_interval=timedelta(days=1),
            required_interval=timedelta(weeks=2),
            required_interval_with_limits=timedelta(days=3),
            )
        response = self.client.get("/edit/{}".format(TestModel.objects.get().pk))
        self.assertEqual(200, response.status_code)

class TestTestAppAdmin(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('foo', 'foomail', 'bar')
        self.client = Client()
        self.client.login(username='foo', password='bar')

    def test_admin(self):
        self.client.get('/admin/')

    def test_test_app_admin_add(self):
        self.client.get('/admin/test_app/testmodel/add/')
