from pathlib import Path, PurePath

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from catalog.models import (Cover, Genre, Music, MusicText, Offer, Style,
                            TypeOffer)


class CoverTestUpdate(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_login = get_user_model().objects.create_user(username='test123', email='passwordTest123@bk.ru',
                                                          password='passwordTest123')
        cls.user_login = user_login
        cls.url_login = reverse('login')
        cwd = Path.cwd()
        image_jpg = open(PurePath.joinpath(cwd, 'catalog', 'tests', 'tests_file', 'image.jpg'), "rb")
        cls.image = SimpleUploadedFile(image_jpg.name, image_jpg.read())

    def setUp(self) -> None:
        self.client.post(self.url_login, {'username': 'test123', 'password': 'passwordTest123'}, follow=True)
        self.type_offer = TypeOffer.objects.create(name='test')

    def test_cover_create(self):
        data = {
            'name': 'Cover test',
            'description': 'Cover test description',
            'images': self.image,
            'price': 50
        }
        url = reverse('upload_cover')
        response = self.client.post(url, data)
        self.assertEqual(Offer.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_cover_list(self):
        offer = Offer.objects.create(seller=User.objects.get(id=1), name='test', description='test',
                                     price=100, type=self.type_offer)
        Cover.objects.create(offer=offer, image=self.image)
        url = reverse('covers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cover_detail(self):
        offer = Offer.objects.create(seller=User.objects.get(id=1), name='test', description='test',
                                     price=100, type=self.type_offer)
        Cover.objects.create(offer=offer, image=self.image)
        url = reverse('cover_detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class MusicTestUpdate(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_login = get_user_model().objects.create_user(username='test123', email='passwordTest123@bk.ru',
                                                          password='passwordTest123')
        cls.user_login = user_login
        cls.url_login = reverse('login')
        cwd = Path.cwd()
        sound_file = open(PurePath.joinpath(cwd, 'catalog', 'tests', 'tests_file', 'music.wav'), "rb")
        cls.sound = SimpleUploadedFile(sound_file.name, sound_file.read())

    def setUp(self) -> None:
        self.client.post(self.url_login, {'username': 'test123', 'password': 'passwordTest123'}, follow=True)
        self.type_offer = TypeOffer.objects.create(name='test')
        self.genre = Genre.objects.create(name='test')

    def test_music_create(self):
        data = {
            'name': 'Music test',
            'description': 'Music test description',
            'sound': self.sound,
            'price': 50,
            'genre': 1
        }
        url = reverse('upload_music')
        response = self.client.post(url, data)
        self.assertEqual(Offer.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_cover_list(self):
        offer = Offer.objects.create(seller=User.objects.get(id=1), name='test', description='test',
                                     price=100, type=self.type_offer)
        Music.objects.create(offer=offer, sound=self.sound, genre=self.genre)
        url = reverse('musics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cover_detail(self):
        offer = Offer.objects.create(seller=User.objects.get(id=1), name='test', description='test',
                                     price=100, type=self.type_offer)
        Music.objects.create(offer=offer, sound=self.sound, genre=self.genre)
        url = reverse('music_detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TextTestUpdate(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_login = get_user_model().objects.create_user(username='test123', email='passwordTest123@bk.ru',
                                                          password='passwordTest123')
        cls.user_login = user_login
        cls.url_login = reverse('login')

    def setUp(self) -> None:
        self.client.post(self.url_login, {'username': 'test123', 'password': 'passwordTest123'}, follow=True)
        self.type_offer = TypeOffer.objects.create(name='test')
        self.style = Style.objects.create(name='test')

    def test_text_create(self):
        data = {
            'name': 'Cover test',
            'description': 'Cover test description',
            'text': 'Test text',
            'price': 50,
            'style': 1
        }
        url = reverse('upload_text')
        response = self.client.post(url, data)
        self.assertEqual(Offer.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_cover_list(self):
        offer = Offer.objects.create(seller=User.objects.get(id=1), name='test', description='test',
                                     price=100, type=self.type_offer)
        MusicText.objects.create(offer=offer, text='test', style=self.style)
        url = reverse('texts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cover_detail(self):
        offer = Offer.objects.create(seller=User.objects.get(id=1), name='test', description='test',
                                     price=100, type=self.type_offer)
        MusicText.objects.create(offer=offer, text='test', style=self.style)
        url = reverse('text_detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
