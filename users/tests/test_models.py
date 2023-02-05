from django.contrib.auth.models import User
from django.test import TestCase

from users.models import Profile


class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test123', email='passwordTest123@bk.ru', password='passwordTest123')

    def test_profile_model(self):
        User.objects.get(id=1)
        Profile.objects.create(user=self.user, balance=50, number=7777777, telegram='test')
        self.assertEqual(len(Profile.objects.all()), 1)
