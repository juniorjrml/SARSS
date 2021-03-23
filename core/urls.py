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
    path('feed/visualizar/<int:id_feed>', views.visualizar_feed, name='visualiza_feed'),
    path('feed/<int:id_user>', views.visualizar_feed, name='visualiza_feed'),
]