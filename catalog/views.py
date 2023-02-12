import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView

from catalog.forms import CoverForm, MusicForm, TextForm
from catalog.models import (Cover, Genre, Music, MusicText, Offer, Style,
                            TypeOffer)
from catalog.serializers import (CoverSerializer, MusicSerializer,
                                 MusicTextSerializer)

logger_login = logging.getLogger('login_logout')
logger_balance = logging.getLogger('balance')


class CoverList(ListView):
    model = Cover
    template_name = 'catalog/cover_list.html'
    paginate_by = 12

    def get_queryset(self):
        return super().get_queryset().select_related('offer').select_related('offer__user').\
            filter(offer__user=None).filter(offer__date=None).order_by('-id')


class MusicList(ListView):
    model = Music
    template_name = 'catalog/music_list.html'
    paginate_by = 12

    def get_queryset(self):
        return super().get_queryset().select_related('offer').select_related('offer__user').\
            filter(offer__user=None).filter(offer__date=None).order_by('-id')


class TextList(ListView):
    model = MusicText
    template_name = 'catalog/text_list.html'
    paginate_by = 12

    def get_queryset(self):
        return super().get_queryset().select_related('offer').select_related('offer__user').\
            filter(offer__user=None).filter(offer__date=None).order_by('-id')


class CoverDetail(DetailView):
    model = Cover
    template_name = 'catalog/cover_detail.html'
    context_object_name = 'cover'


class MusicDetail(DetailView):
    model = Music
    template_name = 'catalog/music_detail.html'
    context_object_name = 'music'


class TextDetail(DetailView):
    model = MusicText
    template_name = 'catalog/text_detail.html'
    context_object_name = 'text'


class UploadCover(LoginRequiredMixin, FormView):
    form_class = CoverForm
    template_name = 'catalog/cover_create.html'
    success_url = '/main'

    def form_valid(self, form):
        if not TypeOffer.objects.filter(name='Image').exists():
            TypeOffer.objects.create(name='Image')
        offer = Offer.objects.create(seller=self.request.user,
                                     name=self.request.POST['name'],
                                     description=self.request.POST['description'],
                                     price=self.request.POST['price'],
                                     type=TypeOffer.objects.get(name='Image'))

        entry_image = Cover.objects.create(offer=offer, image=self.request.FILES['images'])
        entry_image.save()
        return redirect('main')


class UploadMusic(LoginRequiredMixin, FormView):
    form_class = MusicForm
    template_name = 'catalog/music_create.html'
    success_url = '/main'

    def form_valid(self, form):
        if not TypeOffer.objects.filter(name='Music').exists():
            TypeOffer.objects.create(name='Music')
        offer = Offer.objects.create(seller=self.request.user,
                                     name=self.request.POST['name'],
                                     description=self.request.POST['description'],
                                     price=self.request.POST['price'],
                                     type=TypeOffer.objects.get(name='Music'))
        music_file = Music.objects.create(offer=offer, sound=self.request.FILES['sound'],
                                          genre=Genre.objects.get(id=self.request.POST['genre']))
        music_file.save()
        return redirect('main')


class UploadText(LoginRequiredMixin, FormView):
    form_class = TextForm
    template_name = 'catalog/text_create.html'
    success_url = '/main'

    def form_valid(self, form):
        if not TypeOffer.objects.filter(name='Text').exists():
            TypeOffer.objects.create(name='Text')
        offer = Offer.objects.create(seller=self.request.user,
                                     name=self.request.POST['name'],
                                     description=self.request.POST['description'],
                                     price=self.request.POST['price'],
                                     type=TypeOffer.objects.get(name='Text'))
        text_offer = MusicText.objects.create(offer=offer, text=self.request.POST['text'],
                                              style=Style.objects.get(id=self.request.POST['style']))
        text_offer.save()
        return redirect('main')


class CoverListApi(ListAPIView, CreateAPIView, GenericAPIView):
    serializer_class = CoverSerializer

    def get_queryset(self):
        queryset = Cover.objects.select_related('offer', 'offer__user', 'offer__seller').all()
        name = self.request.query_params.get('offer__name')
        user = self.request.query_params.get('offer__user')
        seller = self.request.query_params.get('offer__seller')
        if name:
            queryset = queryset.select_related('offer').filter(offer__name=name)
        if user:
            queryset = queryset.select_related('offer').select_related('offer__user').filter(offer__user=user)
        if seller:
            queryset = queryset.select_related('offer').select_related('offer__seller').filter(offer__seller=seller)
        return queryset

    def get(self, request):
        return self.list(request)


class MusicListApi(ListAPIView, CreateAPIView, GenericAPIView):
    serializer_class = MusicSerializer

    def get_queryset(self):
        queryset = Music.objects.select_related('offer', 'offer__user', 'offer__seller').all()
        name = self.request.query_params.get('offer__name')
        user = self.request.query_params.get('offer__user')
        seller = self.request.query_params.get('offer__seller')
        if name:
            queryset = queryset.select_related('offer').filter(offer__name=name)
        if user:
            queryset = queryset.select_related('offer').select_related('offer__user').filter(offer__user=user)
        if seller:
            queryset = queryset.select_related('offer').select_related('offer__seller').filter(offer__seller=seller)
        return queryset

    def get(self, request):
        return self.list(request)


class MusicTextListApi(ListAPIView, CreateAPIView, GenericAPIView):
    serializer_class = MusicTextSerializer

    def get_queryset(self):
        queryset = MusicText.objects.select_related('offer', 'offer__user', 'offer__seller').all()
        name = self.request.query_params.get('offer__name')
        user = self.request.query_params.get('offer__user')
        seller = self.request.query_params.get('offer__seller')
        if name:
            queryset = queryset.select_related('offer').filter(offer__name=name)
        if user:
            queryset = queryset.select_related('offer').select_related('offer__user').filter(offer__user=user)
        if seller:
            queryset = queryset.select_related('offer').select_related('offer__seller').filter(offer__seller=seller)
        return queryset

    def get(self, request):
        return self.list(request)
