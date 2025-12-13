
import time
import json
import typing
import uuid
import traceback
from contextlib import contextmanager
from threading import Thread
from urllib.parse import urlparse
from urllib.parse import parse_qs
from functools import wraps


class PeriodedThread(Thread):

    def __init__(self, op, time_s=600, start=True):
        super().__init__(target=self.thread_main)
        self.op = op
        if time_s is None:
            time_s = 600
        self.time_s = time_s
        self.active = True
        if start:
            self.start()

    def stop(self):
        self.active = False

    def thread_main(self):
        while self.active:
            time.sleep(self.time_s)
            try:
                self.op()
            except Exception as e:
                print("[periodic] Exception occured. " + str(e))

    def __repr__(self):
        return "PeriodedThread(" + str(self.time_s) + ")"

    def __str__(self):
        return "PeriodedThread(" + str(self.time_s) + ")"


class Base:
    """
        Basisklasse
    """
    __childs = []
    __owner = None

    def __init__(self):
        self.__childs = []
        self.__owner = None

    def owner(self):
        return self.__owner

    def addChild(self, child):
        if child is None:
            return None
        self.__childs.append(child)
        if isinstance(child, Base):
            child.__owner = self
            child.onOwnerChanged(self)
        return child

    def onOwnerChanged(self, newOnwer):
        pass

    def childs(self):
        return self.__childs

    def isRoot(self):
        return self.__owner is None

    def getParents(self):
        res = []        
        current = self.__owner
        while not current is None:
            res.append(current)
            current = current.__owner
        return res

    def getRoot(self):     
        current = self
        while not current.__owner is None:
            current = current.__owner
        return current

    def getParentClass(self, cls):
        for p in self.getParents():
            if isinstance(p, cls):
                return p
        return None

    def onParentClass(self, cls, action, fail_result="Error: ParentClass not found."):
        p = self.getParentClass(cls)
        if not p is None:
            return action(p)
        else:
            print("Parents: " + str(self.getParents()))
            return fail_result

    def className(self):
        a = self
        return "{0}.{1}".format(a.__class__.__module__, a.__class__.__name__)

    def prn(self, msg):
        print(msg)

    def debug(self, msg):
        self.prn("DEBUG: [{0}] {1}".format(self.__class__.__name__, str(msg)))

    def info(self, msg):
        self.prn("INFO: [{0}] {1}".format(self.__class__.__name__, str(msg)))

    def error(self, msg, print_traceback=False):
        self.prn("ERROR: [{0}] {1}".format(self.__class__.__name__, str(msg)))
        if print_traceback and isinstance(msg, Exception):
            self.prn(''.join(traceback.format_tb(msg.__traceback__)))

    def one_line_str(self):
        res = self.className()
        res = res + ' ' + str(getattr(self, 'name', ''))
        return res

    def printTree(self, indent=1, p = print):
        if indent > 10:
            return
        try:
            p(' '.rjust(indent*2, ' ') + self.one_line_str())
            for c in self.__childs:
                if isinstance(c, Base):
                    c.printTree(indent+1, p=p)
                else:
                    p(' '.rjust((indent+1)*2, ' ') + str(type(c)))
        except RecursionError:
            pass

    def getHtmlTree(self):
        s = '<pre class="Base getHtmlTree">'
        p = StrBuffer()
        self.printTree(p=p)
        s = s + str(p) + '</pre>'
        return s

    def hasName(self, name) -> bool:
        return self.getChildByName(name) is not None

    def getChildByName(self, name):
        for c in self.childs():
            if getattr(c, 'name', None) == name:
                return c
        return None

    def findChild(self, **kwargs):
        for c in self.__childs:
            eq = True
            for k in kwargs.keys():
                if not getattr(c, k, None) == kwargs[k]:
                    eq = False
            if eq:
                return c
        return None

    def findChilds(self, **kwargs):
        res = []
        for c in self.__childs:
            eq = True
            for k in kwargs.keys():
                if not getattr(c, k, None) == kwargs[k]:
                    eq = False
            if eq:
                res.append(c)
        return res

    def has_method(self, name: str) -> bool:
        m = getattr(self, name, None)
        return m is not None

    def getOrCreateChild(self, cls, search_dict, args):
        child = self.findChild(**search_dict)
        if child is None:
            child = self.addChild(cls(*args))
        return child

    def delayed(self, time_s, op) -> Thread:
        def thread_main():
            time.sleep(time_s)
            op()
        t = Thread(target=thread_main)
        t.start()
        return t

    def periodic(self, time_s, op) -> Thread:
        return PeriodedThread(op, float(time_s), start=True)

    def free(self):
        try:
            if self.__owner is not None and isinstance(self.__owner, Base):
                self.__owner.__childs.remove(self)
        except:
            pass

    
class Named:
    def getName(self):
        return self.name
    
    
class StrBuffer:
    s = ''
    line_break = "\n"
    def __init__(self, s=''):
        self.s = s
    def __call__(self, msg):
        self.s = self.s + str(msg) + self.line_break
    def __str__(self):
        return str(self.s)
    def toString(self):
        return self.s
    

class Plugins():
    """
       Add Plugins.register('nweb_web', 'mymodule.WebClass')
    """
    PLUGINS = {}
    points = []
    def __init__(self, group):
        from importlib.metadata import entry_points
        points = list(filter(lambda e: e[0].group == group, entry_points().values()))
        if len(points) > 0:
            self.points = points[0]
        if group in Plugins.PLUGINS:
            self.points.extend(Plugins.PLUGINS.get(group, []))

    @classmethod
    def register(cls, name, endpoint):
        if name in cls.PLUGINS:
            cls.PLUGINS[name].append(endpoint)
        else:
            cls.PLUGINS[name] = [endpoint]

    def __iter__(self):
        return iter(self.points)

    def __getitem__(self, name):
        """
          Return e.g. "module.submodule:ClassOrFunction"
        """
        for p in self:
            if p.name == name:
                return p
        return None
  

class Params:
    data = {}
    orginal = None
    def __init__(self, data):
        if isinstance(data, str):
            self.orginal =  data
            if len(data)>0:
                if data[0]=='?':
                    data = data[1:]
                self.data= self.parseQuery('http://domain.end'+data)
            else:
                self.data = {}
        else:
            self.data = data
    def parseQuery(self, url):
        res = {}
        parsed_url = urlparse(url)
        q = parse_qs(parsed_url.query)
        for k in q.keys():
            res[k] = q[k][0]
        return res
    def __contains__(self, element):
        return element in self.data
    def __getitem__(self, name):
        return self.data[name]
    def __str__(self):
        return str(self.orginal)
    def filterKeys(self, key_list):
        res = {}
        for k in key_list:
            if k in self.data:
                res[k] = self.data[k]
        return res

    def get(self, key, default=None):
        return self.data.get(key, default)


class Page(StrBuffer, Base):
    THEMES: list = ['light', 'dark']
    __style = ''
    __vars = {'meta': ''}
    __loaded_scripts = []
    theme = 'light' # light or dark
    def __init__(self, s='', owner=None):
        """
          :param owner: Wird js und css aufgerufen
        """
        super().__init__(s)
        self.__style = ''
        self.__vars = {}
        self.__loaded_scripts = []
        if owner is not None:
            jsf = getattr(owner, 'js', None)
            if callable(jsf):
                self.script(jsf())
            css = getattr(owner, 'css', None)
            if callable(css):
                self.style(css())
            if isinstance(owner, Base):
                owner.addChild(self)

    def __iadd__(self, other):
        self(other)
        return self

    def __getitem__(self, name):
        return self.__vars[name]

    def __setitem__(self, name, value):
        self.__vars[name] = value

    def add_meta(self, s: str):
        if 'meta' in self.__vars:
            self.__vars['meta'] = self.__vars['meta'] + s
        else:
            self.__vars['meta'] = s

    def start_tag(self, tag_name, **kw) -> "self":
        a = ''
        if '_class' in kw:
            kw['class'] = kw['_class']
            kw.pop('_class', None)
        for k in kw.keys():
            if k.startswith('data_'):
                kn = k.replace('data_', 'data-')
            else:
                kn = k
            a += ' ' + kn + '="' + str(kw[k]) + '"'
        self('<'+tag_name+a+'>')
        return self

    def tag(self, tag_name, content='', **kw) -> "self":
        a = ''
        if '_class' in kw:
            kw['class'] = kw['_class']
            kw.pop('_class', None)
        for k in kw.keys():
            if k.startswith('data_'):
                kn = k.replace('data_', 'data-')
            else:
                kn = k
            a += ' ' + kn + '="' + str(kw[k]) + '"'
        self('<'+tag_name+a+'>'+str(content)+'</'+tag_name+'>')
        return self

    def hr(self):
        self('<hr />')
        return self

    def ul(self, items: typing.Iterable):
        s = '<ul>'
        for item in items:
            s += '<li>'+str(item)+'</li>'
        self(s + '</ul>')
        return self

    def input(self, name, **attrs):
        """
        @see form_input
        """
        attrs['name'] = name
        return self.tag('input', '', **attrs)

    def audio(self, src, **attrs):
        """
        @see form_input
        """
        attrs['src'] = src
        attrs['controls'] = 'controls'
        return self.tag('audio', '', **attrs)

    def form_input(self, name, title, **attrs):
        self('<div class="">')
        self.span(title, style='width: 150px;')
        self.input(name, **attrs)
        self('</div>')
        return self

    def combo(self, name, values, **attrs):
        from nwebclient import web
        self(web.combo(name, values, **attrs))
        return self

    def number(self, name, **attrs):
        attrs['name'] = name
        attrs['type'] = 'number'
        return self.tag('input', '', **attrs)

    def slider(self, name, **attrs):
        """ min max """
        attrs['name'] = name
        attrs['type'] = 'range'
        return self.tag('input', '', **attrs)

    def h1(self, text, **attrs):
        return self.tag('h1', text, **attrs)

    def h2(self, text, **attrs):
        return self.tag('h2', text, **attrs)

    def h3(self, text, **attrs):
        return self.tag('h3', text, **attrs)

    def h4(self, text, **attrs):
        return self.tag('h4', text, **attrs)

    def p(self, text):
        return self.tag('p', text)

    def div(self, text='', **attr):
        """
        @see dv()
        """
        return self.tag('div', text, **attr)

    def right(self, text='', **attr):
        attr['style'] = 'text-align: right;'
        return self.tag('div', text, **attr)

    def span(self, text, **attrs):
        return self.tag('span', text, **attrs)

    def td(self, text):
        return self.tag('td', text)

    def ul(self, items, **attrs):
        return self.tag('ul', "\n".join(map(lambda x: '<li>'+str(x)+'</li>', items)), **attrs)

    def pre(self, text, **attrs):
        """
        :param text: Text oder ein dict
        """
        try:
            if isinstance(text, dict) or isinstance(text, list):
                text = json.dumps(text, indent=2)
            return self.tag('pre', text, **attrs)
        except:
            return self.tag('pre', "Invalid Value", **attrs)

    def script(self, js):
        if js is None:
            return self
        if js.startswith('/') or js.startswith('http'):
            if js not in self.__loaded_scripts:
                self('<script src="'+js+'"></script>')
                self.__loaded_scripts.append(js)
            return self
        else:
            return self.tag('script', js)

    def js_ready(self, js):
        return self.script('document.addEventListener("DOMContentLoaded", function() { '+js+' }, false);')

    def style(self, s):
        if s is not None:
            if s.startswith('http') or s.startswith('/'):
                self.add_meta('<link href="' + s + '" rel="stylesheet">')
            else:
                self.__style += s
        return self

    def a(self, content, url):
        return self.tag('a', content, **{'href': url})

    def markdown(self, md):
        """
        https://github.com/showdownjs/showdown
        """
        self.script('/static/js/showdown.min.js')
        hid = 'md_'+str(uuid.uuid4()).replace('-', '')
        self.div(md, id=hid, _class='Page_markdown')
        js = 'var converter = new showdown.Converter();'
        elem = 'document.getElementById("'+hid+'").innerHTML'
        js += elem + ' = converter.makeHtml('+elem+');'
        self.script(js)
        return self

    def js_html(self, js):
        id = 'u'+uuid.uuid1().hex
        self.div('', id=id);
        self.js_ready('document.querySelector("#'+id+'").innerHTML = (function() {'+js+'})();')
        return self

    def load(self, obj):
        self.style(call_method(obj, 'style'))
        self.script(call_method(obj, 'script'))
        fn = getattr(obj, 'jsvars', None)
        if callable(fn):
            self.script('window.py = ' + json.dumps(fn())+';')
        return self

    def prop(self, title, value, html_id=None):
        attr = ''
        if html_id is not None:
            attr += ' id="'+html_id+'"'
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value)
        self.div(title+': <span'+attr+'>'+str(value)+'</span>', _class='prop')

    def grid_simple(self, array=[]):
        """ https://gijgo.com/grid """
        if len(array) == 0:
            self.div("No Data")
        else:
            hid = 'grid_' + str(uuid.uuid4()).replace('-', '')
            self.div('', id=hid)
            first = array[0]
            columns = []
            for key in first.keys():
                columns.append({'field': key, 'sortable': True})
                #  { field: 'DateOfBirth', title: 'Date Of Birth', type: 'date', width: 150 }
            self.script('https://unpkg.com/gijgo@1.9.14/js/gijgo.min.js')
            self.style('https://unpkg.com/gijgo@1.9.14/css/gijgo.min.css')
            self.script('/static/jquery.js')
            self.js_ready("""  var grid = $('#""" + hid + """').grid({
                dataSource: """ + json.dumps(array) + """,
                columns: """ + json.dumps(columns) + """,
                pager: { limit: 50 }
                });""")
        return self

    def grid(self, rows, cols=[]):
        """
           :param rows:
           :param cols: Use nwebclient.web:Grid.col()
        """
        from nwebclient import web
        g = web.Grid(rows, cols)
        g.add_to(self)

    def barchart(self, data={}):
        """ https://www.chartjs.org/docs/latest/getting-started/ """
        hid = 'barchart_' + str(uuid.uuid4()).replace('-', '')
        self.script('https://cdn.jsdelivr.net/npm/chart.js')
        self('<canvas id="'+hid+'"></canvas>')
        script = 'const ctx = document.getElementById("'+hid+'");'
        cfg = {
            'type': 'bar',
            'data': {
                'labels': list(data.keys()),
                'datasets': [{
                    'label': '-',
                    'data': list(data.values()),
                    'borderWidth': 1
                }]
            },
            'options': {
                'scales': {
                    'y': {
                        'beginAtZero': True
                    }
                }
            }
        }
        script += ' new Chart(ctx, '+json.dumps(cfg)+');'
        self.js_ready(script)
        return self

    def alert_error(self, msg=' '):
        from nwebclient import web as w
        self(w.alert_error(msg))

    def alert_success(self, msg=' '):
        from nwebclient import web as w
        self(w.alert_success(msg))

    def alert_info(self, msg=' '):
        from nwebclient import web as w
        self(w.alert_info(msg))

    def nxitems_nav(self):
        res = ''
        for p in self.getParents():
            try:
                nxitems = getattr(p, 'nxitems', None)
                if nxitems is not None:
                    for item in p.nxitems():
                        res += f'<a href="{item.get("url", "")}" class="list_item" title="{item.get("description", "")}" style="display: block">{item.get("title", "Item")}</a>'
            except Exception as e:
                print("Error: Page.nxitems_nav(): " + str(e))
                res += f'<div class="error">{str(e)}</div>'
        return res

    def theme_name(self, params={}):
        t = params.get('theme', self.theme)
        if t in self.THEMES:
            return t
        return 'light'

    def _head_scripts(self):
        return """
            <link rel="stylesheet" href="/static/js/nx/ui.css" />
            <script src="/static/js/nx/ui.js"></script>
            <script src="/static/jquery.js"></script>
            <script src="/static/js/base.js"></script>
            <script src="/static/components/base.js"></script>
        """

    def nxui(self, params={}):
        if 'page' in params and isinstance(params['page'], Page):
            params['page'].div(str(self))
        else:
            script = '' #"document.addEventListener('DOMContentLoaded', function() { window.ui = new Ui(); ui.enableSearch(); }, false);"
            response = """
            <!DOCTYPE html>
            <html>
                <head>
                    """ + self._head_scripts() + """
                    <script>
                        document.addEventListener("DOMContentLoaded", function(event) { 
                            enableSearch("#list", ".list_item");
                        });
                    </script>
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    """ + self.head_content(script=script) + """
                </head>
                <body class='""" + self.theme_name(params) + """'>
                    <div id="lbar" class="leftpart">
                        <div id="ltop">
                            """ + self.part_title(params) + """
                        </div>
                        <div id="list" class="docs">"""+self.nxitems_nav()+"""</div>
                    </div>
                    <article id="main">
                        <h2 class="doc_h">""" + params.get('title', '') + """</h2>
                        <div id="content_ops"></div>
                        <div id="content" class="doc content">""" + str(self) + """</div>
                    </article>
                </body>
            </html>
            """
            self.free()
            return response

    def nxflex(self, params={}):
        return """
        <!DOCTYPE html>
            <html>
            <head>
            <title>Page Title</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
            * { box-sizing: border-box; }
            body { font-family: Arial; margin: 0; }
            
            .nxflex .header {
              padding: 30px;
              text-align: center;
              background: #1abc9c;
              color: white;
            }
            .navbar {
              display: flex;
              background-color: #333;
            }
            .navbar a {
              color: white;
              padding: 14px 20px;
              text-decoration: none;
              text-align: center;
            }
            .navbar a:hover {
              background-color: #ddd;
              color: black;
            }
            .flexarea {  
              display: flex; flex-wrap: wrap;
            }
            .side {
              flex: 200px;
              background-color: #f1f1f1;
              padding: 20px;
            }
            .main {
              flex: 50%;
              background-color: white;
              padding: 20px;
            }
            .footer {
              padding: 20px;
              text-align: center;
              background: #ddd;
            }
            @media screen and (max-width: 700px) {
              .flexarea, .navbar {   
                flex-direction: column;
              }
            }
            </style>
                """ + self.head_content(script='') + """
            </head>
            <body class="nxflex """ + self.theme_name(params) + """">
            
                <div class="header">
                  <h1>My Website</h1>
                  <p>With a <b>flexible</b> layout.</p>
                </div>
                
                <div class="navbar">
                  <a href="#">Link</a>
                  <a href="#">Link</a>
                  <a href="#">Link</a>
                  <a href="#">Link</a>
                </div>
                
                <div class="flexarea">
                  <div class="side">
                    """ + self.nxitems_nav() + """
                  </div>
                  <div id="content" class="main doc content">
                    """ + str(self) + """
                  </div>
                  <div style="flex: 250px; background-color: #ccc;">Right</div>
                </div>
                
                <div class="footer">
                  <h2>Footer</h2>
                </div>   
            </body>
            </html>     
        """

    def nxpane(self, params={}):
        return """<head>
            <script src="/static/js/hpcc/wc-layout.js"></script>
            """ + self._head_scripts() + """
        </head>
        
        <body>
            <h1>npy</h1>
            <hpcc-splitpanel id="pane1" orientation="horizontal" style="width:100%;height:90%;">
                <div style="overflow:auto;min-width:100px;">
                    """+self.nxitems_nav()+"""
                </div>
                <div style="overflow:auto;min-width:48px">""" + str(self) + """</div>
                <hpcc-splitpanel orientation="vertical" style="width:100%;height:100%;border:0px;padding:0px;min-width:48px">
                    <div style="overflow:auto;min-height:48px">
                        <h1>HTML Ipsum Presents</h1>
                        <p><strong>Pellentesque habitant morbi tristique</strong> senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante.</p>
                    </div>
                    <div style="overflow:auto;min-height:48px">
                        <h1>HTML Ipsum Presents</h1>
                        <p><strong>Pellentesque habitant morbi tristique</strong> senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante.</p>
                    </div>
                </hpcc-splitpanel>
            </hpcc-splitpanel>
            <script>
                // pane1._splitPanel.layout.absoluteSizes()
                pane1._splitPanel.layout.setRelativeSizes([20,60,30])
            </script>
        </body>
        """

    def part_title(self, params={}):
        # Title abrufen
        return "<h1>"+self.__vars.get('h', 'nxui')+"</h1>"

    def head_content(self, style='', script=''):
        title = "<title>"+self.__vars.get('title', '')+"</title>\n"
        style_tag = "<style>"+self.__style+style+"</style>"
        res = title + self.__vars.get('meta', '') + style_tag
        if script != '':
            res += "<script>"+script+"</script>"
        return res

    def simple_page(self, params={}):
        if 'page' in params and isinstance(params['page'], Page):
            params['page'].div(str(self))
        else:
            style = """
                body, div { font-family: sans-serif;}
                div.main { margin: auto; width: 800px; }
                body.dark { background-color: #000; color: #ddd;}
            """
            return """
            <html>
              <head>
               """ + self.head_content(style=style) + """
              </head>
              <body class='""" + self.theme_name(params) + """'>
                <header>"""+self.__vars.get('header', '')+"""</header>
                <div class="main">"""+str(self)+"""</div>
                <footer>"""+self.__vars.get('footer', '')+"""</footer>
              </body>
            </html>
            """

    @contextmanager
    def section(self, h=None) -> "Self":
        self('<section style="margin: 4px" class="page_section">')
        if h is not None:
            self.h2(h)
        try:
            yield self
        except Exception as e:
            self("<pre>Error: " + str(e))
            self(''.join(traceback.format_tb(e.__traceback__)))
            self('</pre>')
        finally:
            self("</section>")

    @contextmanager
    def dv(self, **kw) -> "Self":
        self.start_tag('div', **kw)
        try:
            yield self
        except Exception as e:
            self("<pre>Error: " + str(e))
            self(''.join(traceback.format_tb(e.__traceback__)))
            self('</pre>')
        finally:
            self("</div>")

    @contextmanager
    def t(self, tag_name, **kw) -> "Self":
        self.start_tag(tag_name, **kw)
        try:
            yield self
        except Exception as e:
            self("<pre>Error: " + str(e))
            self(''.join(traceback.format_tb(e.__traceback__)))
            self('</pre>')
        finally:
            self("</"+tag_name+">")

    
def action(title=None):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        func.__action = True
        return wrapper
    return actual_decorator


def style():
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator


def script():
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator


def get_decorators(cls):
    """ {func1: [decorator1, decorator2]}  """
    import ast
    import inspect
    decorators = {}

    def visit_FunctionDef(node):
        decorators[node.name] = []
        for n in node.decorator_list:
            name = ''
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id

            decorators[node.name].append(name)

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_FunctionDef
    try:
        node_iter.visit(ast.parse(inspect.getsource(cls)))
    except TypeError:
        print("Error: getsource not on built-in or just in time compiled classes")
    return decorators


def get_with_decorator(cls,  decorator_name):
    """ {func1: {params}, func2: {params}}  """
    import ast
    import inspect
    methods = {}

    def visit_FunctionDef(node):
        names = []
        for n in node.decorator_list:
            name = ''
            named_args = {'method': node.name}
            # print(ast.dump(node))
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
                for k in n.keywords:
                    named_args[k.arg] = k.value.value
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id
            if name == decorator_name:
                methods[node.name] = named_args
            

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_FunctionDef
    node_iter.visit(ast.parse(inspect.getsource(cls)))
    return methods

def call_method(obj, func, *args, **kwargs):
    fn = getattr(obj, func, None)
    if callable(fn):
        return fn(*args, **kwargs)
    return None

class WebPage:
    def page(self, params={}):
        fn = getattr(self, 'toHtml', None)
        if fn is not None:
            return fn(params)
        else:
            return "WebPage"

class WebObject(Base, WebPage):
    def __init__(self, obj, params={}):
        Base.__init__(self)
        self.obj = obj
        self.params = params
        self.addChild(self.obj)
    def solveObject(self, obj):
        import ctypes
        if isinstance(obj, int):
            obj = ctypes.cast(obj, ctypes.py_object).value
        return obj
    def __repr__(self):
        return "WebObject({0})".format(self.obj.__repr__())
    def __str__(self):
        return "WebObject({0})".format(self.obj.__str__())
    def html(self):
        p = Page()
        p.h1("WebObject")
        actions = get_with_decorator(self.obj, 'actions')
        return p.simple_page()
    def toHtml(self, params={}):
        to_html = getattr(self.obj, 'toHtml', None)
        if to_html is None:
            return self.html()
        return self.obj.toHtml(params)
    def page(self, params={}):
        return self.toHtml(params)
    

class WebInfo(Base, Named):
    name = 'nwebclient-info'

    def __init__(self):
        super().__init__()

    def toHtml(self, params={}):
        from importlib.metadata import version 
        p = Page()
        p('<h1>Info</h1>nwebclient ' + str(version('nwebclient')))
        return p.simple_page()


class DictProxy(object):
    obj: dict

    def __init__(self, obj={}):
        self.obj = obj

    def __getitem__(self, key):
        if key in self.obj.keys():
            return self.obj[key]
        else:
            return getattr(self, key)

    def __setitem__(self, key, value):
        self.obj[key] = value

    def __getattr__(self, key):
        if key in self.obj.keys():
            return self.obj[key]
        else:
            raise AttributeError(key)

    def get(self, item, default=None):
        return self.obj.get(item, default)

    def keys(self):
        return self.obj.keys()

    def items(self):
        return self.obj.items()

