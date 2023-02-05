import datetime
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.db.models import F, Sum
from django.shortcuts import HttpResponse, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, View
from django.views.generic.edit import FormView
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView

from catalog.models import Offer
from users.forms import (BalanceForm, HistoryForm, RegisterForm,
                         RegisterFormUpdate)
from users.models import Profile, ProfileImage
from users.serializers import ProfileSerializer

logger_login = logging.getLogger('login_logout')
logger_balance = logging.getLogger('balance')


class Main(ListView):
    model = Offer
    template_name = 'users/main.html'
    context_object_name = 'entres'


class Login(LoginView):
    """Страница входа на сайт"""
    template_name = 'users/login.html'

    def form_valid(self, form):
        logger_login.info(f'Пользователь {self.request.POST.get("username")} успешно авторизировался')
        return super().form_valid(form)

    def form_invalid(self, form):
        logger_login.error('Не удалось войти на сайт')
        return super().form_valid(form)


class Logout(LogoutView):
    """Страница выхода с сайта"""
    template_name = 'users/logout.html'
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        logger_login.info(f'Пользователь {self.request.user} успешно вышел')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(FormView):
    """Страница регистрации"""
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save()
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.email = form.cleaned_data.get('email')
        user.save()
        balance = form.cleaned_data.get('balance')
        number = form.cleaned_data.get('number')
        telegram = form.cleaned_data.get('telegram')
        Profile.objects.create(user=user, balance=balance, number=number, telegram=telegram)
        print(self.request.FILES['image'])
        ProfileImage.objects.create(profile=user.profile, image=self.request.FILES['image'])
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect('main')


class Update(UserPassesTestMixin, UpdateView):
    """Обновление информации о пользователе"""
    model = User
    template_name = 'users/update.html'
    success_url = reverse_lazy('main')
    fields = ['first_name', 'last_name', 'email']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = RegisterFormUpdate(instance=self.object.profile)
        return context

    def test_func(self):
        return self.request.user.id == self.kwargs['pk']

    def form_valid(self, form):
        profile_model = Profile.objects.get(user_id=self.object.id)
        profile_model.telegram = self.request.POST['telegram']
        profile_model.number = self.request.POST['number']
        profile_model.save()
        return super().form_valid(form)


class ShowDetail(LoginRequiredMixin, View):
    http_method_names = ['get', 'post']

    def post(self, request, *args, **kwargs):
        offer = Offer.objects.get(id=request.POST.get('off'))
        offer.user = request.user
        logger_balance.info(f'Пользователь {request.user} добавил в корзину {offer}')
        offer.save()
        return redirect('basket')


class ClearBasket(LoginRequiredMixin, View):
    http_method_names = ['get', 'post']

    def post(self, request):
        Offer.objects.filter(user=request.user).filter(date=None).update(user=None)
        logger_balance.info(f'Пользователь {request.user} очистил корзину')
        return redirect('basket')


def buy_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            with transaction.atomic():
                offer = Offer.objects.filter(date=None).filter(user=request.user).aggregate(sum=Sum('price'))['sum']
                if (offer is not None) and (request.user.profile.balance > offer):
                    request.user.profile.balance -= offer
                    logger_balance.info(f'Пользователь {request.user} совершил покупку на сумму {offer} рублей')
                elif offer is not None:
                    logger_balance.error(f'Пользователю {request.user} нехватает средств для покупки')
                    return HttpResponse('<p>На вашем счете недостаточно средств</p> <a href="/basket/">Корзина</a>')
                request.user.profile.save()
                Offer.objects.filter(user=request.user).update(date=datetime.datetime.now().date())
            return redirect('basket')


class BasketView(LoginRequiredMixin, ListView):
    template_name = 'users/basket.html'
    context_object_name = 'offers'

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user).filter(date=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['summ'] = Offer.objects.filter(user=self.request.user).filter(date=None).aggregate(sum=Sum('price'))['sum']
        context['form'] = HistoryForm()
        return context


class HistoryView(LoginRequiredMixin, ListView):
    model = Offer
    template_name = 'users/history.html'
    context_object_name = 'offers'
    paginate_by = 10

    def get_queryset(self):
        self.day = self.request.GET.get('day')
        if not self.day:
            self.day = 7
        offers = Offer.objects.all().\
            filter(date__gte=(datetime.datetime.now().date() - datetime.timedelta(days=int(self.day)))).\
            annotate(ids=F('id')).order_by('-date')
        return offers


class UpdateBalance(LoginRequiredMixin, FormView):
    form_class = BalanceForm
    template_name = 'users/update_balance.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        profile_model = Profile.objects.get(user_id=self.request.user.id)
        profile_model.balance += int(self.request.POST['count'])
        logger_balance.info(f'Пользователь {self.request.user} пополнил баланс на сумму {self.request.POST["count"]}')
        profile_model.save()
        return super().form_valid(form)


class UsersApi(ListAPIView, CreateAPIView, GenericAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.all()
        user_name = self.request.query_params.get('user__username')
        number = self.request.query_params.get('number')
        if user_name:
            queryset = queryset.filter(user__username=user_name)
        if number:
            queryset = queryset.filter(number=number)
        return queryset

    def get(self, request):
        return self.list(request)
