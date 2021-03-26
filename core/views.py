from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
#from google.oauth2 import id_token
#from google.auth.transport import requests

from .construtor_feed_rss import monta_feed,extrai_noticias
from .form_feed import FeedForm
from .models import User
from .models import Feed
from django.contrib import messages

def busca_usuario(user_id):
    usuario = User.objects.all().get(id=user_id)
    if usuario != User.objects.none():
        return usuario
    else:
        return None

def busca_usuario_nome(user_name):
    usuario = User.objects.all().filter(username=user_name).first()
    if usuario != User.objects.none():
        return usuario
    else:
        return None


def buscar_feeds_usuario(user_id, autorizado=True):
    usuario = busca_usuario(user_id)
    if usuario:
        if autorizado:
            feeds = Feed.objects.all().filter(usuario=usuario.id)
        else:
            feeds = Feed.objects.all().filter(usuario=usuario.id).filter(privado=False)
        return feeds

    else:
        return None


@login_required(login_url='/login/')
def home(request):
    dados = {}
    dados["feeds"] = buscar_feeds_usuario(request.user.id)

    return render(request, 'home.html', dados)


@login_required(login_url='/login/')
def resgistra_feed(request):
    user = request.user
    form = FeedForm()
    dados = {'form': form}
    if request.GET:
        return render(request, 'register_feed.html', dados)
    elif request.POST:
        link = request.POST.get('link')
        user = User.objects.get(id=user.id)
        feed_retornado = monta_feed(link)
        Feed.objects.create(
            title=feed_retornado['title'],
            link=link,
            subtitle=feed_retornado['subtitle'],
            usuario=user,
            privado=True
        )

        return redirect("/")
    else:
        return render(request, 'register_feed.html', dados)


@login_required(login_url='/login/')
def delete_feed(request, id_feed):
    usuario = User.objects.get(id=request.user.id)
    try:
        feed = Feed.objects.get(id=id_feed)
        if usuario == feed.usuario:
            feed.delete()
        else:
            raise Http404()

    except:
        raise Http404()

    return redirect('/')

@login_required(login_url='/login/')
def feed_privado(request, id_feed):
    """

    :param request:
    :param id_feed:
    :return: inverte o valor contido no feed.privado se o request.user for o dono
    """
    usuario = request.user
    try:
        feed = Feed.objects.get(id=id_feed)
        if usuario == feed.usuario:
            feed.privado = not feed.privado
            feed.save()
        else:
            raise HttpResponseNotAllowed()

    except HttpResponseNotAllowed:
        return redirect('')

    return redirect('/')


@login_required(login_url='/login/')
def visualizar_feed(request, id_feed):
    usuario = User.objects.get(id=request.user.id)
    dados = {}
    try:
        feed = Feed.objects.get(id=id_feed)
        if usuario == feed.usuario:
            dados['noticias'] = extrai_noticias(feed.link)
        else:
            raise Http404()

    except:
        raise Http404()

    return render(request, 'visualizar_noticias.html', dados)


@login_required(login_url='/login/')
def visualizar_user(request, nickname):
    usuario = busca_usuario_nome(nickname)
    dados = {}
    if usuario:
        # caso o usuario exista
        autorizado = request.user.id == usuario.id
        feeds = buscar_feeds_usuario(usuario.id, autorizado=autorizado)
        if feeds:
            dados["feeds"] = feeds
        else:
            # Caso nao tenha feed
            raise Http404


    else:
        raise Http404
    return render(request, 'visualizar_usuario.html', dados)


def registra_usuario(request):
    dados = {}
    if request.GET:
        return render(request, 'register.html', dados)
    elif request.POST:
        user = User.objects.create_user(request.POST.get('username'),
                                                 request.POST.get('email'),
                                                 request.POST.get('password'))
        dados['form'] = user
        return redirect("/")
    else:
        return render(request, 'register.html', dados)


def submit_login(request):
    if request.POST:
        nome = request.POST.get('usuario')
        senha = request.POST.get('senha')
        usuario = authenticate(username=nome, password=senha)
        if usuario:
            login(request, usuario)
        else:
            messages.error(request, "Usuario ou Senha Invalidos")  # retorna em caso da autenticação falhar
    return redirect('/')


def login_usuario(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')