import json
import os.path
from io import BytesIO
from pathlib import Path
import urllib.parse
import html

from nwebclient import util
from nwebclient import base as b
import base64
import uuid


class Img:
    CHIP = '/static/img/chip.png'
    CHART = '/static/img/chart.png'
    GIS = '/static/img/gis.png'
    TEST = '/static/img/test.png'
    DATA = '/static/img/data.png'
    APP = '/static/img/app.png'
    PYTHON = '/static/img/app.png'


class CSS:
    UL_MENU = 'nx_menu'


class W:
    CSS_PROPERTIES = [
        "align-content", "align-items", "align-self", "all", "animation", "animation-delay",
        "animation-direction", "animation-duration", "animation-fill-mode", "animation-iteration-count",
        "animation-name", "animation-play-state", "animation-timing-function", "backface-visibility",
        "background", "background-attachment", "background-blend-mode", "background-clip",
        "background-color", "background-image", "background-origin", "background-position",
        "background-repeat", "background-size", "block-size", "border", "border-block",
        "border-block-color", "border-block-end", "border-block-end-color", "border-block-end-style",
        "border-block-end-width", "border-block-start", "border-block-start-color",
        "border-block-start-style", "border-block-start-width", "border-block-style", "border-block-width",
        "border-bottom", "border-bottom-color", "border-bottom-left-radius", "border-bottom-right-radius",
        "border-bottom-style", "border-bottom-width", "border-collapse", "border-color", "border-image",
        "border-image-outset", "border-image-repeat", "border-image-slice", "border-image-source",
        "border-image-width", "border-inline", "border-inline-color", "border-inline-end",
        "border-inline-end-color", "border-inline-end-style", "border-inline-end-width",
        "border-inline-start", "border-inline-start-color", "border-inline-start-style",
        "border-inline-start-width", "border-inline-style", "border-inline-width", "border-left",
        "border-left-color", "border-left-style", "border-left-width", "border-radius", "border-right",
        "border-right-color", "border-right-style", "border-right-width", "border-spacing", "border-style",
        "border-top", "border-top-color", "border-top-left-radius", "border-top-right-radius",
        "border-top-style", "border-top-width", "border-width", "bottom", "box-decoration-break",
        "box-shadow", "box-sizing", "break-after", "break-before", "break-inside", "caption-side", "caret-color",
        "clear", "clip", "clip-path", "color", "column-count", "column-fill", "column-gap", "column-rule",
        "column-rule-color", "column-rule-style", "column-rule-width", "column-span", "column-width",
        "columns", "contain", "content", "counter-increment", "counter-reset", "counter-set", "cursor",
        "direction", "display", "empty-cells", "filter", "flex", "flex-basis", "flex-direction", "flex-flow",
        "flex-grow", "flex-shrink", "flex-wrap", "float", "font", "font-family", "font-feature-settings",
        "font-kerning", "font-language-override", "font-optical-sizing", "font-size", "font-size-adjust",
        "font-stretch", "font-style", "font-synthesis", "font-variant", "font-variant-alternates",
        "font-variant-caps", "font-variant-east-asian", "font-variant-ligatures", "font-variant-numeric",
        "font-variant-position", "font-variation-settings", "font-weight", "gap", "grid", "grid-area",
        "grid-auto-columns", "grid-auto-flow", "grid-auto-rows", "grid-column", "grid-column-end",
        "grid-column-gap", "grid-column-start", "grid-gap", "grid-row", "grid-row-end", "grid-row-gap",
        "grid-row-start", "grid-template", "grid-template-areas", "grid-template-columns",
        "grid-template-rows", "hanging-punctuation", "height", "hyphens", "image-orientation", "image-rendering",
        "image-resolution", "ime-mode", "inherit", "initial", "inline-size", "inset", "inset-block",
        "inset-block-end", "inset-block-start", "inset-inline", "inset-inline-end", "inset-inline-start",
        "isolation", "justify-content", "left", "letter-spacing", "line-break", "line-height", "list-style",
        "list-style-image", "list-style-position", "list-style-type", "margin", "margin-block", "margin-block-end",
        "margin-block-start", "margin-bottom", "margin-inline", "margin-inline-end", "margin-inline-start",
        "margin-left", "margin-right", "margin-top", "mask", "mask-border", "mask-border-mode", "mask-border-outset",
        "mask-border-repeat", "mask-border-slice", "mask-border-source", "mask-border-width", "mask-clip",
        "mask-composite", "mask-image", "mask-mode", "mask-origin", "mask-position", "mask-repeat",
        "mask-size", "mask-type", "max-block-size", "max-height", "max-inline-size", "max-width",
        "min-block-size", "min-height", "min-inline-size", "min-width", "mix-blend-mode", "object-fit",
        "object-position", "offset", "offset-anchor", "offset-distance", "offset-path", "offset-rotate",
        "opacity", "order", "orphans", "outline", "outline-color", "outline-offset", "outline-style",
        "outline-width", "overflow", "overflow-anchor", "overflow-block", "overflow-clip-box", "overflow-inline",
        "overflow-wrap", "overflow-x", "overflow-y", "overscroll-behavior", "overscroll-behavior-block",
        "overscroll-behavior-inline", "overscroll-behavior-x", "overscroll-behavior-y", "padding",
        "padding-block", "padding-block-end", "padding-block-start", "padding-bottom", "padding-inline",
        "padding-inline-end", "padding-inline-start", "padding-left", "padding-right", "padding-top",
        "page-break-after", "page-break-before", "page-break-inside", "paint-order", "perspective",
        "perspective-origin", "place-content", "place-items", "place-self", "pointer-events", "position",
        "quotes", "resize", "right", "rotate", "row-gap", "scale", "scroll-behavior", "scroll-margin",
        "scroll-margin-block", "scroll-margin-block-end", "scroll-margin-block-start", "scroll-margin-bottom",
        "scroll-margin-inline", "scroll-margin-inline-end", "scroll-margin-inline-start", "scroll-margin-left",
        "scroll-margin-right", "scroll-margin-top", "scroll-padding", "scroll-padding-block",
        "scroll-padding-block-end", "scroll-padding-block-start", "scroll-padding-bottom",
        "scroll-padding-inline", "scroll-padding-inline-end", "scroll-padding-inline-start",
        "scroll-padding-left", "scroll-padding-right", "scroll-padding-top", "scroll-snap-align",
        "scroll-snap-stop", "scroll-snap-type", "shape-image-threshold", "shape-margin", "shape-outside",
        "tab-size", "table-layout", "text-align", "text-align-last", "text-combine-upright",
        "text-decoration", "text-decoration-color", "text-decoration-line", "text-decoration-style",
        "text-emphasis", "text-emphasis-color", "text-emphasis-position", "text-emphasis-style",
        "text-indent", "text-justify", "text-orientation", "text-overflow", "text-rendering",
        "text-shadow", "text-transform", "text-underline-position", "top", "touch-action", "transform",
        "transform-box", "transform-origin", "transform-style", "transition", "transition-delay",
        "transition-duration", "transition-property", "transition-timing-function", "translate",
        "unicode-bidi", "user-select", "vertical-align", "visibility", "white-space", "widows", "width",
        "will-change", "word-break", "word-spacing", "word-wrap", "writing-mode", "z-index"
    ]

    @staticmethod
    def is_css_prop(name: str):
        return name.replace('_', '-') in W.CSS_PROPERTIES


def ql(params, newps={}, remove_keys=[]) -> str:
    """
    :return: Query String z.B. "?a=42"
    """
    ps = {**params, **newps}
    for key in remove_keys:
        if key in ps:
            ps.pop(key)
    return '?' + urllib.parse.urlencode(ps)


def htmlentities(text):
    t = str(text)
    return t.replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;').replace('\'', '&#39;').replace('"', '&#34;')


def css_parse_dict(v: dict):
    res = ''
    for k, v in v.items():
        # TODO key anpassen aus margin_left margin-left
        res += k + ': ' + v + '; '
    return res


def tag(tag_name, content, **kw):
    a = ''
    if '_class' in kw:
        kw['class'] = kw['_class']
        kw.pop('_class', None)
    #for k in list(kw.keys()): # TODO
    #    if W.is_css_prop(k):
    #
    for k in kw.keys():
        if k == 'style' and isinstance(kw[k], dict):
            a += ' ' + k + '="' + css_parse_dict(kw[k]) + '"'
        else:
            a += ' ' + k + '="' + str(kw[k]) + '"'
    return '<'+tag_name+a+'>'+str(content)+'</'+tag_name+'>'


def s(text):
    return html.escape(str(text), quote=True)

def a(content, href):
    if isinstance(href, str):
        return tag('a', content, href=href)
    else:
        return tag('a', content, **href)


def pre(content, **kw):
    return tag('pre', content, **kw)


def div(content, **kw):
    return tag('div', content, **kw)


def span(content, **kw):
    return tag('span', content, **kw)


def tt(content, **kw):
    return tag('tt', content, **kw)


def ul(items):
    s = '<ul>'
    for item in items:
        s += '<li>' + str(item) + '</li>'
    return s + '</ul>'


def input(name, **attrs):
    attrs['name'] = name
    return tag('input', '', **attrs)


def hidden(name, val):
    return input(name, type='hidden', value=val)


def combo(name, values, **attrs):
    options = ''
    attrs['name'] = name
    if isinstance(values, list):
        for v in values:
            options += f'<option value="{v}">{v}</option>'
    elif isinstance(values, dict):
        for k, v in values.items():
            options += f'<option value="{v}">{k}</option>'
    return tag('select', options, **attrs)


def textarea(content, **kwargs):
    return tag('textarea', content, **kwargs)


def submit(title="Senden", **kwargs):
    return input(value=title, type='submit', **kwargs)


def style(css):
    return tag('style', css)


def script(js):
    if js.startswith('/') or js.startswith('http'):
        return '<script src="'+js+'"></script>'
    else:
        return f'<script>{js}</script>'


def img(src):
    return f'<img src="{src}" />'


def img_j64(binary_data):
    if isinstance(binary_data, BytesIO):
        binary_data = binary_data.getvalue()
    base64_utf8_str = base64.b64encode(binary_data).decode('utf-8')
    url = f'data:image/jpg;base64,{base64_utf8_str}'
    return img(url)


def img_f64(path):
    return img_j64(util.file_get_contents(path))


def table(content, **kw):
    s = '<table>'
    if isinstance(content, list):
        for rows in content:
            s += '<tr>'
            for cell in rows:
                s += '<td>'+str(cell)+'<td>'
            s += '</tr>'
    else:
        s += content
    s += '</table>'
    return s


def svg_inline(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            lines = f.readlines()
            while len(lines) > 0:
                if lines[0].startswith('<svg'):
                    break
                lines.pop(0)
            return "\n".join(lines)
    else:
        return '<!-- NON EXISTING -->'


def js_ready(js):
    return 'document.addEventListener("DOMContentLoaded", function() { '+str(js)+' }, false);';


def js_fn(name, args, code=[]):
    if isinstance(code, str):
        body = code
    else:
        body = '\n'.join(code)
    return 'function '+name+'('+','.join(args)+') {\n'+body+'\n}\n\n'


def js_interval(t=1000, js='console.log("ping")'):
    return 'setInterval(function() { '+js+' }, '+str(t)+');'


def js_add_event_for_id(id, event_js):
    return 'document.getElementById("'+id+'").addEventListener("click", function(e) {\n '+event_js+' \n});\n'


def button_js(title: str, js_action, css_class=None):
    id = 'btn' + str(uuid.uuid4()).replace('-', '')
    jsa = 'document.getElementById("'+id+'").innerHTML = "Processing..."; '
    title = title.replace('"', "")
    jsa += 'setTimeout(function() { document.getElementById("'+id+'").innerHTML = "'+title+'"; }, 3000);'
    jsa += js_action
    js = js_ready(js_add_event_for_id(id, jsa))
    attr = ''
    if css_class is not None:
        attr += ' class="'+css_class+'"'
    res = '<button id="'+id+'"'+attr+'>'+str(title)+'</button><script type="text/javascript">'+js+'</script>'
    return res


def alert_error(msg=' '):
    m = str(msg)
    return f'<div style="border-left: #900 5px solid; background-color: #b77; color: #000;padding:4px;">{m}</div>'


def alert_success(msg=' '):
    m = str(msg)
    return f'<div style="border-left: #090 5px solid; background-color: #7b7; color: #000;padding:4px;">{m}</div>'


def alert_info(msg=' '):
    m = str(msg)
    return f'<div style="border-left: #009 5px solid; background-color: #77b; color: #000;padding:4px;">{m}</div>'


def js_base_url_exp():
    # (location.port==""?"":":"+location.port)+
    return 'location.protocol+"//"+location.host+"/"'


def route_root(web, root):
    web.add_url_rule('/pysys/root', 'r_root', view_func=lambda: root.getHtmlTree())
    res = NwFlaskRoutes()
    res.addTo(web)
    return res


class WebRoute(b.Base, b.WebPage):
    def __init__(self, route, name, func):
        self.route = route
        self.name = name
        self.func = func
    def page(self, params={}):
        return self.func()

def all_params():
    from flask import request
    requestdata = {**request.args.to_dict(), **request.form.to_dict()}
    for name in request.files.to_dict().keys():
        f = request.files[name]
        requestdata[name] = base64.b64encode(f.read())
    return requestdata


def get_static_path():
    if os.path.isdir('../static'): # Debug
        return os.getcwd()+'/../static/'
    elif os.path.isdir(str(Path.home() / "static")):
        return str(Path.home() / "static") + '/'
    elif os.path.isdir(str(Path.home() / "dev" / "static")):
        return str(Path.home() / "dev" / "static") + '/'
    elif os.path.isdir('/var/www/html/static'):
        # git@gitlab.com:bsalgert/static.git
        # https://gitlab.com/bsalgert/static.git
        # https://gitlab.com/bsalgert/static/-/archive/main/static-main.zip
        return '/var/www/html/static/'
    return None


def response(image=None):
    from flask import Flask, send_file
    if image is not None:
        from PIL import Image
        if isinstance(image, Image):
            buffer = BytesIO()
            image.save(buffer, format="JPEG")  # oder "JPEG"
            buffer.seek(0)
            image = buffer
        return send_file(image, mimetype='image/jpeg')


class NwFlaskRoutes(b.Base):
    """
        Definition on /nw und /nws
    """

    routes = {}

    routes_added = False

    def __init__(self, childs=[]):
        super().__init__()
        self.app = None
        for child in childs:
            self.addChild(child)

    def requestParams(self):
        from flask import request
        data = {}
        for tupel in request.files.items():
            name = tupel[0]
            f = tupel[1]
            #print(str(f))
            data[name] = base64.b64encode(f.read()).decode('ascii')
        params = {
            **request.cookies.to_dict(),
            **request.args.to_dict(), 
            **request.form.to_dict(),
            **data,
            **{'request_url': request.url}}
        return params
    def addTo(self, app):
        self.web = app
        if self.routes_added is True:
            return
        self.routes_added = True
        app.add_url_rule('/nw/<path:p>', 'nw', lambda p: self.nw(p), methods=['GET', 'POST'])
        app.add_url_rule('/nws/', 'nws', self.nws)
    def nws(self):
        p = b.Page().h1("Module")
        for e in b.Plugins('nweb_web'):
            p.div('<a href="{0}" title="Plugin">{1}</a>'.format('/nw/'+e.name, e.name))
        for e in self.childs():
            p.div('<a href="{0}" title="Object">{1}</a>'.format('/nw/' + e.name, e.name))
        return p.simple_page()

    def add_url_rule(self, route, name, view_func):
        print("Route" + route + " via add_url_rule")
        self.routes[route] = view_func
        self.addChild(WebRoute(route, name, view_func))

    def load_flask_blueprints(self, app):
        for e in b.Plugins('flask_blueprints'):
            blueprint = util.load_class(e)
            app.register_blueprint(blueprint)


    def nw(self, path):
        params = self.requestParams()
        n = path.split('/')[0]
        if self.hasName(n):
            return self.getChildByName(n).page(params)
        plugin = b.Plugins('nweb_web')[n]
        if plugin is not None:
            obj = util.load_class(plugin.value, create=True)
            w = self.addChild(b.WebObject(obj, {**{'path': path}, **params}))
            w.name = n
            return w.page(params)
        else:
            return "Error: 404 (NwFlaskRoutes)"

    def handleRoute(self, path, request):
        # add and serv via error404
        return "Route " + str(path), 200

    def error404(self):
        from flask import Flask, request
        if request.path in self.routes.keys():
            return self.handleRoute(request.path, request)
        else:
            status = 404
            return "Error: 404 Not Found, nwebclient.web:NwFlaskRoutes", status

    def create_app(self):
        from flask import Flask, request
        self.app = Flask(__name__)
        self.app.register_error_handler(404, lambda: self.error404())
        # @app.route('/')
        self.addTo(self.app)

    def serv(self, args={},  port=8080):
        self.create_app()
        self.run(port=port)

    def redirect_static(self):
        from flask import Flask, request, redirect
        route = '/static/<path:p>'
        self.app.add_url_rule(route, 'static', lambda p: redirect('https://bsnx.net' + request.path), methods=['GET', 'POST'])
        # AssertionError -> dann gibt es die static route schon

    def serv_dir(self, route, path):
        from flask import send_file
        e = route.replace('/', '')
        p = route + '<path:filename>'
        kwa = {}
        kwa['static_url_path'] = route
        kwa['static_folder'] = path
        #self.app.add_url_rule(p, endpoint=e, view_func=lambda **kwa: self.app.send_static_file(**kwa))  #
        self.app.add_url_rule(p, endpoint=e, view_func=lambda filename: send_file(path + filename))

    def run(self, app=None, port=8080):
        print('NwFlaskRoutes::run(...) in ' + os.getcwd())
        if app is not None:
            self.app = app
        kw = {}
        if os.path.isdir('../app'):  # Debug
            self.serv_dir('/app/', os.getcwd() + '/../app/')
        static_path = get_static_path()
        if static_path is not None: # Debug
            self.serv_dir('/static/', static_path)
            #kwa = {}
            #kwa['static_url_path'] = '/static'
            #kwa['static_folder'] = '/var/www/html/static'
            #self.app.add_url_rule(f"/static/<path:filename>", endpoint="static", view_func=lambda **kwa: self.app.send_static_file(**kwa))  #
        else:
            self.redirect_static()
        self.app.run(host='0.0.0.0', port=int(port), **kw)


class PageElement:
    def add_to(self, p: b.Page):
        pass


class LiteGraph(PageElement):
    """

    """

    node_classes = []

    def __init__(self):
        from nwebclient import visual
        self.width = '1024'
        self.height = '768'
        self.visual = visual
        self.node_classes = []
        self.script = ''
        self.items = visual.Items()
        self.item_name = lambda item: item.name

    def contains_name(self, n):
        return n in list(map(self.item_name, self.items))

    def create_custom_node(self, class_name, title):
        self.node_classes.append(class_name)
        res = 'function '+class_name+'() {'
        #    this.addInput("A", "number");
        #this.addInput("B", "number");
        #this.addOutput("A+B", "number");
        # this.addWidget("text", "Text", "edit me", function(v) {}, {} );
        #this.properties = {precision: 1};
        res += '}'

        # name to show
        res += class_name+'.title = "'+title+'";'

        # function to call when the node is executed
        res += class_name + '.prototype.onExecute = function() {}'

        #this.addWidget("button", "Log", null, function()
        #{
        #    console.log(that.properties);
        #});

        # register in the system
        res += 'LiteGraph.registerNodeType("basic/nx", '+class_name+');'
        return res

    def create_node(self, name, node_type='basic/string', pos=(100, 100), size=(100, 150), value=None, item=None):
        """

        :param name str:
        :param node_type:
        :param pos:
        :param size:
        :param value:
        :param item nwebclient.visual.Box:
        :return:
        """
        res = 'var '+name+' = LiteGraph.createNode("'+node_type+'");'
        res += name + '.pos = ['+str(pos[0])+', '+str(pos[1])+'];'
        res += name + '.size = ['+str(size[0])+', '+str(size[1])+'];'
        res += name + '.addInput("in0", "string" );'
        res += name + '.addOutput("out0", "string" );'
        res += 'graph.add('+name+');'
        if node_type == 'basic/const' and value is not None:
            res += name+'.setValue('+value+');'
        if node_type == 'basic/string' and value is not None:
            res += name+'.setValue("'+value+'");\n'
        if util.is_subclass_of(item.obj.__class__, 'BaseJobExecutor'):
            if getattr(item.obj, 'litegraph_create_note', None) is not None:
                res += getattr(item.obj, 'litegraph_create_note', None)()
        #if isinstance(item.obj, BaseJobExecutor):
        #    #    add vars
        return res

    def create_connection(self, name_a, name_b):
        if self.contains_name(name_a) and self.contains_name(name_b):
            res = name_a + '.connect(0, '+name_b+', 0);'
            self.script += res + "\n"
            return res
        else:
            return ''

    def head(self):
        return """
            <link rel="stylesheet" type="text/css" href="/static/js/litegraph.js/litegraph.css">
	        <script type="text/javascript" src="/static/js/litegraph.js/litegraph.js"></script>
        """

    def name_for(self, item):
        res = self.item_name(item)
        if res is None:
            res = 'id' + str(id(item)) # type(x).__name__
        return res

    def create_script(self):
        res = 'var graph = new LGraph(); var canvas = new LGraphCanvas("#graph", graph);'
        for item in self.items:
            name = self.name_for(item)
            res += self.create_node(name, pos=item.pos, value=name, item=item)
        res += self.script
        res += 'graph.start();'
        return res

    def html(self):
        html = "<canvas id='graph' width='"+str(self.width)+"' height='"+str(self.height)+"' style='border: 1px solid'></canvas>"
        html += "<script>" + self.create_script() + "</script>"
        return html

    def add_to(self, p: b.Page):
        p.add_meta(self.head())
        p(self.html())


class Canvas(PageElement):
    """
        @seealso php ...
    """

    def __init__(self):
        from nwebclient import visual
        self.visual = visual
        self.items = visual.Items()

    def __len__(self):
        return len(self.items)

    def add(self, elem):
        if isinstance(elem, self.visual.Box):
            self.items.append(elem)
        else:
            self.items.append(self.visual.Box(elem))

    def _map_item(self, item: "nwebclient.visual.Box"):
        return div(div(str(item), _class="header")+div(''), _class="Canvas_Box")

    def head(self):
        return """
            <script src="/static/js/jquery/jquery-ui.js"></script>
            <link rel="stylesheet" type="text/css" href="/static/js/jquery/ui.css">
        """ + script(self.js())

    def js(self):
        return js_ready(
            '$(".Canvas_Box").draggable({ handle: ".header" });'
        )

    def html(self):
        return div("\n".join(map(self._map_item, self.items)), _class="python Canvas")

    def add_to(self, p: b.Page):
        p.add_meta(self.head())
        p(self.html())


class Grid(PageElement):

    def __init__(self, rows, cols=[]):
        """
        { width: 64, tmpl: '{entity_id}', align: 'center', events: { 'click': Edit } },
        https://gijgo.com/grid/configuration/column.renderer
          { field: 'PlaceOfBirth', renderer: function (value, record) { return record.ID % 2 ? '<b>' + value + '</b>' : '<i>' + value + '</i>'; }  }
        """
        self.hid = 'grid_' + str(uuid.uuid4()).replace('-', '')
        if isinstance(rows, util.List):
            rows = rows.to_base()
        self.rows = rows
        self.cols = list(map(self._mapcol, cols))

    def _mapcol(self, col):
        if isinstance(col, str):
            return {'field': col}
        else:
            return col

    @staticmethod
    def col(key, title=None, sortable=False, width=None, type=None, tmpl=None, renderer=None):
        c = {'field': key}
        if title is not None:
            c['title'] = title
        if sortable is True:
            c['sortable'] = True
        if width is not None:
            c['width'] = width
        if type is not None:
            c['type'] = type
        if tmpl is not None:
            c['tmpl'] = tmpl
        if renderer is not None:
            c['renderer'] = renderer
        return c

    def add_col(self, *args, **kwargs):
        c = self.col(*args, **kwargs)
        self.cols.append(c)

    def data_json_str(self):
        return json.dumps(self.rows)

    def config(self):
        return {  # columnReorder  grouping: { groupBy: 'CountryName' },
            'dataSource': self.rows,
            'columns':  self.cols,
            'resizableColumns': True,
            'pager': {'limit': 20}
        }

    def js(self):
        return "var grid = $('#"+self.hid+"').grid("+json.dumps(self.config())+");"

    def add_to(self, p: b.Page):
        p.script('/static/jquery.js')
        p.style('/static/js/gijgo/m.css')
        p.script('/static/js/gijgo/m.js')
        p(f'<table id="{self.hid}"></table>')
        p.js_ready(self.js())

