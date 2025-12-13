
from nwebclient import web as w
from nwebclient import base as b
from nwebclient import util as u
import types
import inspect


class Collection:

    def __init__(self, items=[]):
        self.items = list(items)

    def contains_name(self, name):
        for itm in self.items:
            if itm.name == name:
                return True
        return False

    def append(self, item):
        self.items.append(item)

    def __iter__(self):
        return self.items.__iter__()

    def __getitem__(self, item):
        for itm in self.items:
            if itm.name == item:
                return itm
        return None


class Types:
    @staticmethod
    def is_numeric(type_name):
        return type_name.lower() in ['int', 'integer', 'number', 'real', 'float', 'double']


class Field:
    def __init__(self, name: str, datatype: str = 'str'):
        self.name = name
        self.datatype = datatype


class Param:
    func = None
    name: str
    type: str
    description: str
    is_pos: bool
    default_value = None

    def __init__(self, name: str, datatype: str = 'str', is_pos: bool = True):
        self.name = name
        self.type = datatype
        self.is_pos = is_pos

    def desc(self, val):
        self.description = val
        return self

    def default(self, val):
        self.default_value = val
        return self

    def has_default_value(self):
        return self.default_value is not None

    def to_html(self):
        return self.name + f': <span style="color: #ccc;">{self.type}</span> '

    def to_text(self):
        res = self.name + f': {self.type} '
        if self.default_value is not None:
            res += ' = ' + str(self.default_value)
        return res

    def is_numeric(self):
        return Types.is_numeric(self.type)

    def to_input(self):
        v = ''
        if self.default_value is not None:
            v = str(self.default_value)
        args = dict(id=self.name, value=v)
        if self.is_numeric():
            args['type'] = 'number'
        self.name + ": " + w.input(self.name, **args)

    def to_openapi(self):
        """ https://swagger.io/docs/specification/v3_0/describing-parameters/
        in: path|query
          name: userId
          schema:
            type: integer
          required: true
          description: Numeric ID of the user to get

        requestBody:
        description: Optional description in *Markdown*
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Pet"
          application/x-www-form-urlencoded:
            schema:
              $ref: "#/components/schemas/PetForm"
        """
        return {
            'name': self.name,
            'in': 'query',
            'schema': {
                'type': self.type
            },
            'required': self.default_value is None,
            'description': self.description
        }


class NP(Param):
    """
      Abgeleiter Typ als SyntaxSugar für npy
    """
    def __init__(self, name, datatype='str', default_value=None):
        super().__init__(name, datatype)
        self.default(default_value)
        self.is_pos = False


class PInt(Param):
    """
      Abgeleiter Typ als SyntaxSugar für npy
    """
    def __init__(self, name, default_value=None):
        super().__init__(name, 'int')
        self.default(default_value)
        self.is_pos = False

class PStr(Param):
    """
      Abgeleiter Typ als SyntaxSugar für npy
    """
    def __init__(self, name, default_value=None):
        super().__init__(name, 'str')
        self.default(default_value)
        self.is_pos = False


class Func(Collection):
    lang: str
    name: str
    description: str
    defined_in: str
    doc: str
    source = None
    result_type = None

    def __init__(self, name: str = '', description: str = '', defined_in: str = '', *params):
        super().__init__()
        self.name = ''
        self.lang = 'py'
        self.doc = ''
        self.source = None
        if isinstance(name, types.FunctionType):
            self.init_from_func(name)
        elif isinstance(name, Param):
            params = [name, *params]
        else:
            self.name = name
        if isinstance(description, Param):
            params = [description, *params]
        else:
            self.description = description
        if isinstance(defined_in, Param):
            params = [defined_in, *params]
        else:
            self.defined_in = defined_in
        self.items = params
        for param in self.items:
            param.func = self

    def __contains__(self, item):
        if isinstance(item, str):
            return self.contains_name(item)
        return False

    def result(self, type=None):
        if type is not None:
            self.result_type = type
        return self.result_type

    def init_from_func(self, func: types.FunctionType):
        self.name = func.__name__
        sig = inspect.signature(func)
        self._init_doc(func.__doc__)
        self.source = func
        for param in sig.parameters.values():
            p = Param(param.name)
            if param.default != inspect.Parameter.empty:
                p.default_value = param.default
            self.items.append(p)

    def _init_doc(self, doc):
        self.doc = doc
        # TODO parse doc

    def for_py(self):
        ps = ','.join(map(lambda p: p.to_html(), self.items))
        s = f'{self.name} ({ps})'
        return s

    def for_esp(self):
        ps = ' '.join(map(lambda p: p.to_html(), self.items))
        s = f'{self.name} {ps}'
        return s

    def for_npy(self):
        ps = ' '.join(map(lambda p: p.to_html(), self.items))
        s = f'{self.name} {ps}'
        return s

    def to_html(self):
        lng = getattr(self, 'for_' + self.lang, self.for_py)
        s = lng()
        s += f'<br />{self.description}'
        return w.div(s, _class='Func', style='border: 1px #444 solid; padding: 5px; margin: 5px;')

    def to_form(self):
        p = '<form >'
        for pa in self:
            p += pa.to_input()
        p += '</form>'
        return p

    def to_text(self):
        ps = ' '.join(map(lambda p: p.to_text(), self.items))
        s = f'{self.name} {ps}'
        return s

    def is_direct_callable(self):
        i = 0
        for p in self.items:
            if p.default_value is None:
                i += 1
        return i == 0

    def to_dict(self, params={}):
        res = {}
        for p in self.items:
            if p.name in params:
                res[p.name] = params[p.name]
            else:
                res[p.name] = p.default_value
        res['title'] = str(res)
        return res

    def to_q(self):
        return w.ql(self.to_dict())

    def call_on(self, obj, params):
        func = getattr(obj, self.name)
        ps = {}
        for p in self.items:
            if p.name in params:
                ps[p.name] = params[p.name]
        ps.pop('op')
        return func(**ps)

    def to_openapi_properties(self):
        """ https://swagger.io/docs/specification/v3_0/components/ """
        res = {}
        for p in self.params:
            pass

    def to_openapi_params(self):
        pass


class Class(Collection):

    def __init__(self, definition=None, *items):
        super().__init__(items)
        self.name = 'Class'
        if definition is not None:
            self._read_cls(definition)

    def field(self, name, type):
        self.items.append(Field(name, type))
        return self

    @staticmethod
    def read_function(member):
        f = Func(member.__name__)
        f.init_from_func(member)
        return f

    def __str__(self):
        return 'class ' + self.name + '{}'

    def read_dict(self, data={}):
        for (k,v) in data.items():
            self.field(k, v)

    def _read_cls(self, definition):
        if isinstance(definition, str):
            definition = u.load_class(definition, False)
        self.name = definition.__name__
        for name in dir(definition):
            member = getattr(definition, name, None)
            if isinstance(member, object) and member.__class__.__name__ == 'function':
                self.append(self.read_function(member))


class Package(Collection):

    lang: str = 'py'

    def __init__(self, lang='py', *items):
        """
        :param lang: [py, esp, npy]
        """
        super().__init__(items)
        self.lang = lang
        for itm in self.items:
            itm.lang = lang

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def append(self, item):
        item.lang = self.lang
        self.items.append(item)

    def to_html(self):
        s = ''
        for item in self.items:
            s += item.to_html()
        return w.div(s, _class='Package')

    def get_direct_callables(self) -> "list[Func]":
        res = []
        for elem in self:
            if isinstance(elem, Func):
                if elem.is_direct_callable():
                    res.append(elem)
        return res
