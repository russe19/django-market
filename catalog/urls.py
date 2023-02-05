from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from catalog import views

urlpatterns = [
    path('covers/', views.CoverList.as_view(), name='covers'),
    path('musics/', views.MusicList.as_view(), name='musics'),
    path('texts/', views.TextList.as_view(), name='texts'),
    path('i18n', include('django.conf.urls.i18n')),
    path('upload_cover/', views.UploadCover.as_view(), name='upload_cover'),
    path('upload_music/', views.UploadMusic.as_view(), name='upload_music'),
    path('upload_text/', views.UploadText.as_view(), name='upload_text'),
    path('cover_detail<int:pk>/', views.CoverDetail.as_view(), name='cover_detail'),
    path('music_detail<int:pk>/', views.MusicDetail.as_view(), name='music_detail'),
    path('text_detail<int:pk>/', views.TextDetail.as_view(), name='text_detail'),
    path('covers_api/', views.CoverListApi.as_view(), name='cover_api'),
    path('musics_api/', views.MusicListApi.as_view(), name='music_api'),
    path('texts_api/', views.MusicTextListApi.as_view(), name='text_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
