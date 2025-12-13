import glob
import os
import os.path
import types
import urllib.parse
import sys
import importlib
import inspect
import json
from json.decoder import JSONDecodeError
import socket
import time
import uuid
from datetime import datetime
from contextlib import closing
from threading import Thread


class Args:
    """
      Arg-Parser der eine Überprüfung der Argument vornimmt. 
      Wenn man beim aufruf noch nicht weiß welche Argument abgefragt werden sollen
    """
    argv = []
    i = 0
    cfg = None

    def __init__(self, argv=None, read_nxd=True):
        self.read_nxd = read_nxd
        if argv is None:
            self.argv = sys.argv
        else:    
            self.argv = argv

    @staticmethod
    def from_cmd(cmd: str):
        args = Args([])
        args.cfg = {}
        a = cmd.split(' ')
        for i in range(0, len(a)-1):
            if a[i].startswith('--'):
                args.cfg[a[i][2:]] = a[i+1]
        return args

    def __str__(self):
        return f"Args(frist: {self.first()})"

    def __len__(self):
        return len(self.argv)

    def __iter__(self):
        self.__read_cfg()
        return iter(self.cfg.keys().__iter__())

    def help_requested(self):
        return self.hasFlag('help') or self.hasShortFlag('h') or '?' in self.argv

    def hasFlag(self, name):
        return '--'+name in self.argv

    def shift(self):
        if len(self.argv) <= self.i:
            return ''
        res = self.argv[self.i]
        self.i += 1
        return res

    def first(self):
        if len(self.argv) <= self.i:
            return ''
        else:
            return self.argv[self.i]

    def hasName(self, name):
        return name in self.argv

    def hasShortFlag(self, name):
        return '-'+name in self.argv

    def get(self, key, default=None):
        return self.val(key, default)

    def getValue(self, name, default=None):
        """
            liest --name value Parameter
        """
        for i in range(len(self.argv)-1):
            if self.argv[i] == '--'+name:
                return self.argv[i+1]
        return default

    def val(self, name, default=None):
        if self.hasFlag(name):
            return self.getValue(name, default)
        else:
            return self.env(name, default)

    def getValues(self, name):
        res = []
        for i in range(len(self.argv)-1):
            if self.argv[i] == '--'+name:
                res.append(self.argv[i+1])
        return res

    def to_dict(self):
        res = {}
        for i in range(len(self.argv)-1):
            if self.argv[i].startswith('--'):
                res[self.argv[i][2:]] = self.argv[i+1]
        return res

    def merge_yml(self, yml_file):
        try:
            print("[Args] " + yml_file)
            import yaml
            with open(yml_file, 'r') as f:
                data = yaml.load(f.read(), Loader=yaml.Loader)
            self.cfg = merge(self.cfg, data)
        except Exception as e:
            print("[Args] YML-Error:" + str(e), file=sys.stderr)

    def __read_sys_config(self):
        if os.path.isfile('/etc/nweb.yml'):
            self.merge_yml('/etc/nweb.yml')
        if os.path.isdir('/etc/nx.d') and self.read_nxd:
            for f in glob.glob('/etc/nx.d/*.yml'):
                self.merge_yml(f)

    def __read_cfg(self):
        if self.cfg is None:
            try:
                if os.path.isfile('nweb.json'):
                    with open('nweb.json') as f:
                        self.cfg = json.load(f)
                elif os.path.isfile('/etc/nweb.json') and '-no-nx-cfg' not in self.argv:
                    with open('/etc/nweb.json') as f:
                        self.cfg = json.load(f)
                else:
                    self.cfg = {}
                if '-no-nx-cfg' not in self.argv:
                    self.__read_sys_config()
            except JSONDecodeError as e:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=sys.stderr)
                print("!!  JSONDecodeError from nwebclient.util:Args", file=sys.stderr)
                print("!!  nweb.json Syntax Error", file=sys.stderr)
                print("!!  "+str(e), file=sys.stderr)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=sys.stderr)
                self.cfg = {}

    def env(self, name, default=None):
        self.__read_cfg()
        if name in self.cfg:
            return self.cfg[name]
        return os.getenv(name, default)

    def __contains__(self, item):
        self.__read_cfg()
        return (self.cfg is not None and item in self.cfg) or self.hasFlag(item)

    def __getitem__(self, name):
        if isinstance(name, int):
            return self.argv[name]
        elif self.hasFlag(name):
            return self.getValue(name)
        else:
            return self.env(name)

    def __get__(self, i):
        return self.argv[i]

    def dispatch(self, **kwargs):
        arg = self.shift()
        if arg == sys.argv[0]:
            arg = self.shift()
        arg = arg.replace('-', '_')
        if arg in kwargs:
            kwargs[arg](self)
        else:
            print("Unknown Argument. " + arg)
            print("Valid Options: " + ", ".join(kwargs.keys()))
            if 'help' in kwargs:
                kwargs['help']()


class LimitStrList:
    def __init__(self, limit=100, auto_trim=False):
        self.limit = limit
        self.auto_trim = auto_trim
        self.list = []

    def __repr__(self):
        return repr(self.list)

    def __contains__(self, item):
        return item in self.list

    def append(self, item):
        if self.auto_trim:
            item = item.strip()
        self.list.append(item)
        if len(self.list) > self.limit:
            self.list.pop(0)

    def clear(self):
        self.list = []

    def __str__(self):
        s = ''
        for line in self.list:
            s += line + "\n"
        return s

    def __len__(self):
        return len(self.list)

    def __getitem__(self, item):
        return self.list[item]

    def __iter__(self):
        return self.list.__iter__()


class List:
    def __init__(self, items=None):
        if items is None:
            self.items = list()
        else:
            self.items = items

    def __repr__(self):
        if self.is_empty():
            return 'List()'
        else:
            return str(self.items)

    def __iadd__(self, other):
        self.items.append(other)

    def __iter__(self):
        return self.items.__iter__()

    def __getitem__(self, item):
        return self.items[item]

    def __len__(self):
        return len(self.items)

    def shift(self):
        res = self.items[0]
        del self.items[0]
        return res

    def copy(self) -> "List":
        res = List()
        res.add_all(self)
        return res

    def clear(self):
        self.items.clear()

    def is_empty(self):
        return self.__len__() == 0

    def append(self, item):
        self.items.append(item)

    def add_all(self, collection):
        for item in collection:
            self.items.append(item)

    def getattr(self, item, attr):
        key = getattr(item, attr, None)
        if isinstance(key, types.MethodType) or isinstance(key, types.FunctionType):
            key = key()
        if key is None and isinstance(item, dict):
            key = item.get(attr)
        return key

    def sum(self, attr):
        res = 0
        for item in self:
            key = self.getattr(item, attr)
            res += key
        return res

    def max(self, attr):
        res = 0
        for item in self:
            res = max(self.getattr(item, attr), res)
        return res

    def min(self, attr):
        res = 0
        for item in self:
            res = min(self.getattr(item, attr), res)
        return res

    def avg(self, attr):
        return self.sum(attr) / len(self)

    def group_by(self, attr) -> dict:
        res = {}
        for item in self:
            key = self.getattr(item, attr)
            if key in res:
                res[key].append(item)
            else:
                res[key] = List([item])
        return res

    def unique(self, attr):
        res = set()
        for item in self:
            res.add(self.getattr(item, attr))
        return res

    def select(self, **kwargs):
        """
        """
        res = List()
        for item in self:
            add = True
            for key in kwargs:
                if self.getattr(item, key) != kwargs[key]:
                    add = False
            if add:
                res.append(item)
        return res

    def q(self, **kwargs):
        return self.select(**kwargs)

    def classes(self, type):
        res = List()
        for itm in self:
            if isinstance(itm, type):
                res.append(itm)
        return res

    def select_one(self, **kwargs):
        return self.select(**kwargs)[0]

    def contains_value(self, attr, value):
        return len(self.select(**{attr: value})) > 0

    def get_or_create(self, cls, attr, value, ctor={}):
        if self.contains_value(attr, value):
            return self.select_one(**{attr: value})
        else:
            obj = cls(**ctor)
            self.append(obj)
            return obj

    def to_base(self):
        res = []
        from nwebclient import base
        for item in self:
            if isinstance(item, base.DictProxy):
                res.append(item.to_dict())
            else:
                res.append(item)
        return res

    def update_list(self, new_list, added_callback=None, removed_callback=None):
        """
        Vergleicht zwei Listen und ruft Callbacks für hinzugefügte und entfernte Elemente auf.

        :param new_list: Die aktualisierte Liste.
        :param added_callback: Die Callback-Funktion für hinzugefügte Elemente.
        :param removed_callback: Die Callback-Funktion für entfernte Elemente.
        """
        added_elements = set(new_list) - set(self.items)
        for element in added_elements:
            if added_callback is not None:
                added_callback(element)
        removed_elements = set(self.items) - set(new_list)
        for element in removed_elements:
            if removed_callback is not None:
                removed_callback(element)
        self.items = new_list
        return self


class SqlCreateTable:

    def __init__(self, node):
        self.cols = {}
        import sqlglot
        if isinstance(node, str):
            node = sqlglot.parse_one(node)
        self.node = node
        import sqlglot
        self.name = None
        for t in self.node.find_all(sqlglot.exp.Table):
            self.name = t.name
            break
        if self.name is not None:
            print("Table: " + self.name)
            for col in list(self.node.find_all(sqlglot.exp.ColumnDef)):
                print(" Col:" + str(col))
                self.cols[col.name] = {}

    def __iter__(self):
        return self.cols.keys().__iter__()

    def to_sqlite_sql(self):
        import sqlglot
        self.node.set('exists', True)
        return sqlglot.transpile(self.node.sql(), write='sqlite')[0]


class SqlScript:

    tables = []

    def __init__(self, sql):
        import sqlglot
        from sqlglot import exp
        self.tables = []
        self.tree = sqlglot.parse(sql, error_level=sqlglot.ErrorLevel.IGNORE)
        for itm in self.tree:
            if isinstance(itm, exp.Create) and itm.kind == 'TABLE':
                try:
                    self.tables.append(SqlCreateTable(itm))
                except Exception as e:
                    print("[SQL] Parse Error: " + str(e))

    def __getitem__(self, item):
        for t in self.tables:
            if t.name == item:
                return t

    def __iter__(self):
        return self.tables.__iter__()


def has_typed_arg(spec, name, cls):
    ano = spec.annotations.get(name, None)
    if ano is not None:
        return ano == cls
    else:
        return False


def load_class(spec, create=False, args={}, run_args:Args=None):
    """
    spec = 'module:ClassName'
    run_args: Der Wert von run_args wird für den Konstruktorparameter args gesetzt
    """
    if args is None:
        args = {}
    if isinstance(spec, type):
        c_spec = inspect.getfullargspec(spec)
        if run_args is not None and has_typed_arg(c_spec, 'args', Args):
            args['args'] = run_args
        return spec(**args)
    elif not isinstance(spec, str):
        return spec
    try:
        a = spec.split(':')
        m = importlib.import_module(a[0])
        c = getattr(m, a[1])
        if create:
            spec = inspect.getfullargspec(c)
            if run_args is not None and has_typed_arg(spec, 'args', Args):
                args['args'] = run_args
            return c(**args)
        else:
            return c
    except ModuleNotFoundError as e:
        print("[nwebclient.util.load_class] ModuleNotFoundError Spec: " + str(spec), file=sys.stderr)
        print("[nwebclient.util.load_class] PWD: " + str(os.getcwd()), file=sys.stderr)
        raise e


def create_instance(spec: str, **kwargs):
    mi = spec.index(':')
    pi = spec.index('(')
    m = spec[:mi]
    c = spec[mi+1:pi]
    p = spec[pi:]
    modul = importlib.import_module(m)
    obj = eval('modul.' + c + p, globals(), {'modul': modul, **kwargs})
    return obj


def load_resource(module, filename):
    # https://stackoverflow.com/questions/6028000/how-to-read-a-static-file-from-inside-a-python-package
    import importlib.resources as pkg_resources
    #try:
    #    inp_file = (pkg_resources.files(module) / filename)
    #    with inp_file.open("rb") as f:  # or "rt" as text file with universal newlines
    #        return f.read()
    #except AttributeError:
    #    # Python < PY3.9, fall back to method deprecated in PY3.11.
    return pkg_resources.read_text(module, filename)


def exists_module(module_name):
    """
      itertools = importlib.import_module('itertools')
      import pkg_resources
      pkg_resources.get_distribution('requests').version
    """
    import importlib.util
    module_spec = importlib.util.find_spec(module_name)
    found = module_spec is not None
    return found


def append_query(url, params={}):
    return url + '?' + urllib.parse.urlencode(params)


def format_datetime(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M')


def download(url, filename, ssl_verify=True, verbose=False):
    import requests
    r = requests.get(url, stream=True, verify=ssl_verify) 
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    else:
        if verbose:
            print(f"[util.download] Faild, Status: {r.status_code}")


def download_resources(path, resources: dict):
    if path != '':
        if path[-1] != '/':
            path += '/'
    for key in resources.keys():
        f = path + key
        if not os.path.isfile(f):
            print("Downloading: " + key)
            download(resources[key], f, False)


def wget(url, verify=False):
    import requests
    r = requests.get(url, verify=verify)
    return r.text


def wget_to_tmp(url, filename):
    import tempfile
    path = tempfile.gettempdir() + '/' + filename
    if os.path.isfile(path):
        return path
    download(url, path)
    return path


def file_get_contents(filename):
    with open(filename, 'rb') as f:
        return f.read()

def file_get_text(filename):
    with open(filename, 'r') as f:
        return f.read()


def file_get_lines(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.readlines()


def file_put_contents(filename, contents):
    if isinstance(contents, bytes):
        with open(filename, "wb") as f:
            f.write(contents)
    else:
        with open(filename, "w") as f:
            f.write(contents)


def file_append_contents(filename, contents):
    with open(filename, "a") as f:
        f.write(contents + "\n")


def load_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def is_port_free(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    return result != 0


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def run_async(op) -> Thread:
    t = Thread(target=op)
    t.start()
    return t

def setInterval(function, interval):
    def loop():
        while True:
            time.sleep(interval/1000)
            function()

    from threading import Thread
    t = Thread(target=loop)
    t.start()
    return t


def split(a, n):
    """
        Teilt eine Liste in gleich große Teile
    """
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def get_subclasses(obj):
    class_names = []
    while getattr(obj, '__base__', None) is not None:
        class_names.append(obj.__name__)
        obj = obj.__base__
    return class_names


def is_subclass_of(obj, cls_name):
    return cls_name in get_subclasses(obj)


def guid():
    return str(uuid.uuid4()).replace('-', '')


def fullname(klass):
    module = klass.__module__
    if module == 'builtins':
        return klass.__qualname__ # avoid outputs like 'builtins.str'
    return module + ':' + klass.__qualname__


def parse_query_string(qs: str):
    from urllib.parse import parse_qs
    if qs.startswith('?'):
        qs = qs[1:]
    data = parse_qs(qs)
    def fn(v):
        if len(v) == 1:
            return v[0]
        else:
            return v
    data = {k: fn(v) for k, v in data.items()}
    return data


def hash(m) -> str:
    import hashlib
    return hashlib.md5(m.encode()).hexdigest()


def merge(a: dict, b: dict):
    res = {}
    for key, value in a.items():
        if isinstance(value, dict) and isinstance(b.get(key, None), dict):
            res[key] = merge(value, b.get(key, None))
        elif isinstance(value, list) and isinstance(b.get(key, None), list):
            res[key] = [*value, *b.get(key, None)]
        else:
            res[key] = value
    for key, value in b.items():
        if key not in a.keys():
            res[key] = value
    return res


class SkipWithBlock(Exception):
    pass


class Optional(object):
    """

        >>> with Optional('a') as a:
        ...   print(a)
        ...
        a
        >>> with Optional(None) as a:
        ...   print(a)


    """
    def __init__(self, obj):
        self.obj = obj
    def __str__(self):
        return str(self.obj)
    def __enter__(self):
        if self.obj is None:
            sys.settrace(lambda *args, **keys: None)
            frame = sys._getframe(1)
            frame.f_trace = self.trace
        else:
            return self.obj
    def trace(self, frame, event, arg):
        raise SkipWithBlock()
    def __exit__(self, type, value, traceback):
        if type is None:
            return  # No exception
        if issubclass(type, SkipWithBlock):
            return True  # Suppress special SkipWithBlock exception


def flatten_dict(d, parent_key='', sep='_'):
    """
    Flacht ein verschachteltes Dictionary ab, indem verschachtelte Schlüssel
    mit einem Trennzeichen kombiniert werden.

    Beispiel:
        Input: {'a': {'sub': 1}, 'b': {'x': {'y': 2}}, 'c': 3}
        Output: {'a_sub': 1, 'b_x_y': 2, 'c': 3}

    Args:
        d (dict): Das zu flachende Dictionary.
        parent_key (str): Interner Parameter für rekursive Schlüsselpräfixe (nicht manuell setzen).
        sep (str): Das Trennzeichen zur Verbindung verschachtelter Schlüssel.

    Returns:
        dict: Ein flaches Dictionary mit kombinierten Schlüsseln.
    """
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

def get_title(obj, default="Item"):
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get('title', default)
    title_attr = getattr(obj, 'title', default)
    if isinstance(title_attr, types.FunctionType):
        return title_attr()
    else:
        return str(title_attr)


def get_primitive_properties(obj) -> dict:
    """
    Diese Funktion durchsucht alle Attribute eines Python-Objekts und speichert jene,
    die primitive Types (str, int, float, bool, NoneType) besitzen, in einem Dictionary.

    :param obj: Das Python-Objekt, dessen Properties extrahiert werden sollen
    :return: Dictionary mit allen primitiven Eigenschaften
    """
    primitive_types = (str, int, float, bool, type(None))
    primitives = {}
    for attr_name in dir(obj):
        if attr_name.startswith("__"):
            continue
        try:
            attr_value = getattr(obj, attr_name)
            if isinstance(attr_value, primitive_types):
                primitives[attr_name] = attr_value
        except AttributeError:
            pass
    return primitives


def path_combine(a, b):
    return (a + '/' + b).replace('//', '/')

def dispatch(obj, op, prefix='page_', *args, **kwargs):
    func = getattr(obj, prefix + op, None)
    if func is None:
        return func(*args, **kwargs)
    return None
