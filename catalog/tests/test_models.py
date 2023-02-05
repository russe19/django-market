from pathlib import Path, PurePath

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from catalog.models import (Cover, Genre, Music, MusicText, Offer, Style,
                            TypeOffer)


class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='test123', email='passwordTest123@bk.ru',
                                                        password='passwordTest123')
        cls.types = TypeOffer.objects.create(name='test')

    def test_profile_model(self):
        self.offer = Offer.objects.create(seller=self.user, name='test', description='test', price=777, type=self.types)
        self.assertEqual(len(Offer.objects.all()), 1)


class ModelTestMusic(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(username='test123', email='passwordTest123@bk.ru',
                                                    password='passwordTest123')
        types = TypeOffer.objects.create(name='test')
        cls.offer = Offer.objects.create(seller=user, name='test', description='test', price=777, type=types)
        cls.genre = Genre.objects.create(name='test')
        cls.style = Style.objects.create(name='test')

    def test_cover_model(self):
        cwd = Path.cwd()
        image_jpg = open(PurePath.joinpath(cwd, 'catalog', 'tests', 'tests_file', 'image.jpg'), "rb")
        image = SimpleUploadedFile(image_jpg.name, image_jpg.read())
        self.cover = Cover.objects.create(offer=self.offer, image=image)
        self.assertEqual(len(Cover.objects.all()), 1)

    def test_music_model(self):
        cwd = Path.cwd()
        sound_file = open(PurePath.joinpath(cwd, 'catalog', 'tests', 'tests_file', 'music.wav'), "rb")
        sound = SimpleUploadedFile(sound_file.name, sound_file.read())
        self.music = Music.objects.create(offer=self.offer, genre=self.genre, sound=sound)
        self.assertEqual(len(Music.objects.all()), 1)

    def test_text_model(self):
        self.music = MusicText.objects.create(offer=self.offer, text='test text', style=self.style)
        self.assertEqual(len(MusicText.objects.all()), 1)
