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
    feed["subtitle"] = NewsFeed['feed']['subtitle']
    feed["link"] = NewsFeed['href']
    feed["entries"] =[]
    print(NewsFeed.entries[0].keys())
    for entry in NewsFeed.entries:

        entrada = {}
        for campo in campos_noticia:
            entrada[campo] = entry[campo]

        feed["entries"].append(entrada)
    return feed

def extrai_noticias(link):
    NewsFeed = feedparser.parse(link)
    return NewsFeed.entries

if __name__ == '__main__':
    feed = monta_feed("http://g1.globo.com/dynamo/educacao/rss2.xml")
    entries = feed["entries"]
    print(entries[0].keys())