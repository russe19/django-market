from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from users import views

urlpatterns = [
      path('main/', views.Main.as_view(), name='main'),
      path('register/', views.RegisterView.as_view(), name='register'),
      path('login/', views.Login.as_view(), name='login'),
      path('logout/', views.Logout.as_view(), name='logout'),
      path('update/<int:pk>', views.Update.as_view(), name='update'),
      path('basket/', views.BasketView.as_view(), name='basket'),
      path('clear/', views.ClearBasket.as_view(), name='clear'),
      path('shop_detail/<int:off>/', views.ShowDetail.as_view(), name='shop_detail'),
      path('buy/', views.buy_view, name='buy'),
      path('history/', views.HistoryView.as_view(), name='history'),
      path('update_balance/', views.UpdateBalance.as_view(), name='update_balance'),
      path('users_api/', views.UsersApi.as_view(), name='user_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
