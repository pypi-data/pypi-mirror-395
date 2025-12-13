#
# pip install beautifulsoup4 soupsieve
# pip install langdetect
#
from bs4 import BeautifulSoup as Soup
#from soupselect import select
import urllib
import requests

from nwebclient import runner as r

from urllib.parse import urlparse

def is_url(url):
    if '\n' in url or '://' not in url:
        return False
    try:
        result = urlparse(url)
        #return all([result.scheme, result.netloc])
        return True
    except ValueError:
        return False


def is_html(s):
    return '<' in s


def request(url, ssl_verify=True):
    res = requests.get(url, verify=ssl_verify)
    return res.text


class Website:
    url = None
    content = ""
    dom = None

    def __init__(self, url):
        self.dom = Soup('<div></div>', features="lxml")
        if is_url(url):
            self.url = url
            self.content = request(self.url)
        else:
            self.content = url
        self.loadContent()

    def loadContent(self):
        self.dom = Soup(self.content, features="lxml")

    def __repr__(self):
        return "Website("+str(self.url)+", content="+str(len(self.content))+" chars)"

    def __call__(self, selector):
        return self.q(selector)

    def __getitem__(self, name):
        if name == 'text':
            return self.text()
        else:
            return "Unkown Property Value"

    def q(self, selector='h1'):
        return self.dom.select(selector)

    def content_elem(self):
        res = None
        cnt = 0
        for elem in self.q('*'):
            nl = len(list(elem.children))
            if nl > cnt:
                res = elem
                cnt = nl
        return res

    def select_text(self, selector = 'h1'):
        node = self.dom.select_one(selector)
        return node.text

    def find_node_text(self, selector, text):
        for node in self.q(selector):
            if node.text == text:
                return node

    def links(self):
        res = []
        for link in self.dom.find_all('a'):
            res.append(link.get('href'))
        return res

    def text(self):
        return self.dom.get_text()

    def article_text(self):
        node = self.dom.select_one('article')
        return node.text

    def language(self):
        """ Returns en, de, ... """
        from langdetect import detect
        return detect(self.text())

    def toMap(self):
        # https://github.com/scrapinghub/extruct
        return {}

    def jsonld(self):
        return self.dom.find('script', {'type': 'application/ld+json'})

    def to_chunks(self, html=False):
        """ Zerlegt eine Webseite in Text-Chunks """
        # check for partiell site (also ohne html und head)
        # check for classes
        if html:
            return list(map(lambda t: str(t), self.content_elem().children))
        else:
            return list(map(lambda t: t.text, self.content_elem().children))


class WsExtractor(r.BaseJobExecutor):

    ws: Website

    def __init__(self):
        super().__init__()
        self.ws = None

    def execute_ws(self):
        pass

    def execute(self, data):
        if 'url' in data:
            self.ws = Website(data['url'])
        if 'text' in data:
            self.ws = Website(data['text'])
        if self.ws is not None:
            return self.execute_ws()
        return super().execute(data)


class TextExtract(WsExtractor):

    TAGS = [r.TAG.HTML_TRANSFORM]

    @staticmethod
    def text_of(html):
        obj = TextExtract()
        return obj(text=html)['text']

    def execute_ws(self):
        text = self.ws.text()
        return self.success('ok', value=text, text=text)


class LinkExtract(WsExtractor):

    TAGS = [r.TAG.HTML_EXTRACTOR]

    EVENT_LINK = 'on_link'

    def __init__(self, type='linkextract'):
        super().__init__()
        self.define_event(self.EVENT_LINK)
        self.type = type

    def execute_ws(self):
        links = self.ws.links()
        for link in links:
            self.emit_event(self.EVENT_LINK, link=link, value=link)
        return self.success('ok', items=links)

        
# https://spacy.io/models/de
# import spacy
#from spacy.lang.en.examples import sentences 
#nlp = spacy.load("en_core_web_sm")
#doc = nlp(sentences[0])
#print(doc.text)
#for token in doc:
#    print(token.text, token.pos_, token.dep_)
#    import spacy
#from spacy.lang.de.examples import sentences 
#
#nlp = spacy.load("de_core_news_sm")
#doc = nlp(sentences[0])
#print(doc.text)
#for token in doc:
#    print(token.text, token.pos_, token.dep_)