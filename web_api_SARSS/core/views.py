from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from .construtor_feed_rss import monta_feed,extrai_noticias
from .form_feed import FeedForm
from .models import User
from .models import Feed
from django.contrib import messages
["http://g1.globo.com/dynamo/educacao/rss2.xml", "http://g1.globo.com/dynamo/loterias/rss2.xml", "http://g1.globo.com/dynamo/politica/mensalao/rss2.xml"]


def buscar_feeds_usuario(user_id):
    usuario = User.objects.get(id=user_id)
    feeds = Feed.objects.filter(usuario=usuario)
    print(feeds)
    return feeds


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
            usuario=user
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