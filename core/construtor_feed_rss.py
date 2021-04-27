import feedparser

# summary contem um doc html em string
def monta_feed(link):
    """

    :param link: link para o rss
    :return:  dict contendo {  title(titulo do feed),   subtitle( descrição do feed),  href(link para o rss), entries(contem as entradas do feed {'title', 'summary', 'link', 'tags'})
    """
    feed = {}
    campos_noticia = ['title', 'summary', 'link']
    NewsFeed = feedparser.parse(link)
    feed["title"] = NewsFeed['feed']['title']
    try:
        feed["subtitle"] = NewsFeed['feed']['subtitle']
    except KeyError:
        feed["subtitle"] = NewsFeed['feed']['title']

    feed["link"] = NewsFeed['href']
    feed["entries"] = []
    for entry in NewsFeed.entries:
        entrada = {}
        for campo in campos_noticia:
            entrada[campo] = entry[campo]


        feed["entries"].append(entrada)

    #print(NewsFeed.entries[0].keys())
    return feed

def extrai_noticias(link):
    NewsFeed = feedparser.parse(link)
    return NewsFeed.entries

if __name__ == '__main__':
    feed = monta_feed("http://www.bbc.co.uk/portuguese/index.xml")
    feed = monta_feed("https://www.gazetadopovo.com.br/feed/rss/mundo.xml")
    feed = monta_feed("http://g1.globo.com/dynamo/rss2.xml")
    feed = monta_feed("http://noticias.gov.br/noticias/rss")
    feed = monta_feed("https://www.cepea.esalq.usp.br/rss.php")
    feed = monta_feed("https://agencia.fapesp.br/rss/")
    feed = monta_feed("https://www.wired.com/feed/rss")
    feed = monta_feed("https://www.infomoney.com.br/feed")
    feed = monta_feed("http://noticias.r7.com/carreiras/feed.xml")
    entries = feed["entries"]
    #print(entries)