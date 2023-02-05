from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from users.models import Profile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text=_('First name'))
    last_name = forms.CharField(max_length=30, required=False, help_text=_('Last name'))
    email = forms.EmailField(required=False, help_text=_('Email'))
    balance = forms.IntegerField(help_text=_('Balance'), min_value=0, max_value=999999)
    number = forms.IntegerField(help_text=_('Number'), required=False, min_value=000000, max_value=99999999999)
    telegram = forms.CharField(help_text=_('Telegram'), required=False)
    image = forms.ImageField(help_text=_('Avatar'))


class RegisterFormUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('telegram', 'number')


class BalanceForm(forms.Form):
    count = forms.IntegerField(help_text=_('Up balance'), min_value=0, max_value=9999999)


class HistoryForm(forms.Form):
    day = forms.IntegerField(help_text=_('The period for which we request the history'),
                             min_value=0, max_value=365, required=False)
