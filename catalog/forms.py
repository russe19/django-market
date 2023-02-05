from django import forms
from django.utils.translation import gettext_lazy as _

from catalog.models import Genre, Style


class CoverForm(forms.Form):
    name = forms.CharField(max_length=50, help_text=_('Cover name'))
    description = forms.CharField(widget=forms.Textarea, max_length=1000, help_text=_('Description'))
    images = forms.ImageField(help_text=_('Files'))
    price = forms.IntegerField(help_text=_('Price'), min_value=0, max_value=999999)


class MusicForm(forms.Form):
    name = forms.CharField(max_length=50, help_text=_('Music name'))
    description = forms.CharField(widget=forms.Textarea, max_length=1000, help_text=_('Description'))
    sound = forms.FileField(help_text=_('Audio'))
    price = forms.IntegerField(help_text=_('Price'), min_value=0, max_value=999999)
    genre = forms.ModelChoiceField(queryset=Genre.objects.all())


class TextForm(forms.Form):
    name = forms.CharField(max_length=50, help_text=_('Text name'))
    description = forms.CharField(widget=forms.Textarea, max_length=1000, help_text=_('Description'))
    text = forms.CharField(widget=forms.Textarea, max_length=1000, help_text=_('Text'))
    price = forms.IntegerField(help_text=_('Price'), min_value=0, max_value=999999)
    style = forms.ModelChoiceField(queryset=Style.objects.all())
