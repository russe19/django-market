from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppMediaConfig(AppConfig):
    name = 'catalog'
    verbose_name = _('catalog')
