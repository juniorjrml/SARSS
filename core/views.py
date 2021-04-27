from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .construtor_feed_rss import monta_feed, extrai_noticias
from .form_feed import FeedForm
from .form_tag import tagForm
from .models import User, Tag
from .models import Feed
from django.contrib import messages

abcdario = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def pesquisa_tags(tag):
    tags = Tag.objects.all().filter(title__icontains=tag)
    if tags != Tag.objects.none():
        return tags
    return None


def pesquisa_tags_iniciadas_em(inicio):
    tags = Tag.objects.all().filter(title__istartswith=inicio)
    if tags != Tag.objects.none():
        return tags
    return None


def excluir_tags_da_pesquisa_iniciadas_em(inicio, selecao):
     sel = selecao.exclude(title__istartswith=inicio)
     if sel != Tag.objects.none():
         return sel
     return None


def buscar_tags():
    tags = Tag.objects.all()
    if tags != Tag.objects.none():
        return tags
    return None


def busca_tag(tag_id):
    tag = Tag.objects.all().get(id=tag_id)
    if tag != Tag.objects.none():
        return tag
    else:
        return None


def busca_feed(feed_id):
    feed = Feed.objects.all().get(id=feed_id)
    if feed != Feed.objects.none():
        return feed
    else:
        return None


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


@login_required(login_url='/login/')
def home(request):
    dados = {"feeds": buscar_feeds_usuario(request.user.id)}

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
def resgistra_tag(request):
    user = request.user
    form = tagForm()
    dados = {'form': form, 'tags': Tag.objects.all()}

    if user.is_staff:
        if request.GET:
            return render(request, 'register_tag.html', dados)
        elif request.POST:
            title = request.POST.get('title')
            tag = Tag.objects.create(title=title)
            tag.save()

            return redirect("/")
        else:
            return render(request, 'register_feed.html', dados)
    return redirect("/")


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
        feed = Feed.objects.all().get(id=id_feed)
        if usuario == feed.usuario:
            feed.privado = not feed.privado
            feed.save()
    except:
        pass

    return redirect('/')


@login_required(login_url='/login/')
def visualizar_feed(request, id_feed):
    usuario = request.user
    dados = {}
    feed = busca_feed(id_feed)
    if feed:
        if usuario == feed.usuario or not feed.privado:
            dados['noticias'] = extrai_noticias(feed.link)
            dados['feed'] = feed

    return render(request, 'visualizar_noticias.html', dados)


@login_required(login_url='/login/')
def vincular_tags(request, id_feed):
    usuario = request.user
    dados = {}
    feed = busca_feed(id_feed)
    if feed:
        if usuario == feed.usuario:
            dados['feed'] = feed
            dados['categorias'] = {}
            tags_complementar = Tag.objects.all()
            for letra in abcdario:
                tags = pesquisa_tags_iniciadas_em(letra)
                if tags:
                    dados['categorias'][letra] = tags
                    tags_complementar = excluir_tags_da_pesquisa_iniciadas_em(letra, tags_complementar)

            if tags_complementar:
                dados['categorias']["Outros"] = tags_complementar

    return render(request, 'vincular_tags.html', dados)


@login_required(login_url='/login/')
def vincular_tag(request, id_feed, id_tag):
    usuario = request.user
    feed = busca_feed(id_feed)
    tag = busca_tag(id_tag)
    if feed and tag:
        if feed.usuario == usuario:
            if tag not in feed.tags.all():
                feed.tags.add(tag)
        return redirect("/feed/vincular_tags/"+str(id_feed))
    else:
        raise Http404

    return render(request, 'vincular_tags.html')

@login_required(login_url='/login/')
def remover_vinculo_tag(request, id_feed, id_tag):
    usuario = request.user
    feed = busca_feed(id_feed)
    tag = busca_tag(id_tag)
    if feed and tag:
        if feed.usuario == usuario:
            if tag in feed.tags.all():
                feed.tags.remove(tag)
        return redirect("/")
    else:
        raise Http404

    return render(request, 'vincular_tags.html')


def visualizar_tags(request):
    dados = {}
    tags = buscar_tags()
    dados['tags'] = tags
    return render(request, 'visualizar_tags.html', dados)

def pesquisar_tags(request, busca: str):
    tags = pesquisa_tags(busca)
    if tags:
        dados = {'tags': tags}
    else:
        dados = {}
    return render(request, 'visualizar_tags.html', dados)

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
