from pathlib import Path, PurePath

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from catalog.forms import CoverForm, MusicForm, TextForm
from catalog.models import Genre, Style


class OfferFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre = Genre.objects.create(name='test')
        cls.style = Style.objects.create(name='test')

    def test_cover(self):
        cwd = Path.cwd()
        image_jpg = open(PurePath.joinpath(cwd, 'catalog', 'tests', 'tests_file', 'image.jpg'), "rb")
        image = SimpleUploadedFile(image_jpg.name, image_jpg.read())
        data = {'name': 'name', 'description': 'test', 'price': 50}
        files = {'images': image}
        form = CoverForm(data=data, files=files)
        self.assertTrue(form.is_valid())

    def test_music(self):
        cwd = Path.cwd()
        sound_file = open(PurePath.joinpath(cwd, 'catalog', 'tests', 'tests_file', 'music.wav'), "rb")
        sound = SimpleUploadedFile(sound_file.name, sound_file.read())
        data = {'name': 'name', 'description': 'test', 'price': 50, 'genre': self.genre}
        files = {'sound': sound}
        form = MusicForm(data=data, files=files)
        self.assertTrue(form.is_valid())

    def test_text(self):
        data = {'name': 'name', 'description': 'test', 'text': 'text', 'price': 50, 'style': self.style}
        form = TextForm(data=data)
        self.assertTrue(form.is_valid())
