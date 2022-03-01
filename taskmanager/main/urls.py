from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('profile', views.profile, name='profile'),
    path('parsing', views.parsing, name='Парсинг серверов McOnly'),
    path('Найти игрока', views.find_player, name='Найти'),
    path('Онлайн сервера', views.online_server, name='OnlineAllServers'),
    path('Онлайн игрока', views.online_player, name='Онлайн игрока'),
    path('Онлайн одного сервера', views.see_online, name='OnlineOneServer'),
]
