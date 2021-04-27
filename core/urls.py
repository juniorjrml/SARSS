from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registra_usuario, name='register'),
    path('login/', views.login_usuario, name='login'),
    path('login/submit', views.submit_login, name='submit_login'),
    path('logout/', views.logout_user, name='logout'),
    path('logout/', views.logout_user, name='logout'),
    path('feed/register', views.resgistra_feed, name='register_feed'),
    path('feed/delete/<int:id_feed>', views.delete_feed, name='delete_feed'),
    path('feed/altera_privacidade/<int:id_feed>', views.feed_privado, name='flip_feed_privado'),
    path('feed/tag/visualizar/', views.visualizar_tags, name='visualiza_tags'),
    path('feed/tag/pesquisar/<busca>', views.pesquisar_tags, name='visualiza_tags'),
    path('feed/visualizar/<int:id_feed>', views.visualizar_feed, name='visualiza_feed'),
    path('feed/vincular_tag/<int:id_feed>/<int:id_tag>', views.vincular_tag, name='vincular_tag'),
    path('feed/remover_vinculo_tag/<int:id_feed>/<int:id_tag>', views.remover_vinculo_tag, name='remover_tag'),
    path('feed/vincular_tags/<int:id_feed>', views.vincular_tags, name='vincular_tags'),
    path('feed/<nickname>', views.visualizar_user, name='visualiza_user'),
    path('tag/register', views.resgistra_tag, name='register_tag')
]