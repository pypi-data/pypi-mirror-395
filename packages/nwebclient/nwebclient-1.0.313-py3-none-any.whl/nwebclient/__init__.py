import base64

from typing import List, Optional

import requests
import json
import urllib.parse
import sys
import io
import os
import os.path
import traceback
from urllib.parse import urlparse
from collections.abc import Sequence

from nwebclient import util

#import .sdb as sdb

name = "nwebclient"


class NWebGroup:
    __client: "NWebClient" = None
    __data = None

    def __init__(self, client, data):
        self.__client = client
        self.__data = data
        self.__instances = []

    def __getitem__(self, item):
        return self.__data.get(item, None)

    def __iter__(self):
        return self.docs().__iter__()

    def __str__(self):
        t = self.__data.get('title', '-')
        return f'Group({t})'

    def client(self) -> "NWebClient":
        return self.__client

    def get(self, item, default):
        return self.__data.get(item, default)

    def id(self):
        return self.__data['group_id']

    def guid(self):
        return self.__data['guid']

    def title(self):
        return self.__data['title']

    def parent_id(self):
        return self.__data['parent']

    def println(self):
        for key, value in self.__data.iteritems():
            print(key + ": " + value)

    def asDict(self):
        return self.__data

    def docs(self) -> "list[NWebDoc]":
        """
        :rtype: [NWebDoc]
        """
        contents = self.__client.req('api/documents/' + str(self.__data['group_id']))
        j = json.loads(contents)
        items = j['items']
        #return j.items;
        return map(lambda x: NWebDoc(self.__client, x), items)

    def groups(self) -> "list[NWebGroup]":
        res = util.List()
        for g in self.__client.groups():
            if g.parent_id() == self.id():
                res.append(g)
        return res

    def create_doc(self, name, content, kind='markup', **data):
        return self.__client.createDoc(name, content, self.__data['group_id'], kind=kind, **data)

    def create_file(self, name, data):
        return self.__client.createFileDoc(name, self.guid(), data)

    def contains_name(self, name):
        for d in self.docs():
            if d.name() == name:
                return True
        return False

    def doc_by_name(self, name):
        for d in self.docs():
            if d.name() == name:
                return d
        return None

    def is_root(self):
        return str(self.__data['parent']) == '0'


class NWebDoc:
    __client = None
    __data = None

    def __init__(self, client, data):
        self.__client = client
        self.__data = data
        self.__meta = None
        if self.__client.verbose:
            print("Doc created.")

    def __repr__(self):
        name = self.__data['name']
        return f'<Doc {self.id()} Name: {name}>'

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return self.get_childs().__iter__()

    def __getitem__(self, item):
        if isinstance(item, tuple):
            return self.getMeta().get('meta.' + item[0] + "." + item[1], None)
        elif item in self.__data:
            return self.__data[item]
        elif self.is_kind('json'):
            j = json.loads(self.content())
            return j.get(item, None)
        else:
            return 'Doc None Item ' + str(item)

    def get(self, item, default=None):
        if item in self.__data:
            return self.__data.get(item, default)
        elif self.is_kind('json'):
            j = json.loads(self.content())
            return j.get(item, None)
        else:
            return default

    def __contains__(self, item):
        return item in self.__data or (self.is_kind('json') and self.__getitem__(item) is not None)

    def get_owner(self):
        return self.__client

    def title(self):
        return self.__data['title']

    def url(self):
        return self.__client.url() + 'd/' + str(self.id()) + '/'

    def name(self):
        return self.__data['name']

    def kind(self):
        return self.__data['kind']

    def content(self):
        return self.__data['content']

    def content_text(self):
        if self.is_kind_in('markup'):
            from nwebclient import ws
            return ws.TextExtract.text_of(self.__data['content'])
        # TODO markdown?
        return self.__data['content']

    def text_content(self):
        """ Liefert eine Testuelle Darstellung des Dokumentes zurueck"""
        # TODO OCR in self.is_image()
        return self.content()

    def guid(self):
        return self.__data['guid']

    def is_image(self):
        return self.__data['kind'] == 'image'

    def is_kind(self, kind):
        return self.__data['kind'] == kind

    def is_kind_in(self, *args):
        return self.__data['kind'] in args

    def printInfo(self):
        s = "Doc-"+self.kind()+"(id:"+self.id()+", title: "+self.title()
        if self.kind()=="image":
            s+=" thumb: " + self.__data['thumbnail']['nn'] + " "
        s+=")"
        print(s)

    def id(self):
        return self.__data['document_id']

    def tags(self):
        return self.__data.get('tags', [])

    def println(self):
        print(self.__data)
        #for key, value in self.__data.iteritems():
        #    print key + ": " + value

    def downloadThumbnail(self, file, size='nn'):
        path = 'image/'+str(self.id())+'/thumbnail/'+size+'/'+str(self.id())+'.jpg'
        self.__client.reqToFile(path, file)
        return 0

    def getThumbnail(self, size='nn'):
        path = 'image/'+str(self.id())+'/thumbnail/'+size+'/'+str(self.id())+'.jpg'
        return self.__client.reqToBin(path)

    def get_thumbnail_url(self, size='m'):
        path = 'image/' + str(self.id()) + '/thumbnail/' + size + '/' + str(self.id()) + '.jpg'
        return self.__client.req_url(path)

    def as_image(self, size='cs'):
        from PIL import Image
        #f = 'current.jpg'
        #self.downloadThumbnail(f, 'cs')
        return Image.open(io.BytesIO(self.getThumbnail(size)))

    def as_b64_image(self, size='orginal'):
        return base64.b64encode(self.getThumbnail(size)).decode('utf-8')

    def save(self, file):
        self.__client.reqToFile('/w/d/'+str(self.id())+'/download', file)

    def setContent(self, content):
        self.__data['content'] = content
        self.__client.req('api/document/'+str(self.__data['document_id']), {
            'action': 'update',
            'content': content
        })

    def setTitle(self, value):
        self.__data['title'] = value
        self.__client.req('api/document/'+str(self.__data['document_id']), {
            'action': 'update',
            'title': value
        })

    def setKind(self, value):
        self.__data['title'] = value
        self.__client.req('api/document/'+str(self.__data['document_id']), {
            'action': 'update',
            'kind': value
        })

    def setMetaValue(self, ns, name, value):
        if isinstance(value, dict):
            value = json.dumps(value)
        data = {'ns': ns, 'name': name, 'value': str(value)}
        #print("DATA: " + str(data))
        return self.__client.req('w/api/doc/'+str(self.__data['document_id'])+'/meta', data)

    def getMeta(self):
        """
            "meta.trello.id": "66b4bfe481322b971",
            "meta.trello.board_doc": "12091",
            "meta.trello.data
        """
        if self.__meta is None:
            self.__meta = json.loads(self.__client.reqGet('w/api/doc/'+str(self.__data['document_id'])+'/meta'))
        return self.__meta

    def to_dict(self) -> dict:
        return {
            'document_id': self.id(),
            'guid': self.guid(),
            'name': self.name(),
            'title': self.title()
        }

    def get_childs(self) -> list:
        """ Liefert den Bucket Inhalt zurueck """
        return map(lambda guid: self.__client.doc(guid), self.__data.get('bucket', []))

    def matches(self, q):
        return q in str(self.content()) or q in self.tags() or q in str(self.title())


class NWebClient(object):
    """
       /w/api

    """
    
    __url = "" 
    __user = ""
    __pass = ""
    __cfg = {}
    __last_url = '{none}'
    ssl_verify = False
    verbose = False

    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and args[0] == 'npy':
            from nweb import client
            return super().__new__(client.InternalClient)
        return super().__new__(cls)

    def __init__(self, url=None, username='', password=''):
        """
          Anstatt url kann auch ein Pfad zur einer JSON-Datei, die die Schluessel enthaelt, angegeben werden. 
          url https://bsnx.net/4.0/

          oder ein key für die nweb.json
        """
        self.__groups = None
        if url is None:
            if os.path.isfile('nweb.json'):
                url = 'nweb.json'
            elif os.path.isfile('/etc/nweb.json'):
                url = '/etc/nweb.json'
            elif os.getenv('NWEB_URL') is not None and os.getenv('NWEB_USER') is not None and os.getenv('NWEB_PASS') is not None:
                url = os.getenv('NWEB_URL')
                username = os.getenv('NWEB_USER')
                password = os.getenv('NWEB_PASS')
        if url[0] == '/' or url.endswith('nweb.json'):
            self.__cfg = json.loads(self.file_get_contents(url))
            self.__url = self.__cfg['url']
            self.__user = self.__cfg['username']
            self.__pass = self.__cfg['password']
        elif username == '' and password == '':
            self.init_from_config_name(url)
        else:
            self.__url = url
            self.__user = username
            self.__pass = password

    def init_from_config_name(self, name):
        if os.path.isfile('nweb.json'):
            self.__cfg = json.loads(NWebClient.file_get_contents('nweb.json'))
        elif os.path.isfile('/etc/nweb.json'):
            self.__cfg = json.loads(NWebClient.file_get_contents('/etc/nweb.json'))
        cfg = self.__cfg
        if name in cfg:
            cfg = cfg[name]
        self.__url = cfg['url']
        self.__user = cfg['username']
        self.__pass = cfg['password']

    @staticmethod
    def list():
        if os.path.isfile('nweb.json'):
            cfg = json.loads(NWebClient.file_get_contents('nweb.json'))
        elif os.path.isfile('/etc/nweb.json'):
            cfg = json.loads(NWebClient.file_get_contents('/etc/nweb.json'))
        res = []
        for key in cfg.keys():
            if isinstance(cfg[key], dict) and 'url' in cfg[key] and 'username' in cfg[key] and 'password' in cfg[key]:
                res.append(key)
        return res

    def __call__(self, q):
        return "NWebClient TODO"

    def __getitem__(self, key):
        if key in self.__cfg:
            return self.__cfg[key]
        else:
            s = self.setting(key)
            if s is not None:
                return s
            else:
                return "Non Existing"

    def __repr__(self):
        return f'<NWebClient {self.__url} User: {self.__user} docs() >'

    def url(self):
        return self.__url

    def domain(self):
        return urlparse(self.__url).netloc

    def is_setup(self):
        return self.__user is not None and self.__user != ""

    def v(self, msg):
        if self.verbose:
            print("[NWebClient]" + str(msg))

    @staticmethod
    def file_get_contents(filename):
        with open(filename) as f:
            return f.read()

    def _appendGet(self, url, name, value):
        v = name + '=' + urllib.parse.quote(value)
        if '?' in url:
            return url + '&' + v
        else:
            return url + '?' + v

    def reqToFile(self, path, name):
        url = self.__url + path
        url = self._appendGet(url, 'username', self.__user)
        url = self._appendGet(url, 'password', self.__pass)
        r = requests.get(url, stream=True, verify=self.ssl_verify) 
        if r.status_code == 200:
            with open(name, 'wb') as f:
                for chunk in r:
                    f.write(chunk)

    def reqToBin(self, path):
        url = self.__url + path
        url = self._appendGet(url, 'username', self.__user)
        url = self._appendGet(url, 'password', self.__pass)
        r = requests.get(url, verify=self.ssl_verify)
        if r.status_code == 200:
            return r.content
        return None

    def req_url(self, path, params={}):
        if self.__user != "":
            params["username"] = self.__user
            params["password"] = self.__pass
        url = self.__url+path
        return util.append_query(url, params)

    def reqGet(self, path, params={}):
        if self.__user != "":
            params["username"] = self.__user
            params["password"] = self.__pass
        url = self.__url+path
        self.v("GET " + url)
        res = requests.get(url, data=params, verify=self.ssl_verify)
        return res.text

    def req(self, path, params={}):
        if self.__user != "":
            params["username"] = self.__user
            params["password"] = self.__pass
        url = self.__url+path
        self.__last_url = url
        self.v("POST " + url)
        res = requests.post(url, data=params, verify=self.ssl_verify)
        return res.text

    def reqJson(self, path, params={}):
        resp = self.req(path, params)
        try:
            return json.loads(resp)
        except Exception as e:
            print("Invalid JSON Response:")
            print(resp)
            raise e


    def upload(self, path, params={}, name='file', data=None):
        """ open('file.txt','rb') """
        url = self.__url+path
        params['response'] = 'json'
        if 'kind' not in params:
            params['kind'] = 'binary'
        if self.__user != "":
            params["username"] = self.__user
            params["password"] = self.__pass
        files = {name: data}
        self.v("UPLOAD " + url)
        r = requests.post(url, files=files, data=params, verify=self.ssl_verify)
        return json.loads(r.text)

    def doc(self, id) -> NWebDoc:
        response = self.req("api/document/"+str(id), {format: "json"})
        #print(response)
        data = json.loads(response)
        return NWebDoc(self, data)

    def exists(self, id):
        try:
            str(self.doc(id))
            return True
        except:
            return False

    def images(self, q=''):
        if q != '':
            q += '&'
        q += 'kind=image'
        return self.docs(q)

    def docs(self, q: str = '') -> List[NWebDoc]:
        """ 
          Syntax: q e.g. kind=image
              no_meta=ns.name Nur Dokumente die dieses Meta-Feld nicht haben
              tag
              start, limit
              group_id
              user_id
              from_id  Ab einer document_id weitere Document anzeigen
              orderby
              asc=1
          API: w/api/docs
        
        """
        ja = self.req('w/api/docs?'+q)
        try:
            items = json.loads(ja)
            return list(map(lambda x: NWebDoc(self, x), items))
        except Exception as error:
            print("URL: " + self.__last_url)
            print("Response:")
            print(ja)
            raise

    def group(self, id): 
        data = json.loads(self.req("api/group/"+str(id), {format: "json"}))
        return NWebGroup(self, data)

    def groups(self) -> "list[NWebGroup]":
        if self.__groups is None:
            items = self.reqJson('w/api/groups')
            self.__groups = list(map(lambda g: NWebGroup(self, g), items))
        return self.__groups


    def getOrCreateGroup(self, guid, title):
        return "TODO"
    def getOrCreateDoc(self, group_id, name):
        g = self.group(group_id)
        if g.contains_name(name):
            return g.doc_by_name(name)
        else:
            return self.createDoc(name, '', group_id)
    def createDoc(self, name, content, group_id, kind='markup', **data) -> Optional[NWebDoc]:
        """ Return: JSON """
        res = self.req("w/group/"+str(group_id)+"/create", {
            "title": name,
            "content": content,
            "kind": kind,
            "response": "json",
            "guid": data.get('guid', util.guid())
        })
        print(res)
        j = json.loads(res)
        if 'document_id' in j:
            return self.doc(j['document_id'])
        else:
            print("Fail to Create Doc. " + res)
            return None
    def createFileDoc(self, name, group_id, data):
        """
            data=open('file', 'rb')
        """
        res = self.upload("w/group/"+str(group_id)+"/create", {
            "title": name,
            "kind": 'binary',
            "response": "json"
        }, 'file', data)
        return self.doc(res['document_id'])

    def deleteDoc(self, id):
        return self.req('w/d/'+str(id)+'/delete', {'confirm': 1})

    def downloadImages(self, limit=1000, tag=None, size=None):
        # https://bsnx.net/4.0/w/api/docs?tag=Untertage
        q = 'kind=image&limit='+str(limit)
        if not tag is None:
            q = q + "&tag=" + str(tag)
        docs = self.docs(q)
        for doc in docs:
            if size is None:
                self.reqToFile('image/'+str(doc.id())+'/orginal/web/'+str(doc.id())+'.jpg', str(doc.id())+ '.jpg')
            else:
                self.reqToFile('image/'+str(doc.id())+'/thumbnail/'+size+'/t.jpg', str(doc.id())+ '.jpg')
            print("Download Image: " + str(doc.id()))
    def downloadImageDataset(self, tags=[], limit=500):
        for tag in tags:
            print("Processing Tag: " + str(tag))
            folder = tag.replace(' ', '_')
            os.mkdir(folder)
            os.chdir(folder)
            self.downloadImages(limit=limit, tag=tag, size='cs')
            os.chdir('..')
        print("Done.");
    def imagesUrls(self, tag=None, limit=1000, size='cs', file=None):
        """ Erstellt eine Liste mit Image-URLs """
        res = []
        q = 'kind=image&limit='+str(limit)
        if not tag is None:
            q = q + "&tag=" + str(tag)
        docs = self.docs(q)
        for doc in docs:
            url = self.__url + 'image/'+str(doc.id())+'/thumbnail/'+size+'/'+str(doc.id())+'/t.jpg'
            url = url + '?username=' + self.__user + "&password=" + self.__pass
            res.append(url)
        if not file is None:
            with open(file, "w") as f:
                for item in res:
                    f.write("%s\n" % item)
        return res

    def mapDocMeta(self, meta_ns, meta_name, filterArgs='kind=image', limit=1000, update=True, mapFunction=None):
        """

         :param filterArgs: fuer docs(q)
        """
        meta = meta_ns + '.' + meta_name
        structure = {}
        q = 'no_meta='+meta+'&'+'limit='+str(limit)+'&'+filterArgs
        docs = self.docs(q)
        i = 0
        for doc in docs:
            print("Processing: " + str(doc) + "   i:" + str(i))
            try:
                result = mapFunction(doc, self)
                if update:
                    print(doc.setMetaValue(meta_ns, meta_name, result))
                print("Value: " + str(result))
                structure[doc.guid()] = {
                  meta_ns+'.'+meta_name: result
                }
            except Exception as e:
                print("[NWebClient] Error: " + str(e))
                print(traceback.format_exc())
                structure[doc.guid()] = {
                    "error": str(e)
                }
            i = i + 1
        print("Count: "+str(i))    
        print("Done.")
        return structure

    def sql(self, sql):
        res = self.reqJson('api/sql/select', {'sql':sql, 'format': 'json'})
        return res['items']

    def me(self):
        """

        {"title":"Admin",
         "id":1,
         "name":"root",
         "doc_ids":["16118","16119",...,"17643"],
         "group_names":["admin"]}

        """
        user_data = self.reqJson('w/api/me', {})
        return user_data

    def tests(self):
        try:
            return self.reqJson('../test/api', {'tests': []})
        except:
            return {'tests': []}

    def log(self, message: str = 'ping'):
        """ Tabelle: er__messages php:log_message """
        return self.req('w/api/log', {'message': message})

    def setting(self, key, default=None):
        v = self.req('w/api/setting', {'key': key})
        if v == '':
            return default
        return v

    def setting_set(self, key, value):
        return self.req('w/api/setting', {'key': key, 'value': value})

    def metrics_get_value(self, name):
        return self.req(f'../metrics/w/m/{name}/value').strip()


def metric_val(baseUrl, metricName, val):
    """ baseUrl: string = e.g. https://bsnx.net/metric-endpoint """
    requests.get(url=baseUrl, params={'metric': metricName, 'val': val})
    
def download(url, filename, ssl_verify=True):
    r = requests.get(url, stream=True, verify=ssl_verify) 
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)


def main():
    print("nx-c")
    c = NWebClient(None)
    args = util.Args()
    print(sys.argv)
    print(str(c.docs()))


if __name__ == '__main__': # nx-c vom python-package bereitgestellt
    main()
