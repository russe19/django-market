from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from catalog.models import Offer, TypeOffer


class BasketTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test123', email='passwordTest123@bk.ru', password='passwordTest123')
        type_offer = TypeOffer.objects.create(name='test')
        Offer.objects.create(seller=user, name='test', description='test',
                             price=100, type=type_offer)

    def setUp(self) -> None:
        self.client.post(reverse('login'), {'username': 'test123', 'password': 'passwordTest123'}, follow=True)

    def test_basket(self):
        response = self.client.get(reverse('basket'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/basket.html')

    def test_clear(self):
        response = self.client.post(reverse('clear'), follow=True)
        self.assertEqual(response.status_code, 200)
