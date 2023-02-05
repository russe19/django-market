from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from catalog.models import Offer


class Profile(models.Model):
    """Профиль"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Balance'), default=0)
    number = models.IntegerField(blank=True, verbose_name=_('Phone number'))
    telegram = models.CharField(max_length=50, blank=True, verbose_name=_('Telegram'))

    class Meta:
        verbose_name_plural = _('profiles')
        verbose_name = _('profile')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class ProfileImage(models.Model):
    """Фото профиля"""
    profile = models.OneToOneField(Profile, verbose_name=_('profile'), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.profile.user.first_name} {self.profile.user.last_name}'

    class Meta:
        verbose_name_plural = _('profile images')
        verbose_name = _('profile image')


class Status(models.Model):
    name = models.CharField(verbose_name=_('Status'), max_length=100)

    def __str__(self):
        return self.name


class Bonus(models.Model):
    """Бонусы пользователя"""
    profile = models.OneToOneField('Profile', verbose_name=_('profile'), on_delete=models.CASCADE)
    count = models.IntegerField(default=0, verbose_name=_('bonus count'))
    status = models.ForeignKey('Status', on_delete=models.CASCADE, verbose_name=_('Status'))

    def __str__(self):
        return f'{self.profile.user.first_name} {self.profile.user.last_name}'


class HistoryBuy(models.Model):
    """История покупок"""
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, verbose_name=_('user'), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
