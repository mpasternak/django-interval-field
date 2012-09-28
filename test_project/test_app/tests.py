"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import Client

from django.contrib.auth.models import User


class TestTestApp(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        res = self.client.get('/')
        self.assertContains(res, 'go to the admin', status_code=200)

    def test_test(self):
        res = self.client.get('/test/')
        self.assertEquals(res.status_code, 200)


class TestTestAppAdmin(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('foo', 'foomail', 'bar')
        self.client = Client()
        self.client.login(username='foo', password='bar')

    def test_admin(self):
        self.client.get('/admin/')

    def test_test_app_admin_add(self):
        self.client.get('/admin/test_app/testmodel/add/')
