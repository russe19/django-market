from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Offer(models.Model):
    """Товар"""
    seller = models.ForeignKey(User, verbose_name=_('seller'), on_delete=models.CASCADE, related_name='seller')
    user = models.ForeignKey(User, verbose_name=_('user'), blank=True, null=True, on_delete=models.CASCADE,
                             related_name='user')
    name = models.CharField(max_length=50, verbose_name=_('Cover name'), default='Empty')
    description = models.TextField(max_length=1000, verbose_name=_('Description'), default='Empty')
    created_at = models.DateField(verbose_name=_('Date create'), auto_now_add=True)
    date = models.DateField(blank=True, null=True, verbose_name=_('date buy'))
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Price'))
    type = models.ForeignKey('TypeOffer', verbose_name=_('type offer'), on_delete=models.CASCADE)
    property = models.ManyToManyField('Property', through='ProductProperty', verbose_name=_('property'))

    def __str__(self) -> str:
        return f'Product(pk:{self.pk}, name:{self.name})'


class TypeOffer(models.Model):
    """Тип товара"""
    name = models.CharField(max_length=100, verbose_name=_('offer type'))

    def __str__(self):
        return self.name


class Cover(models.Model):
    """Обложка"""
    offer = models.OneToOneField(Offer, verbose_name=_('offer'), on_delete=models.CASCADE, related_name='cover')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.offer.name

    class Meta:
        verbose_name_plural = _('covers')
        verbose_name = _('cover')


class MusicText(models.Model):
    """Текст"""
    offer = models.OneToOneField(Offer, verbose_name=_('offer'), on_delete=models.CASCADE, related_name='text')
    text = models.TextField(max_length=1000, verbose_name=_('Text'))
    style = models.ForeignKey('Style', verbose_name=_('Style'), blank=True, null=True,
                              on_delete=models.SET_NULL)

    def __str__(self):
        return self.offer.name

    class Meta:
        verbose_name_plural = _('music texts')
        verbose_name = _('music text')


class Music(models.Model):
    """Музыка"""
    offer = models.OneToOneField(Offer, verbose_name=_('offer'), on_delete=models.CASCADE, related_name='music')
    genre = models.ForeignKey('Genre', verbose_name=_('Genre'), blank=True, null=True,
                              on_delete=models.SET_NULL)
    sound = models.FileField(upload_to='musics/')

    def __str__(self):
        return self.offer.name

    class Meta:
        verbose_name_plural = _('musics')
        verbose_name = _('music')


class Genre(models.Model):
    """Жанр"""
    name = models.CharField(verbose_name=_('Genre'), max_length=100)


class Style(models.Model):
    """Стиль"""
    name = models.CharField(verbose_name=_('Style'), max_length=100)


class Property(models.Model):
    """Свойство продукта"""
    name = models.CharField(max_length=512, verbose_name=_("name"))

    def str(self):
        return self.name


class ProductProperty(models.Model):
    """Значение свойства продукта"""
    product = models.ForeignKey(Offer, on_delete=models.PROTECT)
    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name='prod')
    value = models.CharField(max_length=128, verbose_name=_("value"))

    def str(self):
        return self.property.name
