"""
    Runner-System

    https://bsnx.net/npy/documentation/nwebclient.runner
"""
import threading
import types

import math
import sys
import json
import time
import traceback
import importlib
import urllib.parse
import glob
import requests
import datetime
import subprocess
import base64
import io
import os
import re
import os.path
from os.path import expanduser
import pathlib
import inspect
from threading import Thread
from io import BytesIO
import logging

from nwebclient import web
from nwebclient import base
from nwebclient import util
from nwebclient import ticker
from nwebclient import machine
from nwebclient import NWebClient
from nwebclient import dev


jobrunner = None
current = None

ERROR_SERVER = 500
ERROR_UNKNOWN_JOB_TYPE = 599


class TAG:
    IMAGE = 'image'
    IMAGE_EXTRACTOR = 'image_extract'
    HTML_TRANSFORM = 'html_transform'
    HTML_EXTRACTOR = 'html_extract'
    TEXT_TRANSFORM = 'text_transform'
    """ Zieht Informationen aus einem Text, z.B. Klassifikation """
    TEXT_EXTRACTOR = 'text_extract'
    HARDWARE = 'hardware'


class Ports:
    WS2812 = 2812
    PM2_UI = 7001
    STIRLING_PDF = 7003
    REPL = 7004
    PAPERLESS = 7005
    CHROME = 7006
    NSFW_DETECTOR = 7009
    PORTAINER = 7100
    CAMERA = 7171
    NX3D = 7272
    DOCUMENT_ANALYSIS = 27201


class MoreJobs(Exception):
    """ raise MoreJobs([...]) """
    def __init__(self, jobs=[]):
        self.data = {'jobs': jobs}


def js_functions():
    return web.js_fn('base_url', [], [
        '  var res = location.protocol+"//"+location.host;',
        '  res += "/";'
        '  return res;'
    ]) + web.js_fn('post_url_encode', ['data'], [
        'var formBody = [];',
        'for (var property in data) {',
        '  var encodedKey = encodeURIComponent(property);',
        '  var encodedValue = encodeURIComponent(data[property]);',
        '  formBody.push(encodedKey + "=" + encodedValue);}',
        'return formBody.join("&");'
    ]) + web.js_fn('post', ['data'], [
        'return {method:"POST",',
        ' headers: {'
        '  "Content-Type": "application/x-www-form-urlencoded"',
        ' },',
        ' body: post_url_encode(data)'
        '};'
    ]) + web.js_fn('show_error', ['data'], [
        'const $error = document.querySelector("#error");'
        'console.log(data);',
        'if ($error !== null) {',
        '  const msg = data["error_message"];',
        '  if (msg !== undefined) {',
        '    $error.append(data["error_message"]);',
        '  } else {',
        '    $error.append(JSON.stringify(data) + "\\n")',
        '  }',
        '  if ("trace" in data) {',
        '    $error.append(data["trace"]);',
        '  }',
        '}'
    ]) + web.js_fn('show_result', ['data'], """
        if (data.hasOwnProperty('message')) {
            const $content = document.getElementById('content');
            const $alert = document.createElement('div');
            $alert.classList.add('alert');
            $alert.innerHTML = data['message'];
            $content.prepend($alert);
        }
    """) + web.js_fn('exec_job', ['data', 'on_success=null'], [
        'fetch(base_url(), post(data)).then((response) => response.json()).then( (result_data) => { ',
        '  if (result_data.hasOwnProperty("ui_reload")) {',
        '    location.reload();',
        '  }',
        '  document.getElementById("result").innerHTML = JSON.stringify(result_data, null, 2); ',
        '  if (on_success!==null) {',
        '    on_success(result_data)',
        '  } else {',
        '    show_error(result_data);'
        '  }'
        '});'
    ]) + web.js_fn('exec_job_p', ['data', 'on_success=null'], [
        'for (const [key, value] of Object.entries(data)) {',
        '  if ( (typeof value === "string" || value instanceof String) && value.startsWith("#")) {',
        '    data[key] = document.querySelector(value).value;',
        '  }',
        '}',
        'fetch(base_url(), post(data)).then((response) => response.json()).then( (result_data) => { ',
        '  if (result_data.hasOwnProperty("ui_reload")) {',
        '    location.reload();',
        '  }',
        '  document.getElementById("result").innerHTML = JSON.stringify(result_data); ',
        '  if (on_success!==null) {',
        '    on_success(result_data)',
        '  } else { console.log(result_data); }',
        '});'
    ]) + web.js_fn('observe_value', ['type', 'name', 'selector=null', 'interval=5000'], [
        'if (selector == null) selector = "#"+name;',
        'setInterval(function() {',
        '  exec_job({type:type,getvar:name}, function(result) {',
        '    document.querySelector(selector).innerHTML = result["value"];'
        '  });',
        '}, interval);'
    ])


class Mqtt:

    topic = 'main'
    mqtt = None

    @staticmethod
    def create_client(client_id='npy'):
        import paho.mqtt
        from paho.mqtt import client as mqtt_client
        if paho.mqtt.__version__[0] > '1':
            client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id, transport='tcp')
        else:
            client = mqtt_client.Client(client_id, transport='tcp')
        return client

    def __init__(self, args={}, topic='main', on_message=None):
        try:
            from paho.mqtt import client as mqtt_client
            self.mqtt = self.create_client()
            self.topic = topic
            self.on_message = on_message
            # client.username_pw_set(username, password)
            def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    #self.info("Connected to MQTT Broker. Subscribe to Topic: " + self.MQTT_TOPIC)
                    self.mqtt.subscribe(self.topic)
                else:
                    print("Failed to connect, return code %d\n", rc)

            def on_message_func(client, userdata, msg):
                #print("Received MQTT Message")
                #data = json.loads(msg.payload.decode())
                #client.publish(self.MQTT_RESULT_TOPIC, '')
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
                if self.on_message is not None:
                    self.on_message(msg.payload.decode())

            # def on_log(client, userdata, level, buf):
            #    print("MQTT Log")
            self.mqtt.on_connect = on_connect
            self.mqtt.on_message = on_message_func
            self.success = True
            # client.on_log = on_log
            self.mqtt.connect_async(args.get('MQTT_HOST', '127.0.0.1'), args.get('MQTT_PORT', 1883), keepalive=65530)
            #if forever:
            #    self.mqtt.loop_forever()
            #else:
            self.mqtt.loop_start()
        except Exception as e:
            print("Error: MQTT: " + str(e))
            self.success = False

    def publish(self, topic, message):
        if self.mqtt is not None:
            self.mqtt.publish(topic, message)

    def __call__(self, *args, **kwargs):
        if self.mqtt is not None:
            self.mqtt.publish(self.topic, args[0])


def remote(url, data={}, **kwargs):
    data = {**data, **kwargs}
    if url.startswith(':'):
        url = 'http://127.0.0.1' + url
    try:
        resp = requests.post(url, data)
        return resp.json()
    except Exception as e:
        return {'success': False, 'message': str(e)}


class BaseJobExecutor(base.Base):
    """
        BaseJobExecutor
            execute(data:dict)

        https://bsnx.net/npy/documentation/nwebclient.runner:BaseJobExecutor
    """

    stdout: util.LimitStrList
    param_names: dict = {}
    var_names: list = []
    event_defs: list = []
    event_listener: dict = {}

    def __init__(self, type=None):
        super().__init__()
        if type is not None:
            self.type = type
        self.signatures = dev.Package(lang='npy')
        self.stdout = util.LimitStrList(15)
        self.param_names = {}
        self.var_names = []
        self.event_defs = []
        self.event_listener = {}

    def __str__(self):
        return self.__class__.__name__ + "()"

    def opt_dispatcher(self) -> "LazyDispatcher":
        """
            # type: r.LazyDispatcher
        :return:
        """
        return util.Optional(self.getParentClass(LazyDispatcher))

    def opt_nweb(self) -> "nweb.NWeb":
        return util.Optional(getattr(self.getRoot(), 'nweb', None))

    def setting(self, name, default=None):
        if self.getRoot() is not None:
            nw = getattr(self.getRoot(), 'nweb', None)
            if nw is not None:
                return nw.setting(self.type + '.' + name, default)
        return default

    def setting_set(self, name, value):
        if self.getRoot() is not None:
            nw = getattr(self.getRoot(), 'nweb', None)
            if nw is not None:
                if isinstance(value, dict):
                    value = json.dumps(value)
                return nw.set_setting(self.type + '.' + name, value)

    def get_connections(self) -> list:
        """
        :return list[{type}]:
        """
        res = []
        for event_def in self.event_defs:
            res.append(event_def)
        # TODO outgoing event
        return res

    def define_sig(self, *args, **kwargs) -> dev.Func:
        """
            Definiert eine Funktion
            example: define_sig(Param('op'))
        """
        if len(args) == 1 and isinstance(args[0], dev.Func):
            args[0].defined_in = type(self).__name__
            self.signatures.append(args[0])
            return args[0]
        else:
            f = dev.Func(*args, **kwargs)
            f.defined_in = type(self).__name__
            self.signatures.append(f)
            return f

    def define_params(self, param_map):
        """ deprecated """
        for key in param_map.keys():
            self.param_names[key] = param_map[key]

    def define_event(self, type: str):
        """
          Das definierte Event kann in der Klasse mit emit_event ausgelöst und mit add_event_listner hinzugefuegte
          Listener koennen auf das Event reagieren

          @category event
        """
        self.event_defs.append({
            'type': type
        })
        self.event_listener[type] = []

    def define_vars(self, *var_names):
        for var_name in var_names:
            self.var_names.append(var_name)

    def add_event_listener(self, type: str, exec):
        """
        :param exec:  fn(data)
        @category event
        """
        self.event_listener[type].append(exec)

    def pipe_event(self, type: str, newtype=None, extra_data={}):
        """
            @category event
        """
        def pipe_event(data):
            data = {**data, **extra_data}
            if newtype is not None:
                data['type'] = newtype
            self.onParentClass(LazyDispatcher, lambda p: p.execute(data))

        self.add_event_listener(type, pipe_event)
        return self.success('event_piped')

    def emit_event(self, type, **kwargs):
        """
            @category event
        """
        if type in self.event_listener:
            for listener in self.event_listener[type]:
                try:
                    kwargs['type'] = type
                    listener(kwargs)
                except Exception as e:
                    self.error(f"Event {type}: " + str(e))

    def page_events(self, params={}):
        """
        @category event
        """
        p = base.Page(owner=self)
        p.h1("Events")
        for event in self.event_defs:
            p.div(event['type'])
        listener_count = 0
        for items in self.event_listener.values():
            listener_count += len(items)
        p.prop("Event-Listener-Count", listener_count)
        p.hr()
        with p.section(h="Register Event Listener"):
            if 'event_type' in params:
                self.event_process_form(p, params)
            p('<form>')
            p.input('type', type='hidden', value=self.type)
            p.input(self.type, type='hidden', value='events')
            p.form_input('event_type', "Event Type", value='', placeholder='event_type')
            p.form_input('new_type', "New Type", value='', placeholder='Executed Job Type')
            p.form_input('extra', "Extra", value='', placeholder='?key=value')
            p.input('submit', type='submit', value='add listener')
            p('</form>')
        return p.nxui()

    def event_process_form(self, p:base.Page, params={}):
        event_type = params['event_type']
        new_type = params['new_type']
        extra = util.parse_query_string(params['extra'])
        self.pipe_event(event_type, new_type, extra)

    def page_help(self, params={}):
        p = base.Page(owner=self)
        p.pre(self.__doc__)
        args = getattr(self, 'args', {})
        if 'nxdoc' in args:
            p.div(web.a("Documentation", args.get('NPY_PUBLIC_URL', '/') + 'documentation/' + util.fullname(self)))
        return p.nxui()

    def __call__(self, data=None, **kwargs):
        if data is None:
            return self.execute(kwargs)
        else:
            return self.execute(data)

    def prn(self, msg):
        self.stdout.append(msg)
        super().prn(msg)

    def js(self):
        return js_functions()

    def success(self, msg='ok', **kwargs):
        """
          kwargs: [ui_reload, ui_target]

          :param msg:
          :param kwargs :
          :param ui_reload gibt an ob die Webseite neu geladen werden soll:
          :return:
        """
        return {'success': True, 'message': msg, **kwargs}

    def fail(self, msg='', **kwargs):
        self.stdout.append('ERROR: Job Fail.' + str(msg))
        return {'success': False, 'message': msg, **kwargs}

    def emit_var_change(self, name, newvalue):
        self.emit_event('change_' + name, **{'old': self.get_var(name=name), 'new': newvalue})

    def set_var(self, data):
        name = data['setvar']
        setter = getattr(self, 'set_' + name, None)
        if setter is not None:
            setter(data['value'])
        else:
            self.emit_var_change(name, data['value'])
            setattr(self, name, data['value'])
        return self.success('Var Set (BaseJobExecutor)', ui_reload=True)

    def get_var(self, data=None, name=None, direct=False):
        if data is not None:
            name = data['getvar']
        value = None
        getter = getattr(self, 'get_' + name, None)
        if getter is not None:
            value = getter()
        else:
            value = getattr(self, name, '')
        if isinstance(value, base.Base):
            value = str(value)
        if direct:
            return value
        else:
            return {'success': True, 'value': value}

    def execute_operation(self, data):
        op_name = data['op']
        op = getattr(self, 'execute_' + op_name, None)
        if op is not None:
            return op(data)
        elif self.signatures.contains_name(op_name):
            sig = self.signatures[op_name]
            data.pop('op')
            return sig.call_on(self, data)
        else:
            return self.fail('operation not exists, ' + op_name)

    def execute(self, data):
        if 'setvar' in data and data['setvar'] in self.var_names:
            return self.set_var(data)
        elif 'getvar' in data:  # and data['getvar'] in self.var_names:
            return self.get_var(data)
        elif 'pipe_event' in data:
            return self.pipe_event(data['event_type'], data['new_type'], data.get('extra', {}))
        elif '__str__' in data:
            return {'success': True, 'value': self.__str__()}
        elif '__repr__' in data:
            return {'success': True, 'value': self.__repr__()}
        elif 'op' in data:
            return self.execute_operation(data)
        elif 'stdout' in data:
            return self.success('ok', value=self.stdout.__str__())
        elif 'page' in data:
            return self.api_page(data)
        else:
            return self.fail('Unknown Operation (BaseJobExecutor)', request_keys=list(data.keys()))

    def canExecute(self, data):
        return True

    def api_page(self, params={}):
        page_name = params['page']
        part = getattr(self, 'part_' + page_name, None)
        if part is None:
            return self.fail('no part')
        else:
            p = base.Page(owner=self)
            part(p, params)
            return self.success(content=str(p))

    def page_index(self, params={}):
        return self.page_intern(params)

    def page_intern(self, params={}):
        p = base.Page(owner=self)
        p.h1(self.__class__.__name__)
        self.part_index(p, params)
        p(self.html_info())
        p(self.html_modules())
        # TODO show execute form
        self.part_intern_links(p)
        return p.nxui(params)

    def part_intern_links(self, p):
        items = [
            web.a("StdOut", self.link(self.part_stdout)),
            web.a("Events", self.link('events')),
            web.a("Vars", self.link('reflect')),
            web.a("Help", self.link('help')),
            web.a("Run", self.link(self.part_run)),
            web.a("OpenAPI", self.link(self.page_openapi)),
            web.a("Sigs", self.link(self.part_sigs)),
            web.a("Buttons", self.link(self.part_buttons))
        ]
        p.ul(items, _class=web.CSS.UL_MENU)


    def page_reflect(self, params={}):
        p = base.Page(owner=self)
        p.h1("Reflect")
        for name in self.var_names:
            v = str(self.get_var(name=name, direct=True))
            if 'extend' in params:
                p.form_input(name, name, value=v, id=name)
                p.div(web.a("Watch", self.link(self.part_varwatch, name=name)))
                p.div(web.a("Graph", self.link(self.part_vargraph, name=name)))
                p.div(self.action_btn_parametric("Set", dict(type=self.type, setvar=name, value='#'+name)))
            else:
                p.prop(name, v)
        p.right(web.a("Extend", web.ql(params, {'extend':1})))
        return p.nxui()

    def part_vargraph(self, p: base.Page, params={}):
        name = params['name']
        p('<canvas id="chart"></canvas>')
        p.script('/static/js/chartjs/chartjs.js')
        p.script('/static/js/chartjs/streaming.js')
        p.script('/static/js/chartjs/adapter-date.js')
        p.script("""
          
          const onRefresh = chart => {
              const url = '/?type="""+self.type+"""&getvar="""+name+"""';
              $.get(url, function(data) {
                  data = JSON.parse(data);
                  const now = Date.now();
                  chart.data.datasets.forEach(dataset => {
                    dataset.data.push({
                      x: now,
                      y: data['value']
                    });
                  });
              });
            };
            $(function() {
                const ctx = document.getElementById('chart');
                window.chart = new Chart(ctx, {
                 type: 'line',
                 data:  {
                    datasets: [
                        {   label: 'Value',
                            borderColor: 'red',
                            data: []}
                    ]
                 },
                 options: {
                    scales: {
                      x: {
                        type: 'realtime',
                        realtime: {
                          duration: 120000,
                          refresh: 2000,
                          delay: 4000,
                          onRefresh: onRefresh
                        }
                      },
                      y: {
                        title: {
                          display: true, text: 'Value'
                        }
                      }
                    },
                    interaction: { intersect: false }
                 }
            });
          });
        """)
        p.prop(name, str(self.get_var(name=name, direct=True)))

    def part_varwatch(self, p: base.Page, params={}):
        name = params['name']
        p.prop(name, str(self.get_var(name=name, direct=True)))
        p.js_ready('setTimeout(function() { window.location.reload(true); }, 5000);')

    def link(self, page, append='', **kwargs):
        try:
            if isinstance(page, types.MethodType):
                page = page.__name__[5:]
            if len(kwargs) > 0:
                if append == '':
                    append = urllib.parse.urlencode(kwargs)
                else:
                    append += '&' + urllib.parse.urlencode(kwargs)
            return f'?type={self.type}&{self.type}={str(page)}&' + str(append)
        except Exception as e:
            print(str(e))
            return '?LINK-ERROR&msg=BaseJobExecutor.link&' + str(e)

    def part_index(self, p: base.Page, params={}):
        pass

    def part_run(self, p: base.Page, params={}):
        for sig in self.signatures:
            if sig.is_direct_callable():
                data = {'type': self.type, 'op': sig.name}
                p.div(self.exec_btn(sig.name, data))
        p.pre('', id='result')

    def page_var(self, params={}):
        p = base.Page(owner=self)
        var_name = params.get('varname', 'varname')
        v = self.execute({'getvar': var_name}).get('value', 0)
        p.h1("Var")
        p.prop(var_name, v, id=var_name)
        from nwebclient import nts
        guid = self.type+'.' + var_name
        js = 'document.getElementById("'+var_name+'").innerHTML = "'+str(v)+'";'
        nts.nx_channel_html_part(guid, js, console=False)
        self.periodic(3, lambda: nts.nx_channel_emit(guid, v))
        return p.nxui()

    def part_stdout(self, p:base.Page, params={}):
        p.pre(str(self.stdout))

    def html_info(self):
        return web.div("Params:" + ','.join(self.param_names)) + web.div("Vars:" + ','.join(self.var_names))

    def html_modules(self):
        ms = getattr(self, 'MODULES', [])
        return web.div("Modules: " + str(ms))

    def page(self, params={}):
        try:
            page_name = params.get(getattr(self, 'type', 'page'), 'index')
            page = getattr(self, 'page_' + page_name, None)
            if page is None:
                part = getattr(self, 'part_' + page_name, None)
                if part is None:
                    page = self.page_index
                else:
                    p = base.Page(owner=self)
                    part(p, params)
                    return p.nxui()
            return page(params)
        except Exception as e:
            p = base.Page(owner=self)
            p.h1("Exception")
            p.p(str(e))
            p.pre(''.join(traceback.format_tb(e.__traceback__)))
            return p.nxui()

    def setupRestApp(self, app):
        pass

    def action_btn(self, data={}, css_class=None, **kwargs):
        if not data:
            data = kwargs
        return web.button_js(data.get('title', "Execute"), 'exec_job('+json.dumps(data)+');', css_class=css_class)

    def action_btn_parametric(self, title, data={}, on_success='null', css_class=None, **kwargs):
        if not data:
            data = kwargs
        return web.button_js(title, 'exec_job_p('+json.dumps(data)+', '+on_success+');', css_class=css_class)

    def to_text(self, result):
        return json.dumps(result, indent=2)

    @classmethod
    def pip_install(cls):
        print("PIP Install")
        try:
            m = ' '.join(cls.MODULES)
            exe = sys.executable + ' -m pip install ' + m
            print("Install: " + exe)
            subprocess.run(exe.split(' '), stdout=subprocess.PIPE)
            print("Install Done.")
        except AttributeError:
            print("No Modules to install.")

    def exec_btn(self, title, data=None, **kwargs):
        if data is None:
            data = kwargs
        return web.button_js(title, 'exec_job('+json.dumps(data)+');')

    def page_openapi(self, params={}):
        p = base.Page(owner=self)
        from nwebclient import openapi
        p(openapi.page_part(self.link(self.page_openapi_json)))
        return p.nxui()

    def page_openapi_json(self, params={}):
        from nwebclient import openapi
        api = openapi.OpenApi()
        for s in self.signatures:
            api.add_route('/', parameters=s.to_openapi_params())
        return api.to_openapi_json()

    def part_sigs(self, p: base.Page, params={}):
        for sig in self.signatures:
            p(sig.for_npy())
            # sig.to_form()
            p('<hr />')

    def part_buttons(self, p: base.Page, params={}):
        for sig in self.signatures:
            if sig.is_direct_callable():
                p(self.action_btn(sig.to_dict()))

    def ui_runner_link(self, type:str, spec, params={}) -> str:
        """
        @param type:
        @param spec: Npy-Runner-Spec e.g. "nxbot:MyRunner(42)"
        @param params:
        @return:

        """
        parent = self.getParentClass(LazyDispatcher)
        if parent is not None:
            if 'create_type' in params:
                parent.loadDict({type: spec})
            if parent.support_type(type):
                return web.a(type, f'?type={type}')
            else:
                return web.a("create type " + type, '/pysys/registry_show?p_name='+type)
        else:
            return ''


class LazyDispatcher(BaseJobExecutor):
    key = 'type'
    classes = {}
    instances: dict[str, BaseJobExecutor] = {}
    args = {}
    def __init__(self, key='type', args:util.Args={}, **kwargs):
        super().__init__()
        self.key = key
        self.args = args
        self.classes = {}
        self.instances = {}
        self.trigger = {}
        self.loadDict(kwargs)

    def __iter__(self):
        return self.instances.values().__iter__()

    def __repr__(self):
        return 'LazyDispatcher('+str([*self.classes.keys(), *self.instances.keys()])+')'

    def supported_types(self):
        return set([*self.classes.keys(), *self.instances.keys()])

    def support_type(self, type) -> bool:
        return type in self.supported_types()

    def loadDict(self, data):
        """
        :param data:
        :return:
        """
        self.info("loadDict("+str(data)+")")
        if data is None:
            return
        for k in data.keys():
            try:
                v = data[k]
                if isinstance(v, str):
                    if v.startswith('?'):
                        self.execute(v)
                    else:
                        try:
                            self.info("type:"+k+" "+v)
                            self.classes[k] = self.create_class(v)
                        except ModuleNotFoundError as e:
                            self.error(f"Error: type: {k}, Modul {v} not found. (LazyDispatcher) Exception: {e}")
                elif isinstance(v, dict) and self.key in v:
                    self.load_dict_entry(v)
                else:
                    self.loadRunner(k, v)
            except Exception as e:
                self.error("Error: Load Runner " + k)
                self.error(e)
        return self.success('loaded')

    def load_dict_entry(self, data: dict):
        if 'class' in data:
            cls = data['class']
            data.pop('class')
            self.create_class(cls, data)
        else:
            self.execute(data)

    def _setup_object(self, obj: BaseJobExecutor) -> BaseJobExecutor:
        try:
            for sig in obj.signatures:
                sig.append(dev.PStr('type', obj.type))
        except Exception as e:
            obj.error(e)
        return obj

    def create_class(self, v, ctor_args={}):
        if not isinstance(v, str):
            return self._setup_object(v)
        if '(' in v:
            obj = util.create_instance(v, args=self.args, dispatcher=self, u=util)
        else:
            obj = util.load_class(v, True, ctor_args, self.args)
        # self.info("create_class: " + str(getattr(obj, 'args', '---')))
        if isinstance(obj, base.Base):
            self.addChild(obj)
        return self._setup_object(obj)

    def add_runner(self, runner):
        """
        @see loadRunner
        :param runner BaseJobExecutor:
        :return:
        """
        return self.loadRunner(runner.type, runner)

    def loadRunner(self, key, spec):
        self.info(f"Load runner: " + str(spec) + " key: " + str(key))
        try:
            if isinstance(spec, dict) and 'py' in spec:
                runner = eval(spec['py'], globals())
                self.setupRunner(runner)
                self.instances[key] = runner
            else:
                spec.type = key
                self.instances[key] = spec
                self.setupRunner(spec)
        except Exception as e:
            self.error("loadRunner faild. " + str(e))
            return self.fail(str(e))
        return {'success': True, 'type': key}

    def setupRunner(self, runner):
        self.addChild(runner)
        self._setup_object(runner)
        webapp = getattr(self.owner(), 'web', None)
        if webapp is not None:
            self.info("Loading Routes " + str(webapp) + " on " + str(runner))
            runner.setupRestApp(webapp)
        return runner

    def remove(self, data: dict):
        job_type = data['remove']
        self.classes.pop(job_type)
        self.instances.pop(job_type)
        return self.success('removed')

    def execute_sub(self, sub, data):
        result = sub.execute(data)
        t = data[self.key]
        if t in self.trigger:
            params = result.copy()
            params[self.key] = self.trigger[t]
            self.execute(params)
        return result

    def is_regex_type(self, type_name):
            return '|' in type_name or '*' in type_name

    def execute_multi(self, type, data={}):
        res = {}
        results = []
        for t in self.supported_types():
            if re.search(type, t) is not None:
                data[self.key] = t
                r = self.execute(data)
                results.append(r)
                res = util.merge(res, r)
        res['results'] = results
        return res

    def execute(self, data):
        if isinstance(data, str) and data.startswith('?'):
            data = util.parse_query_string(data)
        if self.key in data:
            t = data[self.key]
            if self.is_regex_type(t):
                return self.execute_multi(t, data)
            if t in self.instances:
                data = self.execute_sub(self.instances[t], data)
            elif t in self.classes:
                c = self.classes[t]
                self.instances[t] = self.setupRunner(self.create_class(c))
                data = self.execute_sub(self.instances[t], data)
            else:
                data = self.execute_internal_action(data, t)
        else:
            data = super().execute(data)
        return data

    def execute_internal_action(self, data, t):
        if 'list_runners' == t:
            return {'names': list(self.classes.keys())}
        elif 'remove' == t:
            return self.remove(data)
        elif 'load_runners' == t:
            return self.loadDict(data.get('runners', {}))
        else:
            data['success'] = False
            data['error_code'] = ERROR_UNKNOWN_JOB_TYPE
            data['message'] = 'Unkown Type (LazyDispatcher)'
            self.error(f"Unknown Type: {t}")
            return data

    def get_runner(self, type) -> BaseJobExecutor:
        if type in self.instances:
            return self.instances[type]
        elif type in self.classes:
            c = self.classes[type]
            self.instances[type] = self.setupRunner(c())
            return self.instances[type]
        return None

    def get_runner_by_class(self, cls_name) -> "list[BaseJobExecutor]":
        res = []
        for c in self.instances.values():
            if c.__class__.__name__ == cls_name:
                res.append(c)
        return res

    def canExecute(self, data) -> bool:
        if self.key in data:
            return data[self.key] in self.classes or data[self.key] in ['list_runners']
        return False

    def part_readme(self, p: base.Page, params={}):
        h = pathlib.Path.home() / 'README.md'
        if h.is_file():
            p.markdown(util.file_get_text(str(h)))

    def is_selected(self, runner, params={}):
        if 'tag' in params:
            return params['tag'] in getattr(runner, 'TAGS', [])
        elif 'starred' in params:
            return getattr(runner, 'starred', False)
        return True

    def write_to(self, p: base.Page, summary=False, params={}):
        p.h2('Dispatcher')
        self.part_readme(p)
        for key in self.instances:
            if self.is_selected(self.instances[key], params):
                p('<div class="runner_preview part_box" title="'+key+'">')
                p.h3("Runner: " + key)
                p.div("Parameter: " + ','.join(self.instances[key].param_names.keys()))
                p.div("Vars: " + ','.join(self.instances[key].var_names))
                if isinstance(self.instances[key], BaseJobExecutor) and self.instances[key].has_method('write_to'):
                    self.instances[key].write_to(p, summary=True)
                p.div(web.a(key, f'/pysys/dispatcher?type={key}')+' - '+web.a("Exec", f'/pysys/runner-ui?type={key}'))
                p('</div>')
        p.h2('Loading Runner')
        for key in self.classes:
            if key not in self.instances:
                p.div("Load: " + self.action_btn({'title': key, 'type': key, 'ui_reload': True}))
        p.h2('Execute')
        p.ul([
            web.a("Runner-UI", '/pysys/runner-ui'),
            web.a("Results", '/pysys/job-results'),
            web.a("All Runners", '/pysys/registry'),
            web.a("Graph", '?type=graph'),
            web.a("Transform & Pipeline", '?type=dispatcher_create')
        ], _class=web.CSS.UL_MENU)

    def get_events(self):
        res = util.List()
        for itm in self.instances.values():
            res.add_all(map(lambda x: {'runner': itm, **x}, itm.event_defs))
        return res

    def page_dispatcher_create(self, params={}):
        p = base.Page(owner=self)
        with p.section(h="Transform"):
            Transform.create_form(p)
        p.h3("Pipelines")
        for itm in util.List(self.instances.values()).classes(Pipeline):
            p.div(itm.type)
        p.h3("Create Pipeline")
        p("Type der gepipelines werden soll")
        p("TODO besser eine sig?")
        for ev in self.get_events():
            p.div(ev['runner'].type + ":  " + ev['type'])
            p.pre(ev) # type ist name, runner

        return p.nxui()

    def nav(self, p: base.Page):
        p.a("Runner", '/pysys/runner')

    def page_dispatch(self, params={}):
        runner = self.get_runner(params['type'])
        if runner is not None:
            page = getattr(runner, 'page', None)
            if page is not None:
                return page(params)
            else:
                return "<h1>404, no page() in Runner</h1>"
        else:
            page = getattr(self, 'page_' + params['type'], None)
            if page is not None:
                return page(params)
            else:
                return "404, no page() in Dispatcher"

    def page_dispatch_cls(self, params={}):
        runner = self.get_runner_by_class(params['cls'])
        p = base.Page(owner=self)
        params['page'] = p
        for r in runner:
            page = getattr(r, 'page', None)
            if page is not None:
                page(params)
        self.nav(p)
        return p.nxui()

    def page_dispatch_multi(self, params={}):
        ts = params.get('types', '').split(',')
        p = base.Page(owner=self)
        params['page'] = p
        for t in ts:
            r = self.get_runner(t)
            page = getattr(r, 'page', None)
            if page is not None:
                page(params)
        self.nav(p)
        return p.nxui()

    def page_graph(self, params={}):
        from nwebclient import visual as v
        p = base.Page(owner=self)
        g = web.LiteGraph()
        g.item_name = lambda item: item.type

        g.items.add_all(map(lambda x: v.Box(x), self.instances.values()))
        g.items.layout_non_overlapping()
        for runner in self.instances.values():
            for connection_target in runner.get_connections():
                g.create_connection(runner.type, connection_target['type'])
        g.add_to(p)
        return p.nxui()

    def page(self, params={}):
        p = base.Page(owner=self)
        opts = {'theme': params.get('theme', base.Page.theme)}
        if 'type' in params:
            return self.page_dispatch(params)
        else:
            opts['title'] = 'Dispatcher'
            self.write_to(p, params=params)
        return p.nxui(opts)

    def nxitems(self):
        res = []
        for key in self.instances:
            res.append({'title': key, 'url': '/pysys/dispatcher?type='+key})
        return res

    def setupRestApp(self, app):
        from flask import request
        if self.args is not None:
            base.Page.theme = self.args.get('theme', None)
        try:
            app.add_url_rule('/pysys/dispatcher', 'dispatcher', view_func=lambda: self.page_dispatch({**request.args, **request.form, **request.files}), methods=['GET', 'POST'])
            app.add_url_rule('/pysys/cls', 'dispatcher_cls', view_func=lambda: self.page_dispatch_cls({**request.args}))
            app.add_url_rule('/pysys/multi', 'dispatcher_multi', view_func=lambda: self.page_dispatch_multi({**request.args}))
            for runner in self.instances.values():
                runner.setupRestApp(app)
        except Exception as e:
            self.error(str(e))

    def byTag(self, tag: str) -> list:
        res = []
        for r in self.instances.values():
            tags = getattr(r, 'TAGS', [])
            if tag in tags:
                res.append(r)
        return res

    def get_direct_callables(self):
        res = util.List()
        for elem in self.instances.values():
            res.add_all(elem.signatures.get_direct_callables())
        return res


class RunnerLogHandler(logging.Handler):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    def emit(self, record):
        # Hier wird jede Lognachricht verarbeitet
        msg = self.format(record)
        self.owner.info(msg + " " + record.levelname)


class Multi(BaseJobExecutor):

    def __init__(self):
        super().__init__()
        self.type = 'multi'

    def execute_on_parent(self, data):
        try:
            return self.owner().execute(data)
        except Exception as e:
            return self.fail(str(e))

    def execute_jobs(self, jobs):
        res = {'success': True}
        for key in jobs.keys():
            self.info("Multi Start " + str(key))
            res[key] = self.execute_on_parent(jobs[key])
        return res

    def execute(self, data):
        if 'jobs' in data:
            return self.execute_jobs(data['jobs'])
        return super().execute(data)


class JobRunner(base.Base):

    MQTT_TOPIC = 'jobs'
    MQTT_RESULT_TOPIC = 'result'

    """
      Werte aus dem JobAuftrag die nach einer Ausführung übernommen werden
    """
    result_job_keys = ['guid', 'ui_reload', 'ui_target']
    
    counter = 0 
    
    # Start Time
    start = None
    last_job_time = None
    last_http_time = None  # Zeit des letzten Requests, um zu schauen ob eine Verbindung zustande gekommen ist.

    args = {}
    
    jobexecutor = None
    
    web = None

    nweb = None
    
    def __init__(self, jobexecutor, args: util.Args = {}):
        super().__init__()
        self.jobexecutor = jobexecutor
        self.addChild(self.jobexecutor)
        if args is None:
            args = util.Args()
        print(str(args), flush=True)
        self.args = args
        if JobRunner.nweb is None:
            JobRunner.nweb = self.init_nweb()

    def init_nweb(self):
        try:
            from nweb import DB, NWeb
            if 'DB' in self.args:
                nw = NWeb({}, DB(self.args['DB']))
                nw.create_tables()
                return nw
        except Exception as e:
            print("NWeb Persdistence not available. " + str(e))
        return self.nweb

    def __getitem__(self, item):
        return self.jobexecutor.get_runner(item)

    def __repr__(self):
        return '{JobRunner: ' + self.jobexecutor.__repr__() + '}'

    def info(self, msg):
        #out = lambda msg: "[JobRunner] "+str(msg)
        print("[JobRunner] " + msg)

    def __call__(self, job):
        return self.execute_job(job)

    def execute(self, job):
        return self.execute_job(job)

    def after_job(self, job, result):
        if 'next' in job:
            pass
            # TODO transform result
            # TODO execute result
        return result

    def execute_job(self, job):
        self.last_job_time = datetime.datetime.now()
        try:
            result = self.jobexecutor(job)
            result = self.after_job(job, result)
        except MoreJobs as mj:
            result = self.execute_data(mj.data)
        except Exception as e:
            self.info('Error: Job faild')
            result = job
            result['success'] = False
            result['error'] = True
            result['error_code'] = ERROR_SERVER
            result['error_message'] = str(e)
            result['trace'] = str(traceback.format_exc())
        if 'type' in job and isinstance(result, dict):
            result['job_type'] = job['type']
        if isinstance(result, dict):
            for key in self.result_job_keys:
                if key in job:
                    result[key] = job[key]
            # TODO check if inputs defined
        return result

    def execute_data(self, data):
        self.start = datetime.datetime.now()
        result = {'jobs': []}
        for job in data['jobs']:
            job_result = self.execute_job(job)
            result['jobs'].append(job_result)
            self.counter = self.counter + 1
        delta = (datetime.datetime.now()-self.start).total_seconds() // 60
        self.info("Duration: "+str(delta)+"min")
        return result

    def execute_file(self, infile, outfile=None):
        try:
            data = json.load(open(infile))
            result = self.execute_data(data)
            outcontent = json.dumps(result)
            print(outcontent)
            if not outfile is None:
                if outfile == '-':
                    print(outcontent)
                else:
                    with open(outfile, 'w') as f:
                        f.write(outcontent)
        except Exception as e:
            self.info("Error: " + str(e))
            self.info(traceback.format_exc());
            self.info("Faild to execute JSON-File "+str(infile))

    def execute_mqtt(self, args, forever=False):
        from paho.mqtt import client as mqtt_client
        if 'mqtt_topic' in args:
            self.MQTT_TOPIC = args['mqtt_topic']
        if 'mqtt__result_topic' in args:
            self.MQTT_RESULT_TOPIC = args['mqtt_result_topic']
        self.mqtt = Mqtt.create_client('NPyJobRunner')
        self.info("Starting MQTT")

        # client.username_pw_set(username, password)
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.info("Connected to MQTT Broker. Subscribe to Topic: " + self.MQTT_TOPIC)
                self.mqtt.subscribe(self.MQTT_TOPIC)
            else:
                self.info("Failed to connect, return code %d\n", rc)

        def on_message(client, userdata, msg):
            print("Received MQTT Job")
            try:
                data = json.loads(msg.payload.decode())
                result = self.execute(data)
                client.publish(self.MQTT_RESULT_TOPIC, json.dumps(result))
                #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            except Exception as e:
                print("MQTT Job Failed")
                print(str(e))

        # def on_log(client, userdata, level, buf):
        #    print("MQTT Log")
        self.mqtt.on_connect = on_connect
        self.mqtt.on_message = on_message
        # client.on_log = on_log
        self.mqtt.connect_async(args['MQTT_HOST'], args.get('MQTT_PORT', 1883), keepalive=65530)
        if forever:
            self.mqtt.loop_forever()
        else:
            self.mqtt.loop_start()

    def execute_queue(self):
        if os.path.isfile('nweb.db'):
            self.execute_nwebdb()
        if os.path.isfile('jobs.json'):
            self.execute_jobs()

    def execute_jobs(self, filename='jobs.json', result_filename=None):
        with open(filename, 'r') as f:
            jobs = json.load(f)
            job_results = []
            for job in jobs:
                job_results.append(self.execute_job(job))
            if result_filename is not None:
                with open(result_filename, 'w') as rf:
                    json.dump({'items': job_results}, rf)

    def execute_nwebdb(self):
        import sqlite3
        connection = sqlite3.connect('nweb.db')
        try:
            cur = connection.cursor()
            cur.execute("SELECT id, data FROM nweb_jobs")
            for job in cur.fetchall():
                res = self.execute(json.loads(job[1]))
                s = json.dumps(res)
                cur.execute("UPDATE nweb_jobs SET result = ? WHERE id = ?", (s, job[0]))
            cur.close()
        finally:
            connection.close()

    def _index(self, request):
        if 'NxRust' in request.headers.get('user-agent', 'DefaultAgent'):
            return "use type=xy var=42"
        elif self.ui_enabled():
            return self.ui_index()
        else:
            return '{"success": false, "message": "No Input"}'

    def ui_index(self):
        return web.style('body {background-color: black; color: #ddd; }') + "Job Endpoint. " + web.a("Runner", '/pysys/runner')

    def execute_rest_job(self):
        from flask import Flask, request
        data = {**request.args.to_dict(), **request.form.to_dict()}
        if len(data) == 0:
            return self._index(request)
        result = self.execute_job(data)
        try:
            if isinstance(result, dict):
                return json.dumps(result)
            else:
                return result
        except Exception as e:
            return json.dumps({
                'success': False,
                'message': str(e),
                'type': str(type(result)),
                'value': str(result),
                'trace': str(traceback.format_exc())})

    def ui_enabled(self):
        return 'disable-ui' not in self.args

    def before_request(self):
        self.last_http_time = time.time()

    def nxname(self):
        from nwebclient import nx
        return nx.get_name()


    def execute_rest(self, port=8080, run=True, route='/', app=None):
        """
        :param run: True, False, 'async'
        """
        self.info("Starting webserver")
        from flask import Flask, request
        if app is None:
            app = Flask(__name__, static_folder=None)
        app.before_request(self.before_request)
        #@app.route('/')
        #def home():
        #    return json.dumps(execute_data(request.form.to_dict(), jobexecutor))
        # Add To Root
        self.info("Executor: " + str(type(self.jobexecutor).__name__))
        app.add_url_rule(route, 'job_runner', view_func=lambda: self.execute_rest_job(), methods=['GET', 'POST'])
        if self.ui_enabled():
            self.jobexecutor.setupRestApp(app)
            app.add_url_rule('/pysys/job-counter', 'job_counter', view_func=lambda: str(self.counter))
            app.add_url_rule('/pysys/job-results', 'job_results', view_func=lambda: self.page_results())
            app.add_url_rule('/pysys/runner-ui', 'r_runner_ui', view_func=lambda: self.page_ui(request.args.to_dict()))
            app.add_url_rule('/pysys/runner', 'r_runner', view_func=lambda: self.jobexecutor.page(web.all_params()))
            app.add_url_rule('/pysys/registry', 'r_registry', view_func=lambda: self.page_registry(request.args.to_dict()))
            app.add_url_rule('/pysys/registry_show', 'r_registry_show', view_func=lambda: self.page_registry_show({**request.args.to_dict(), **request.form.to_dict()}), methods=['GET', 'POST'])
            app.add_url_rule('/pysys/last_job_time', 'r_last_job_time', view_func=lambda: str(self.last_job_time))
            app.add_url_rule('/nxname', 'r_nxname', view_func=self.nxname)
            self.web = web.route_root(app, self.getRoot())
        else:
            self.web = app
        if run is True:
            self.__run(app, port)
        elif run == 'async':
            t = Thread(target=lambda: self.__run(app, port))
            t.start()
        elif run == 'repl':
            t = Thread(target=lambda: self.__run(app, port))
            t.start()
            self.repl()
        return app

    def repl(self):
        from nxbot.system import Repl
        Repl(self)

    def __run(self, app, port):
        self.info("Flask.run(...)")
        if self.ui_enabled():
            self.web.run(app, port=port)
        else:
            app.run(host=self.args.get('HOST', '0.0.0.0'), port=int(port))

    def nxitems(self):
        return [{'title': "Registry", 'url': '/pysys/registry'}, {'title': "Create Job Ui", 'url': '/pysys/runner-ui'},
                {'title': "Runner", 'url': '/pysys/runner'}]

    def page_ui(self, params={}):
        p = base.Page(owner=self)
        p.h1("Runner UI")
        p.script(js_functions()+web.js_fn('add', ['name=""', 'value=""'], """
            var $ctrls = document.getElementById("ctrls");
            var $d = document.createElement("div");
            $d.classList.add("entry");
            $d.innerHTML = '<input class="name" value="'+name+'" placeholder="Key" /><input class="value" value="'+value+'" placeholder="Value" />';
            $ctrls.appendChild($d);
            """)+
            web.js_fn('run', [], [
                'var data = {};'
                'document.querySelectorAll("#ctrls .entry").forEach(function(node) {',
                '  data[node.querySelector(".name").value] = node.querySelector(".value").value;'
                '});',
                'console.log(data);',
                'exec_job(data);'
            ])
        )
        if 'type' in params:
            r = self.jobexecutor.get_runner(params['type'])
            p.div("Job for " + str(params['type']))
            p.div(r.__doc__)
            n = r.param_names
            for key in n:
                p.div(key + ': ' + n[key])
            p.script(web.js_ready('add("type", "'+params['type']+'")'))
        p.div(web.button_js("+", 'add()'), id='ctrls')
        p.div(web.button_js("Run", 'run()'))
        p.div(id='result')
        p.hr()
        p.a("PyModule", 'pymodule')
        p.a("Runner", '/pysys/runner')
        p.h2("About Runner")
        p.div("Job-Count: " + str(self.counter))
        return p.nxui()

    def registry_install(self, name, eps, p):
        try:
            e = eps.select(group='nweb_runner', name=name)[0]
            runner = e.load()
            p.div('Runner geladen')
            # if isinstance(self.jobexecutor, LazyDispatcher):
            res = self.jobexecutor.loadRunner(e.name, runner())
            p.pre(str(res))
            # else:
            #    p.div("Invalid Runner: " +str(type(self.jobexecutor).__name__) + " Valid: LazyDispatcher")
        except ImportError as exception:
            p.div("Runner konnte nicht geladen werden. (ImportError)")
            p.div("Modul: " + str(exception.name))
            p.div(str(exception))
        except Exception as exception:
            p.div("Runner konnte nicht geladen werden. (Exception)")
            p.div(str(exception))

    def page_registry(self, params={}):
        p = base.Page(owner=self)
        from importlib.metadata import entry_points
        eps = entry_points()
        p.h1("Runner Regsitry")
        if 'install' in params:
            self.registry_install(params['install'], eps, p)
        parts = eps.select(group='nweb_runner')
        p('<div class="div_registry_runners">')
        for name in parts.names:
            p(self.div_registry_runner(parts[name]))
        p('</div>')
        p.hr()
        p.a("Runner", '/pysys/runner')
        p.js_ready('enableSearch(".div_registry_runners", ".div_registry_runner")')
        return p.nxui()

    def div_registry_runner(self, part):
        install = web.a("Load", '?install=' + part.name)
        show = web.a("Show", '/pysys/registry_show?p_name=' + part.name)
        return web.div(part.name + " = " + str(part.value) + " " + install + " " + show, _class='div_registry_runner')

    def link_registry_show(self, name):
        return '/pysys/registry_show?p_name=' + name

    def page_registry_show(self, params={}):
        p = base.Page(owner=self)
        from importlib.metadata import entry_points
        eps = entry_points()
        try:
            part = eps.select(group='nweb_runner', name=params['p_name'])[0]
            runner = part.load()
            p.h2("Runner: " + params['p_name'])
            p.prop("Tags", ", ".join(getattr(runner, 'TAGS', [])))
            p.markdown(runner.__doc__)
            ms = getattr(runner, 'MODULES', [])
            if 'pip' in params:
                p(self.registry_pip_install(params, ms))
            if len(ms) == 0:
                p.div("Module: (keine)")
            else:
                p.div("Module: " + ','.join(ms) + " " + web.a("pip install", self.link_registry_show(params['p_name'])+'&pip=install'))
            spec = inspect.getfullargspec(runner)
            self.create_form(p, spec, runner, params)
            p.hr()
            install = web.a("Load", '/pysys/registry?install=' + part.name)
            p.div(install)
        except Exception as e:
            p.div("Error: " + str(e))
        return p.nxui()

    def create_form(self, p: base.Page, spec, runner, params):
        p.div("Constructor")
        p('<form method="POST">')
        ctor_params = {}
        for arg in spec.args:
            if arg != 'self':
                p.div(" - " + arg + web.input(arg))
                if arg in params and params[arg] != '':
                    ctor_params[arg] = params[arg]
        if ('create' in params):
            self.jobexecutor.add_runner(runner(**ctor_params))
        p(web.submit("Erstellen", name='create'))
        p("</form>")

    def registry_pip_install(self, params, modules):
        exe = sys.executable + ' -m pip install ' + ' '.join(modules)
        r = subprocess.run(exe.split(' '), stdout=subprocess.PIPE)
        return web.pre(exe) + web.pre(str(r.stdout)) + web.div(web.a("Back", self.link_registry_show(params['p_name'])))

    def page_results(self):
        p = base.Page()
        p.h1("Results")
        n = NWebClient(None)
        results = n.group('F954BAE7FE404ACE1A40140D66B637DC')
        for result in results.docs():
            p.div("Name: " + str(result.name()))
            p.div("Kind: " + str(result.kind()))
            if result['llm']:
                p.div("Prompt: " + str(result['prompt']))
                p.div("Response: " + str(result['response']))
            #p.div("Type: " + str(result['type']))
            #p.div("Content: " + str(result.content()))
        p.hr()
        p.div(web.a("Runner", '/pysys/runner'))
        return p.nxui()


class MultiExecutor(BaseJobExecutor):
    
    executors = []
    
    def __init__(self, *executors):
        super().__init__()
        self.executors = executors

    def execute(self, data):
        for exe in self.executors:
            if exe.canExecute(data):
                exe(data)

    def canExecute(self, data):
        for exe in self.executors:
            if exe.canExecute(data):
                return True
        return False


class SaveFileExecutor(BaseJobExecutor):
    filename_key = 'filename'
    content_key = 'content'

    def execute(self, data):
        with open(data[self.filename_key], 'w') as f:
            f.write(data[self.content_key])

    def canExecute(self, data):
        return 'type' in data and data['type'] == 'savefile'

    @staticmethod
    def run(data):
        r = SaveFileExecutor()
        return r(data)


class Pipeline(BaseJobExecutor):
    """
      Jobs nacheinander Ausführen
      @see Transform
    """

    executors = []

    def __init__(self, *args):
        super().__init__('pipeline')
        self.executors.extend(args)
        for item in self.executors:
            self.addChild(item)

    def execute(self, data):
        for item in self.executors:
            data = item(data)
        return data

    def part_index(self, p: base.Page, params={}):
        p.h1("Pipeline")
        for item in self.executors:
            p.div("E" + item.type + ": " + item.__class__.__name__)


class Dispatcher(BaseJobExecutor):
    key = 'type'
    runners = {}

    def __init__(self, key='type', **kwargs):
        super().__init__()
        #for key, value in kwargs.items():
        self.key = key
        self.runners = kwargs
        for item in self.runners.values():
            self.addChild(item)

    def execute(self, data):
        if self.key in data:
            runner = self.runners[data[self.key]]
            return runner(data)
        else:
            return {'success': False, 'message': "Key not in Data", 'data': data}

    def canExecute(self, data):
        if self.key in data:
            return data[self.key] in self.runners
        return False


class AutoDispatcher(LazyDispatcher):
    """
       python -m nwebclient.runner --rest --mqtt --executor nwebclient.runner:AutoDispatcher
    """
    def __init__(self, key='type', **kwargs):
        super().__init__(key, **kwargs)
        self.args = util.Args()
        data = self.args.env('runners')
        if isinstance(data, dict):
            self.loadDict(data)
            self.info("Runner-Count: " + str(len(data)))
        elif len(self.classes) == 0:
            print("===================================================================================")
            self.info("Warning: No Runners configurated.")
            self.info("")
            self.info("Edit /etc/nweb.json")
            self.info("{")
            self.info("  \"runners\": {")
            self.info("      <name>: <class>,")
            self.info("      \"print\": \"nwebclient.runner:PrintJob\"")
            self.info("   }")
            self.info("}")
            list_runners()
            print("===================================================================================")


class MainExecutor(AutoDispatcher):
    """
      python -m nwebclient.runner --executor nwebclient.runner:MainExecutor --rest --mqtt
    """
    def __init__(self, **kwargs):
        super().__init__(key='type', pymodule='nwebclient.runner:PyModule')
        self.execute({'type': 'pymodule'})


class RestRunner(BaseJobExecutor):

    ssl_verify = False

    def __init__(self, url, type='rest'):
        super().__init__()
        self.type = type
        self.url = url

    def execute(self, data):
        response = requests.post(self.url, data=data, verify=self.ssl_verify)
        return json.load(response.content)
    

class PrintJob(BaseJobExecutor):
    """ nwebclient.runner.PrintJob """
    
    def __init__(self):
        super().__init__('print')
    
    def execute(self, data):
        print(json.dumps(data, indent=2))
        return self.success()


class ImageExecutor(BaseJobExecutor):
    """

    """
    image = None
    image_key = 'image'

    def load_image(self, filename):
        with open(filename, "rb") as f:
            return base64.b64encode(f.read()).decode('ascii')

    def image_filename(self):
        filename = 'image_executor.png'
        self.image.save(filename)
        return filename

    def get_image(self, key, data):
        """
          URL/Pfad/Base64
          oder key_id für nweb-id
        """
        from PIL import Image
        if key + '_url' in data:
            response = requests.get(data[key + '_url'])
            return Image.open(BytesIO(response.content))
        elif key + '_filename' in data:
            return Image.open(data[key + '_filename'])
        elif key + '_id' in data:
            return NWebClient(data.get('nweb', None)).doc(data[key + '_id']).as_image('m')
        elif key in data:
            if len(data[key]) > 1000:
                image_data = base64.b64decode(data[key])
                return Image.open(io.BytesIO(image_data))
            elif data[key].startswith('/'):
                with open(data[key], "rb") as f:
                    return Image.open(io.BytesIO(f.read()))
            elif data[key].startswith('nweb:'):
                return self.get_nweb_image(data[key], data)
            else:
                image_data = base64.b64decode(data[key])
                return Image.open(io.BytesIO(image_data))
        else:
            return None

    def get_nweb_image(url: str, data={}):
        nc = NWebClient(None)
        id = url.split('/')[-1]
        return nc.doc(id).as_image()

    def read_str(self, s):
        return base64.b64decode(s)

    def is_unset_image(self, data):
        try:
            return 'unset_image' in data and self.image_key in data
        except:
            return False

    def execute(self, data):
        from PIL import Image
        image = self.get_image('image', data)
        if image is not None:
            data = self.executeImage(image, data)
        elif 'file0' in data:
            self.image = Image.open(io.BytesIO(self.read_str(data['file0'])))
            data = self.executeImage(self.image, data)
        if self.is_unset_image(data):
            data.pop(self.image_key)
        return data

    def executeImage(self, image, data):
        return data
    

class NWebDocMapJob(BaseJobExecutor):
    def execute(self, data):
        # python -m nwebclient.nc --map --meta_ns ml --meta_name sexy --limit 100 --meta_value_key sexy --executor nxml.nxml.analyse:NsfwDetector --base nsfw.json
        from nwebclient import nc
        n = NWebClient(None)
        exe = util.load_class(data['executor'], create=True)
        filterArgs = data['filter']
        meta_ns = data['meta_ns']
        meta_name = data['meta_name']
        meta_value_key = data['meta_value_key']
        base  = data['base']
        dict_map = data['dict_map']
        update = data['update']
        limit = data['limit']
        fn = nc.DocMap(exe, meta_value_key, base, dict_map)
        n.mapDocMeta(meta_ns=meta_ns, meta_name=meta_name, filterArgs=filterArgs, limit=limit, update=update, mapFunction=fn)
        data['count'] = fn.count
        return data


class TickerCmd(BaseJobExecutor):
    type = 'ticker_cmd'
    def execute(self, data):
        args = data['args']
        if isinstance(args, str):
            args = args.split(' ')
        data['result'] = self.onParentClass(ticker.Cpu, lambda cpu: cpu.cmd(args))
        return data
        
        
class PyModule(BaseJobExecutor):
    """
      nwebclient.runner:PyModule
    """
    type = 'pymodule'

    def __init__(self):
        super().__init__()

    def js(self):
        return super().js()

    def page_index(self, params={}):
        p = base.Page(owner=self)
        p.h1("PyModule Executor")
        # eval_runner
        # eval_ticker
        p.div('modul.GpioExecutor(17)')
        p.input('py', id='py', placeholder='Python')
        p.input('modul', id='modul', placeholder='Module', value='nwebclient.runner')
        p += web.button_js("Add Runner", 'exec_job({type:"pymodule",modul:document.getElementById("modul").value,eval_runner:document.getElementById("py").value});')
        p += web.button_js("Add Ticker", 'exec_job({type:"pymodule",modul:document.getElementById("modul").value,eval_ticker:document.getElementById("py").value});')
        p.hr()
        p.tag('textarea', "result['value'] = 42;", id='code', spellcheck='false')
        p += web.button_js("Exec", 'exec_job({type:"pymodule",exec:document.getElementById("code").value});')
        p.hr()
        p.div('', id='result')
        return p.nxui()

    def setupRestApp(self, app):
        super().setupRestApp(app)

    def execute(self, data):
        if 'modul' in data:
            modul = importlib.import_module(data['modul'])
            if 'run' in data:
                exe = getattr(modul, data['run'], None)
                return exe(data)
            if 'eval_runner' in data:
                runner = eval(data['eval_runner'], globals(), {'modul': modul})
                r_type = data['new_type'] if 'new_type' in data else runner.type
                return self.owner().loadRunner(r_type, runner)
            if 'file_runner' in data:
                runner = eval(util.file_get_contents(data['file_runner']), globals(), {'modul': modul})
                r_type = data['new_type'] if 'new_type' in data else runner.type
                runner.type = r_type
                return self.owner().loadRunner(r_type, runner)
            if 'eval_ticker' in data:
                ticker = eval(data['eval_ticker'], globals(), {'modul': modul})
                self.getRoot().add(ticker)
                return {'success': True}
            if 'eval' in data:
                res = eval(data['eval'], globals(), {'modul': modul})
                return {'success': True}
        elif 'exec' in data:
            code = data['exec']
            if isinstance(code, list):
                code = "\n".join(code)
            self.info("exec:" + str(code))
            result = {}
            exec(code, globals(), {
                'owner': self,
                'result': result,
                'data': data
            })
            return result
        elif 'file' in data:
            self.execute_file(data, data['file'])
        self.info("Module Unknown")
        return {'success': False, 'message': 'PyModule Unknown', 'request': data}

    def execute_file(self, data, file):
        with open(file, 'r') as f:
            result = {}
            exec(f.read(), globals(), {
                'owner': self,
                'result': result
            })
            return result


class PyEval(BaseJobExecutor):
    """
        Besser code.InteractiveConsole(variables) verwenden, um auch variablen definieren zu können
        >>> import code
        >>> c = code.InteractiveInterpreter({'a': 42})
        >>> c.runcode('print(a)')
        42
        >>> c.runcode('a += 1')
        >>> c.runcode('print(a)')
        43
    """
    type = 'eval'

    def __init__(self):
        super().__init__()
        import code
        self.session = code.InteractiveInterpreter(dict(
            this=self,
            data={},
            state={},
            result={}
        ))
        self.main = ''

    def execute(self, data):
        self.session.locals['data'] = data
        #return eval(data['eval'], globals(), {'data': data, 'runner': self.owner()})
        self.session.runcode(self.main)
        return self.session.locals['result']

    def part_index(self, p: base.Page, params={}):
        p.ul([
            "data - Job Parameter",
            "result - Ergebnis des Jobs"
        ])
        # TODO edit main
        # TODO run code
        p.pre(json.dumps(self.session.locals['data']))


class CmdExecutor(BaseJobExecutor):
    """
      "cmd": "nwebclient.runner:CmdExecutor",
    """
    pids = []

    def __init__(self):
        super().__init__('cmd')

    def execute(self, data):
        if 'async' in data:
            pid = subprocess.Popen(data['cmd'], stderr=subprocess.STDOUT, shell=True)
            self.pids.append(pid)
            data['success'] = True
        else:
            try:
                data['output'] = subprocess.check_output(data['cmd'])
            except Exception as e:
                data['error_source'] = "CmdExecutor"
                data['error_message'] = str(e)
                #data['output'] = str(e.output)
        return data


class Transform(BaseJobExecutor):
    """
      Transformiert ein Data-Objekt,
      damit es mit anderen Runnern ausgeführt werden kann

      @see LazyDispatcher::part_dispacher_create

      rule
            {key: new_key, source: old_key}
            {set: {object} }
            {map: {object} }
    """

    start_new = True
    rules = []

    def __init__(self, type='transform', rules=[], start_new=True, override={}, map={}):
        super().__init__(type)
        self.define_event('on_transformed')
        self.start_new = start_new
        self.rules = rules
        if len(override) > 0:
            self.rules.append({'set': override})
        if len(map) > 0:
            self.rules.append({'map': map})

    def apply_rule(self, result, data, rule):
        if 'key' in rule:
            result[rule['key']] = data.get(rule.get('source', False))
        if 'set' in rule:
            d = rule['set']
            for k in d.keys():
                result[k] = d[k]
        if 'map' in rule:
            for k, v in rule['map']:
                result[v] = result[k]

    def execute(self, data):
        res = data
        if self.start_new:
            res = {}
        for rule in self.rules:
            self.apply_rule(res, data, rule)
        self.emit_event('on_transformed', **res)
        return res

    @staticmethod
    def create_form(p: base.Page):
        p.form_input('new_type', "New Type")
        p.form_input('emit_type', "Emit Type")
        p.form_input('set', "Set")
        p.form_input('map', "Map")

    def part_index(self, p: base.Page, params={}):
        p.h1("Transform")
        p.p(f"Dieser Job transformiert vom Type {self.type}")
        for rule in self.rules:
            p.pre(json.dumps(rule, indent=2))


class If(BaseJobExecutor):
    type = 'if'

    def execute_on_parent(self, data):
        o = self.owner()
        if isinstance(o, LazyDispatcher):
            return o.execute(data)
        else:
            return {'success': False, 'value': False}

    def solve_value(self, data):
        if isinstance(data, dict):
            res = self.execute_on_parent(data)
            if 'if_value_key' in data:
                return res.get(data['if_value_key'], False)
            return res
        else:
            return data

    def execute(self, data):
        a = self.solve_value(data.get('a', {}))
        b = self.solve_value(data.get('b', True))
        job = data.get('job', {})
        #self.info("A: " + str(a))
        #self.info("B: " + str(b))
        if a == b:
            self.info("If True")
            return self.execute_on_parent(job)
        else:
            #self.info("Else: " + str(data.get('else', {})))
            res = data.get('else', {})
            return res



class Static(BaseJobExecutor):

    def __init__(self, **kwargs):
        super().__init__('static')
        self.response = kwargs

    def execute(self, data):
        return self.response


class Echo(BaseJobExecutor):

    def __init__(self, type='echo'):
        self.type = type

    def execute(self, data):
        return self.data


class ProcessExecutor(BaseJobExecutor):

    type = 'process'

    restart = False
    exit_code = None

    cmd = 'uptime'
    cwd = None

    start_count = 0
    p = None

    line_listener = []
    end_listener = []

    def __init__(self, cmd=None, start=True, restart=False, cwd=None, on_line=None, on_end=None, on_up=None):
        super().__init__()
        if cmd is None:
            start = False
        self.var_names.append('restart')
        self.var_names.append('start_count')
        self.cmd = cmd
        self.cwd = cwd
        self.p_stdout = []
        self.start_count = 0
        self.restart = restart
        self.line_listener = []
        if on_line is not None:
            self.line_listener.append(on_line)
        self.end_listener = []
        if on_end is not None:
            self.end_listener.append(on_end)
        self.on_up = on_up
        if start:
            self.start()

    def start(self):
        self.thread = Thread(target=lambda: self.loop())
        self.thread.start()
        return {'success': True, 'message': 'Process Start'}

    def write(self, text):
        self.p.stdin.write(text)

    def loop(self):
        #print("Start ")
        self.start_count += 1
        #self.info("Starting " + self.cmd)
        self.p = subprocess.Popen(self.cmd, cwd=self.cwd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        self.errReader = Thread(target=lambda: self.loopErr()).start()
        if self.on_up is not None:
            self.on_up(self.p)
        while self.p.poll() is None:
            try:
                self.on_new_line(self.p.stdout.readline().decode('ascii'))
            except Exception as e:
                self.error("Unable to process Line: " + str(e))
        self.exit_code = self.p.returncode
        self.on_process_ended()

    def loopErr(self):
        while self.p.poll() is None:
            try:
                self.on_new_line(self.p.stderr.readline().decode('ascii'))
            except Exception as e:
                self.error("Unable to process Line: " + str(e))

    def on_process_ended(self):
        self.info("Process ended.")
        for action in self.end_listener:
            action(self)
        if self.restart:
            self.start()

    def on_new_line(self, line):
        self.p_stdout.append(line)
        for listener in self.line_listener:
            try:
                listener(line)
            except Exception as e:
                self.error("Unable to process Line: " + str(e))

    def pid(self):
        if self.p is None:
            return None
        else:
            return self.p.pid

    def kill(self):
        self.p.kill()
        return {'success': True}

    def terminate(self):
        self.p.terminate()
        self.p.wait()
        return self.success()

    def is_alive(self):
        if self.p is None:
            return False
        poll = self.p.poll()
        return poll is None

    def waitForEnd(self):
        time.sleep(0.1)
        while self.is_alive():
            time.sleep(0.1)
        return self

    def lines(self):
        res = map(lambda s: s.strip(), self.p_stdout)
        def filter_fn(s):
            return s != ''
        return list(filter(filter_fn, res))

    def execute(self, data):
        if 'run' in data:
            self.p_stdout = []
            self.start()
            self.waitForEnd()
            return self.success('exec', stdout=self.text())
        data['stdout'] = '\n'.join(self.p_stdout)
        data['pid'] = self.pid()
        data['start_count'] = self.start_count
        if 'start' in data:
            return self.start()
        elif 'kill' in data:
            return self.kill()
        elif 'terminate' in data:
            return self.terminate()
        return data

    def text(self):
        return '\n'.join(self.lines())

    def page(self, params={}):
        p = base.Page(owner=self)
        p.h2("Process " + self.cmd)
        p += web.button_js("Start", 'exec_job({type:"' + self.type + '",start:1});')
        p.pre(str('\n'.join(self.stdout)))
        return p.simple_page(params)

    
class WsExecutor(BaseJobExecutor):
    type = 'ws'
    
    def __init__(self):
        super().__init__()
    
    def execute(self, data):
        from nwebclient import ws
        w = ws.Website(data['url'])
        if 'py' in data:
            data['result'] = eval(data['py'], globals(), {'w': w})
            data['success'] = True
        if 'selector' in data:
            data['result'] = w.select_text(data['selector'])
            data['success'] = True
        return data

    def page(self, params={}):
        p = base.Page(owner=self)
        p.h1("Website")
        return p.nxui()


class ThreadedQueueExecutor(BaseJobExecutor):

    queue = []
    thread = None
    job_count = 0

    def __init__(self, start_thread=True):
        super().__init__()
        self.queue = []
        self.job_count = 0
        if start_thread:
            self.create_thread()
            self.thread.start()

    def create_thread(self):
        self.thread = Thread(target=lambda: self.thread_main())
        self.thread.setName(self.__threadName())

    def __threadName(self):
        return 'ThreadedQueueExecutor'
    def thread_start(self):
        self.info("Thread begin")
    def thread_main(self):
        self.info("Thread started")
        self.thread_start()
        while True:
            try:
                self.thread_tick()
                if getattr(threading.current_thread(), 'stop_request', False):
                        break
            except Exception as e:
                self.error(str(e))
                traceback.print_exc()

    def thread_tick(self):
        try:
            if not len(self.queue) == 0:
                print("In Thread Job Tick")
                first = self.queue[0]
                self.queue.remove(first)
                self.thread_execute(first)
                self.job_count += 1
                if len(self.queue) == 0:
                    self.thread_queue_empty()
        except Exception as e:
            self.error("Exception: " + str(e))
    def thread_execute(self, data):
        pass

    def thread_queue_empty(self):
        pass

    def is_busy(self):
        return len(self.queue) > 0

    def execute(self, data):
        if 'start_thread' in data:
            self.create_thread()
            self.thread.start()
            return {'success': True, 'message': 'Start Thread.'}
        elif 'queue' in data:
            self.queue.append(data)
        else:
            return super().execute(data)


class SerialExecutor(ThreadedQueueExecutor):
    """
      python -m nwebclient.runner --executor nwebclient.runner:SerialExecutor --rest --mqtt

      Connect:
        curl -X GET "http://192.168.178.79:8080/?port=/dev/ttyS0"
        curl -X GET "http://192.168.178.79:8080/?start_thread=true"
        curl -X GET "http://192.168.178.79:8080/?send=Hallo"
        curl -X GET "http://192.168.178.79:8080/?enable=rs485"
        curl -X POST https://reqbin.com/ -H "Content-Type: application/x-www-form-urlencoded"  -d "param1=value1&param2=value2"

    """
    MODULES = ['pyserial']
    CFGS = ['baudrate']
    type = 'serial'
    #port = '/dev/ttyUSB0'
    # S0
    port = '/dev/serial0'
    baudrate = 9600
    serial = None
    send = None
    buffer = ''
    buffer_size = 0
    rs485 = False
    send_pin = 17 #S3
    gpio = None
    disconnect_request = False
    message = ''
    wait_time = 0.05
    line_listener = []
    last_receive = 0
    count_error = 0
    count_receive = 0

    def __init__(self, start_thread=False, port=None, baudrate=None, args: util.Args = {}):
        super().__init__(start_thread=start_thread)
        self.line_listener = []
        self.wait_time = 0.1
        self.count_error = 0
        self.count_receive = 0
        self.param_names['send'] = "Sendet Daten über den Serial Port (Alias: print)"
        self.param_names['port'] = ""
        self.param_names['info'] = ""
        self.param_names['getbuffer'] = ""
        self.param_names['readbuffer'] = "Gibt den Inhalt zurueck und löscht den Buffer"
        self.param_names['enable'] = ""
        self.define_vars('port', 'baudrate', 'rs485', 'send_pin', 'buffer_size', 'wait_time', 'last_receive')
        self.define_event('on_line')
        if port is not None:
            self.port = port
        if 'baudrate' in args:
            baudrate = int(args['baudrate'])
        if baudrate is not None:
            self.baudrate = baudrate

    @property
    def port_name(self):
        return self.port.split('/')[-1]

    def change_baud(self, baud: int = 9600):
        self.baudrate = baud
        if self.thread is not None:
            setattr(self.thread, 'stop_request', True)
        time.sleep(1)
        self.create_thread()
        self.thread.start()
        return self.success(ui_realod=1)

    def send_wait(self):
        while self.serial.out_waiting > 0:
            self.infof("Serial out_waiting: {self.serial.out_waiting}")
        time.sleep(self.wait_time)  # besser serial flush

    def _sendData(self):
        if self.send is not None:
            if self.rs485:
                self.gpio.output(self.send_pin, True)
            if isinstance(self.send, bytes):
                bindata = self.send
            else:
                bindata = (self.send + "\n").encode()
            self.serial.write(bindata)
            self.serial.flush()
            self.send = None
            # Das Übertragen von serial.write findet Async statt, daher darf der Schreib-Pin nicht zu schnell
            # auf lesen gesetzt werden
            self.send_wait()
            if self.rs485:
                self.gpio.output(self.send_pin, False)

    def buffer_clearing(self):
        if len(self.buffer) > 100000:
            self.buffer = ''

    def thread_tick(self):
        self.buffer_clearing()
        if self.disconnect_request:
            if self.serial is not None:
                self.serial.close()
                self.serial = None
        else:
            self._sendData()
            line = self.serial.readline()
            if line != -1:
                try:
                    line_str = line.decode('utf8') # UnicodeDecodeError: 'ascii' codec can't decode byte 0xff in position 0: ordinal not in range(128)
                    if line_str != '':
                        self.last_receive = time.time()
                        self.count_receive += 1
                        self.emit_line(line_str)
                except UnicodeDecodeError as e:
                    self.count_error += 1
                    self.repair_line(line)
                    #    if not self.invert_line(line):
                    #        line_str = line.hex()
                    #        self.emit_line('HEX: ' + line_str)

    def repair_line(self, bindata: bytes):
        try:
            if len(bindata) > 0:
                if bindata[0] == 0xff:
                    bindata = bindata[1:]
                    self.emit_line(bindata.decode('utf8'))
            # TODO invert_line
        except:
            self.emit_line(bindata.decode('utf8', errors='ignore'))
        return False

    def emit_line(self, line_str: str):
        self.info(line_str)
        self.buffer += line_str + "\n"
        self.buffer_size = len(self.buffer)
        self.on_line(line_str)

    def invert_line(self, line):
        try:
            bin_str = bytes(list(map(lambda b: ~b + 0xff, list(bytearray(line)))))
            # bytes(list(map(lambda b: ~b + 0xff, list(bytearray(bytes.fromhex(h))))))
            line_str = bin_str.decode('utf8', errors='ignore')
            self.emit_line(line_str)
            return True
        except:
            return False

    def on_line(self, line):
        for listener in self.line_listener:
            listener(line)
        self.emit_event('on_line', value=line)

    def thread_start(self):
        import serial
        #from serial.tools import list_ports
        # https://github.com/ShyBoy233/PyGcodeSender/blob/main/pyGcodeSender.py
        self.info("Connect to " + self.port)
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=3)
            self.on_conected()
        except Exception as e:
            self.message = str(e)
            self.error("Connection failed. " + str(e))

    def on_conected(self):
        self.message += "Connected."
        self.info("Connected.")

    def enableRs485(self, data):
        import RPi.GPIO as GPIO
        # sudo apt-get install python-rpi.gpio
        if 'pin' in data:
            self.send_pin = int(data['pin'])
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.send_pin, GPIO.OUT)
        GPIO.output(self.send_pin, False)
        self.gpio = GPIO
        self.rs485 = True
        return {'success': self.rs485, 'pin': self.send_pin, 'mode': 'BCM'}

    def read_buffer(self):
        buf = self.buffer
        self.buffer = ''
        return {'buffer': buf}

    def state_info(self):
        return {
            'baud': self.baudrate,
            'port': self.port,
            'rs485': self.rs485,
            'send_pin': self.send_pin,
            'connected': self.is_connected(),
            'message': self.message,
            'serial': str(self.serial)
        }

    def on_line_nxesp(self, line):
        data = {'type': 'nxesp', 'cmd': line}
        self.onParentClass(LazyDispatcher, lambda p: p.execute(data))

    def enable_nxesp(self):
        self.line_listener.append(self.on_line_nxesp)
        return {'success': True, 'nxesp': 'enabled'}

    def write(self, message):
        self.execute({'print': message})

    def execute(self, data):
        if 'send' in data:
            self.send = data['send']
            return {'success': True, 'result': 'queued'}
        elif 'send_bin' in data:
            self.send = bytes.fromhex(data['data'])
            return {'success': True, 'result': 'queued'}
        if 'print' in data:
            self.send = data['print']
            self._sendData()
            return {'success': True, 'result': 'sended'}
        elif 'port' in data:
            self.port = data['port']
            return {'success': True}
        elif 'baud' in data:
            self.baudrate = int(data['baud'])
            return {'success': True}
        elif 'info' in data:
            return self.state_info()
        elif 'getbuffer' in data:
            return {'buffer': self.buffer}
        elif 'readbuffer' in data:
            return self.read_buffer()
        elif 'enable' in data and data['enable'] == 'rs485':
            return self.enableRs485(data)
        elif 'nxesp' in data:
            return self.enable_nxesp()
        elif 'clear' in data:
            self.buffer = ''
            return self.success()
        elif 'close' in data:
            self.disconnect_request = True
            return self.success('disconnect_request')
        elif 'fake_line' in data:
            self.on_line(data['fake_line'])
            return self.success('fake_line')
        elif 'change_baud' in data:
            return self.change_baud(int(data['change_baud']))
        else:
            return super().execute(data)

    def list_ports(self):
        import serial.tools.list_ports as t
        ports = t.comports()
        res = []
        for p in ports:
            res.append(p.name) # p.dev
        return res

    def js(self):
        return web.js_fn('on_get_buffer', ['data'], [
            'document.querySelector("#buffer").innerHTML = data["buffer"];'
        ]) + web.js_fn('on_info', ['data'], [
            'document.querySelector("#rs485_pin").innerHTML = data["send_pin"];',
            'document.querySelector("#connected").innerHTML = data["connected"];',
            'document.querySelector("#baudrate").innerHTML = data["baud"];',
            'document.querySelector("#message").innerHTML = data["message"];'
        ]) + super().js()

    def part_index(self, p: base.Page, params={}):
        p.h1("Serial Executor")
        self.write_to(p)
        p.prop("RS485-Pin", self.send_pin, html_id='rs485_pin')
        p.prop("RS485", str(self.rs485), html_id='rs485_enabled')
        p.prop("Buffer", self.buffer_size, html_id='buffer_size')
        p.prop("Ports", self.list_ports())
        p.prop("Message", self.message, html_id='message')
        p.prop("count_error", self.count_error)
        p.prop("count_receive", self.count_receive)
        #p.js_ready(f'observe_value("{self.type}", "buffer_size", "#buffer_size");')
        p += self.exec_btn("Connect", {'type': "serial", 'start_thread': True})
        p += self.exec_btn("Enable RS485", {'type': "serial", 'enable': "rs485"})
        p += self.exec_btn("Send", {'type': "serial", 'send': "Hallo"})
        p += web.button_js("Info", 'exec_job({type:"serial",info:1}, on_info);')
        p += web.button_js("Get Buffer", 'exec_job({type:"serial",getbuffer:1}, on_get_buffer);')
        p += web.input('baudrate', value='9600', id='in_baudrate')
        p += web.button_js("Set Baud", 'exec_job_p({type:"serial",baud:"#in_baudrate"});')
        p += web.input('port', value='/dev/serial0', id='in_port')
        p += web.button_js("Set Port", 'exec_job_p({type:"serial",port:"#in_port"});')
        p += self.exec_btn("ttyS0", type="serial", port="/dev/ttyS0")
        p += self.exec_btn("ttyUSB0", type="serial", port="/dev/ttyUSB0")
        p += self.exec_btn("Pipe To NxEsp", type="serial", nxesp=1)
        p += self.exec_btn("Clear Buffer", type="serial", clear=1)

        p.div('', id='result')
        p.hr()
        p += web.input('data', value='Hallo Welt', id='data')
        p += web.button_js("Send", 'exec_job_p({type:"serial",print:"#data"});')
        p.hr()
        p.div(web.a("Runner", '/pysys/runner'))
        p.hr()
        p.pre("", id='buffer')
        p.hr()
        btn2400 = self.action_btn(dict(title="2400", type=self.type, change_baud=2400))
        p.prop("Baudrate", "2400, 9600, 14400, 19200, 115200, 250000 " + btn2400)
        p.prop("Devices", "/dev/serial0")
        p.div(web.a("Send UI", self.link(self.part_send)))
        p.pre("", id='error')

    def is_connected(self):
        return self.serial is not None

    def write_to(self, p: base.Page, summary=False):
        c = "False" if not self.is_connected() else f"True (Buffer:{len(self.buffer)})"
        p.prop("Connected", c, html_id='connected')
        p.prop("Port",  self.port, html_id='port')
        p.prop("Baudrate", self.baudrate, 'baudrate')
        if summary is True:
            p.right(web.a("Open", f'/pysys/{self.type}_ctrl'))

    def part_send(self, p: base.Page, params={}):
        p.hr()
        p.h3("Send Binary")
        p.form_input("data", "Hex Data", id='data')
        p(self.action_btn_parametric("Send Bin", dict(type=self.type, send_bin=1, data='#data')))
        p.pre('', id='result')


class GCodeExecutor(ThreadedQueueExecutor):
    """
      python -m nwebclient.runner --executor nwebclient.runner:GCodeExecutor --rest

      git -C ~/nwebclient/ pull && pip3 install ~/nwebclient/ && python3 -m nwebclient.runner --executor nwebclient.runner:GCodeExecutor --rest

      
      UI: http://127.0.0.1:8080/runner
    """
    MODULES = ['pyserial']
    type = 'gcode'
    port = '/dev/ttyUSB0'
    # 250000
    baudrate = 250000
    serial = None
    timeout_count = 0
    log = None
    mqtt_topic = 'main'
    posAbs = None
    """ Status der Stepper: True On False Off """
    steppers = None
    last_command = 0
    pos = None

    def __init__(self, start_thread=False, args: util.Args = {}):
        super().__init__(start_thread=start_thread)
        self.timeout_count = 0
        self.args = util.Args() if args is None else args
        self.steppers = None
        self.baudrate = args.get(self.type + '_baud', self.baudrate)
        self.port = args.get(self.type + '_port', self.port)
        self.pos = machine.Instruction('G0')
        self.initMqtt()
        self.param_names['gcode'] = "Execute GCode"
        self.param_names['connect'] = "Verbinden"
        self.define_vars('port', 'baudrate', 'speed', 'lenkung', 'interval', 'robo_f')
        self.define_sig(self.moveX)
        self.define_sig(self.moveY)
        self.define_sig(self.moveZ)
        self.define_sig(self.mx)
        self.define_sig(self.my)
        self.define_sig(self.mz)

    def initMqtt(self):
        mqtt_host = self.args.get('MQTT_HOST')
        if mqtt_host is not None: 
            self.log = ticker.MqttPub(host=mqtt_host)
            self.log(self.mqtt_topic, '__init__')

    def __len__(self):
        return len(self.queue)

    def prn(self, msg):
        print(msg)
        if self.log is not None:
            self.log(self.mqtt_topic, msg)

    def thread_start(self):
        import serial
        #from serial.tools import list_ports
        # https://github.com/ShyBoy233/PyGcodeSender/blob/main/pyGcodeSender.py
        self.info("Connect to " + self.port)
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=3)
            self.info("Connected.")
            self.emit_event('on_connect')
        except Exception as e:
            self.error("Connection faild. " + str(e))

    def thread_tick(self):
        super().thread_tick()
        if self.serial is not None:
            if not self.serial.is_open:
                self.emit_event('on_disconnect')
                self.serial = None

    def thread_execute(self, data):
        if 'gcode' in data:
            self.execGCode(data['gcode'])

    def thread_queue_empty(self):
        self.info("Queue is empty.")

    def processOnOff(self, gcode, on_start, off_start, state):
        if gcode.startswith(on_start):
            return True
        elif gcode.startswith(off_start):
            return False
        else:
            return state

    def processGCode(self, gcode):
        try:
            self.last_command = time.time()
            self.steppers = self.processOnOff(gcode, 'M17', 'M18', self.posAbs)
            self.posAbs = self.processOnOff(gcode, 'M82', 'M83', self.posAbs)
            if gcode.startswith('G0') or gcode.startswith('G1'):
                if self.posAbs is False:
                    pass # add pos
                if self.posAbs is True:
                    self.pos.update_pos(gcode)
            elif gcode.startswith('G92'):
                self.pos = machine.Instruction('G0 X0 Y0 Z0')
            elif gcode.startswith('M4'):
                self.onM4_SpindleOn()
            elif gcode.startswith('M5'):
                self.onM5_SpindleOff()
        except Exception as e:
            self.error("Error in processGCode")
            self.error(e)

    def onM4_SpindleOn(self):
        pass

    def onM5_SpindleOff(self):
        pass

    def execGCode(self, gcode):
        if gcode.strip().startswith(';') or gcode.isspace() or len(gcode) <= 0:
            return
        self.info("Exec G-Code: " + gcode)
        self.processGCode(gcode)
        self.serial.write((gcode+'\n').encode())
        while 1:  # Wait untile the former gcode has been completed.
            try:
                line = self.serial.readline()
                self.info("Response: " + line.decode('ascii', 'ignore'))
                if line.startswith(b'ok'):
                    break
                self.timeout_count += 1
                # print("readline timeout")
            except Exception as e:
                self.error("Error in execGCode")
                self.error(e)
                break

    def is_connected(self):
        return self.serial is not None and self.serial.is_open

    def queueGCode(self, gcode):
        self.queue.append({'gcode': gcode})

    def mx(self, val=10):
        self.moveX(val)
        self.queueGCode('G92 X0 Y0 Z0')
        self.queueGCode('M84 ')
        return self.success('mx')

    def my(self, val=10):
        self.moveY(val)
        self.queueGCode('G92 X0 Y0 Z0')
        self.queueGCode('M84 ')
        return self.success('my')

    def mz(self, val=10):
        self.moveZ(val)
        self.queueGCode('G92 X0 Y0 Z0')
        self.queueGCode('M84 ')
        return self.success('mz')

    def moveX(self, val=10):
        self.queueGCode('G0 X'+str(val))

    def moveY(self, val=10):
        self.queueGCode('G0 Y'+str(val))

    def moveZ(self, val=10):
        self.queueGCode('G0 Z'+str(val))

    def heatBed(self, temp):
        self.queueGCode('M190 S'+str(temp)) # M140 for without wait

    def heatE0(self, temp):
        self.queueGCode('M109 T0 S'+str(temp)) # M104
        # G92 X0 Y0 Z0 ; Set Home

    def __repr__(self):
        return "GCode(queue({0}),thread, port:{1} count:{2})".format(len(self), self.port, self.job_count)

    def moveControls(self):
        return """
          <table>
            <tr>
              <td></td>
              <td>""" + self.btn_gcodes('Y+', ['G1 Y10', 'G92 X0 Y0 Z0']) + """</td>
              <td></td>
              <td>""" + self.btn_gcodes('Z+', ['G1 Z10', 'G92 X0 Y0 Z0']) + """</td>
              <td>""" + self.btn_gcodes('Z+1', ['G1 Z1', 'G92 X0 Y0 Z0']) + """</td>
            </tr>
            <tr>
              <td>""" + self.btn_gcodes('X-', ['G1 X-10', 'G92 X0 Y0 Z0']) + """</td>
              <td></td>
              <td>""" + self.btn_gcodes('X+', ['G1 X10', 'G92 X0 Y0 Z0']) + """</td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <td></td>
              <td>""" + self.btn_gcodes('Y-', ['G1 Y-10', 'G92 X0 Y0 Z0']) + """</td>
              <td></td>
              <td>""" + self.btn_gcodes('Z-', ['G1 Z-10', 'G92 X0 Y0 Z0']) + """</td>
              <td>""" + self.btn_gcodes('Z-1', ['G1 Z-1', 'G92 X0 Y0 Z0']) + """</td>
            </tr>
          <table>
          <div>
            """ + self.btn_gcodes('Heat E0 205', ['M109 T0 S205']) + """
            """ + self.btn_gcodes('Heat Bed 60', ['M190 S60']) + """
            """ + self.btn_gcodes('Extrude', ['G1 E5']) + """
            """ + self.exec_btn("Connect", type=self.type, connect=1) + """
          </div>
          <div>
            Einstellungen:
            <div>
              """ + self.btn_gcodes('M4 Laser/Spindle On', ['M4']) + """
              """ + self.btn_gcodes('10%', ['M4 O25']) + """
              """ + self.btn_gcodes('25%', ['M4 O70']) + """
              """ + self.btn_gcodes('50%', ['M4 O128']) + """
              """ + self.btn_gcodes('M5 Laser/Spindle Off', ['M5']) + """<br />
            </div>
            """ + self.btn_gcodes('M17 Steppers On', ['M17']) + """<br />
            """ + self.btn_gcodes('M18 Steppers Off', ['M18']) + """<br />
            """ + self.btn_gcodes('M82 E Absolute Pos', ['M82']) + """
            """ + self.btn_gcodes('M83 E Relativ Pos', ['M83']) + """<br />
            """ + self.btn_gcodes('M92 Steps per Unit', ['M92 X20 Y20 Z800']) + """<br />
            """ + self.btn_gcodes('G90 Absolute Pos', ['G90']) + """
            """ + self.btn_gcodes('G91 Relativ Pos', ['G91']) + """<br />
            """ + self.btn_gcodes('G92 Set Home here', ['G92 X0 Y0 Z0']) + """<br />
            """ + self.btn_gcodes('M121 Disable Endstops', ['M121']) + """<br />
            """ + self.btn_gcodes('M204 Setze Beschleunigung', ['M204 T10']) + """<br />
            M42 P44 S10
            TODO GCode Input
            <input name="gcode" id="gcode" type="text" />
            """ + web.button_js("Exec GCode", 'exec_job_p({"type": "gcode", "gcode": "#gcode"})') + """
            <hr />
            GCode: """ + str(self.args.get('GCODE_PATH', '')) + """
            
            
          </div>
          <button id="btnFocus">Tastatur</button>
          
          <div id="result"></div>
        """

    def gcodes(self):
        path = self.args.get('GCODE_PATH', None)
        if path is None:
            path = '.'
        files = [f for f in os.listdir(path) if os.path.isfile(path+'/'+f) and f.endswith(".gcode")]
        html = ''
        for f in files:
            d = web.a("Details", f'?type={self.type}&{self.type}=gcode&file={f}')
            html += '<li><a href="?type=gcode&file='+str(f)+'">'+str(f)+'</a> - '+d+'</li>'
        return '<div><span title="'+path+'">GCodes:</span><br /><ul>'+html+'</ul></div>'

    def queueFile(self, file):
        path = self.args.get('GCODE_PATH', None)
        if path is None:
            path = '.'
        f = path + '/' + file
        with open(f, 'r') as fh:
            for line in fh.readlines():
                self.queueGCode(line)

    def handleActions(self, params):
        try: # sollte raus
            if 'gcode' in params:
                self.queue.append(params)
            if 'a' in params and params['a'] == 'connect':
                self.execute({'connect': 1})
            if 'file' in params:
                self.queueFile(params['file'])
        except Exception as e:
            return "Error: " + str(e)
        return ""

    def js(self):
        return super().js() + """
         $(function() {
               function gcode(code) {
                 console.log(code);
                 $.get('?gcode='+encodeURI(code));
               };
               $('#btnFocus').click(function() {
                $(document).bind('keydown', function (evt) {
                    console.log(evt.keyCode);
                    switch (evt.keyCode) {
                        case 40: // Pfeiltaste nach unten
                        case 98: // Numpad-2
                            gcode('G0 Y-1');
                            return false; break;
                        case 38: // nach oben
                        case 104: // Numpad-8
                            gcode('G0 Y1');
                            return false; break;
                        case 37: // Pfeiltaste nach links
                        case 100: // Numpad-4
                            gcode('G0 X-1');
                            return false; break;
                        case 39: 
                        case 102: // NumPad-6
                            gcode('G0 X1');
                            return false; break;
                        // w=87
                        // S=83
                        // NumPad+ = 107
                        // NumPad- = 109
                    }		
                });
               });
            });
        """

    def page_index(self, params={}):
        p = base.Page(owner=self)
        p += '<script src="https://bsnx.net/4.0/templates/sb-admin-4/vendor/jquery/jquery.min.js"></script>'
        p += '<script>' + self.js() + '</script>'
        p += self.handleActions(params) + self.__repr__() + self.moveControls() + self.gcodes()
        p.prop("Baudrate", self.baudrate)
        return p.nxui()

    def connect(self, data={}):
        self.create_thread()
        self.thread.start()
        if 'port' in data:
            self.port = data['port']
        return self.success('connected.')

    def param_maxqueue(self, data):
        return (not 'maxqueue' in data) or (int(data['maxqueue']) < len(self.queue))

    def executeGCode(self, data):
        if 'clear' in data:
            self.queue = []
        self.queueGCode(data['gcode'])
        return self.success('gcode queued.')

    def executeGCodes(self, data):
        if 'clear' in data:
            self.queue = []
        if isinstance(data['gcodes'], str):
            for gcode in data['gcodes'].split(','):
                self.queueGCode(gcode)
        else:
            for gcode in data['gcodes']:
                self.queueGCode(str(gcode))
        return self.success('gcode queued.')

    def execute(self, data):
        if 'gcode' in data and self.param_maxqueue(data):
            return self.executeGCode(data)
        elif 'gcodes' in data and self.param_maxqueue(data):
            return self.executeGCodes(data)
        elif 'connect' in data:
            return self.connect(data)
        elif 'split_low' in data:
            self.split_low(data)
        elif 'split_high' in data:
            self.split_high(data)
        else:
            return super().execute(data)

    def split_low(self, data):
        file = data['file']
        import nwebclient.machine as m
        g = m.GCode(file)
        gcodes = g.split_low(int(data.get('layer', 4)))
        gcodes.append('G0 X10 Y10')
        self.executeGCodes({'gcodes': gcodes})

    def split_high(self, data):
        file = data['file']
        import nwebclient.machine as m
        g = m.GCode(file)
        self.executeGCodes({'gcodes': g.split_high(int(data.get('layer', 4)))})

    def setupRestApp(self, app):
        from flask import request
        super().setupRestApp(app)
        app.add_url_rule('/pysys/gcode', 'gcode', view_func=lambda: self.page(request.args))
        app.add_url_rule('/pysys/robot', 'robot', view_func=lambda: self.page_robot())
        app.add_url_rule('/pysys/gsetup', 'gsetup', view_func=lambda: self.page_setup())

    def btn_gcode(self, title, gcode):
        return web.button_js(title, 'exec_job({"type":"gcode", "gcode": "'+gcode+'"});')

    def btn_gcodes(self, title, gcodes):
        gcodes = map(lambda gcode: '"'+gcode+'"', gcodes)
        return web.button_js(title, 'exec_job({"type":"gcode", "gcodes": ['+','.join(gcodes)+']});')

    speed = 12
    lenkung = 6
    interval = 1100
    robo_f = 900

    def page_robot(self):
        if not self.is_connected():
            self.connect()
        p = base.Page(owner=self)
        p += '<script src="https://bsnx.net/4.0/templates/sb-admin-4/vendor/jquery/jquery.min.js"></script>'
        if self.posAbs is False:
            p.right("Relative Positioning activ")
        if self.is_connected():
            p.right("Verbunden", title="Baud: " + str(self.baudrate))
        g_vor = f'G0 X{self.speed} Y{self.speed} F{self.robo_f}'
        g_left = f'G0 X{(self.speed+self.lenkung)} Y0 F{self.robo_f}'
        g_left_b = f'G0 X{self.speed} Y{-self.speed} F{self.robo_f}'
        g_right = f'G0 X0 Y{(self.speed+self.lenkung)} F' + str(self.robo_f)
        g_right_b = f'G0 X{-self.speed} Y{self.speed} F{self.robo_f}'
        g_back = 'G0 X' + str(-self.speed) + ' Y' + str(-self.speed) + ' F' + str(self.robo_f)
        h = 'G92 X0 Y0'
        left = self.btn_gcodes("Links", [g_left, h])
        left_b = self.btn_gcodes("Links", [g_left_b, h])
        vor = self.btn_gcodes("Vor", [g_vor, h])
        right = self.btn_gcodes("Rechts", [g_right, h])
        right_b = self.btn_gcodes("Rechts", [g_right_b, h])
        back = self.btn_gcodes("Zurück", [g_back, h])
        p += web.table([
            [left,   vor,  right],
            [left_b, back, right_b]
        ])
        # Joystick von Dir NW N NE, In der Mitte is C
        p.div('', id='result')
        p.div('', id='joystick', style="width:200px;height:200px;margin:50px;position:fixed;bottom:30px;left:30px;")
        p.script('/static/js/joystick/joystick.js')
        p.script(web.js_ready('var joy = new JoyStick("joystick"); \n' +
            'setInterval(function(){ '+
                'if (joy.GetDir()=="N") { exec_job({"type":"gcode", "maxqueue": 2, "gcodes": ["'+g_vor+'", "G92 X0 Y0"]}); }'+
                'if (joy.GetDir()=="NW") { exec_job({"type":"gcode", "maxqueue": 2, "gcodes": ["'+g_left+'", "G92 X0 Y0"]}); }' +
                'if (joy.GetDir()=="NE") { exec_job({"type":"gcode", "maxqueue": 2, "gcodes": ["'+g_right+'", "G92 X0 Y0"]}); }' +
                'if (joy.GetDir()=="S") { exec_job({"type":"gcode", "maxqueue": 2, "gcodes": ["' + g_back + '", "G92 X0 Y0"]}); }' +
            '}, '+str(self.interval)+');'))
        for v in self.var_names:
            p.div(v+": " + str(getattr(self, v, '')))
        p.hr()
        p += web.input('robo_f', value=self.robo_f, id='robo_f')
        p += web.button_js("Set F", 'exec_job_p({type:"'+self.type+'",setvar:"robo_f", value:"#robo_f"});')
        p += web.input('speed', value=self.speed, id='speed')
        p += web.button_js("Set speed", 'exec_job_p({type:"' + self.type + '",setvar:"speed", value:"#speed"});')
        p += web.input('interval', value=self.interval, id='interval')
        p += web.button_js("Set interval", 'exec_job_p({type:"' + self.type + '",setvar:"interval", value:"#interval"});')
        p += web.button_js("Steppers On", 'exec_job({type:"' + self.type + '",gcode:"M17"});')
        p += web.button_js("Steppers Off", 'exec_job({type:"' + self.type + '",gcode:"M18"});')
        p += web.button_js("X-", 'exec_job({type:"' + self.type + '",gcodes:["M17", "G92 X0", "'+f'G0 X-{self.speed} F{self.robo_f}'+'", "M18"]});')
        p += web.button_js("X+", 'exec_job({type:"' + self.type + '",gcodes:["M17", "G92 X0", "'+f'G0 X{self.speed} F{self.robo_f}'+'", "M18"]});')

        return p.simple_page()

    def page_setup(self):
        p = base.Page(owner=self)
        # TODO ls /dev | grep ttyUSB
        return p.simple_page()

    def write_to(self, p: base.Page, summary=False):
        p.div(web.a("Roboter", '/pysys/robot'))

    def page_gcodes(self, params={}):
        p = base.Page(owner=self)
        p += self.gcodes()
        return p.nxui()

    def page_gcode(self, params={}):
        p = base.Page(owner=self)
        dir = self.args.get('GCODE_PATH', './')
        f = params.get('file', None)
        path = dir + f
        p.h1(f"GCode: {f}")
        import nwebclient.machine as m
        try:
            g = m.GCode(path)
            p.div(f"Size: X: {g.min('X')} - {g.max('X')}, Y: {g.min('Y')} - {g.max('Y')}")
            p(g.to_svg())
            p.prop("Lines", len(g))
            p.prop("Layer-Count", g.get_layer_count())
            p.hr()
            p.h3("Split")
            p.input('layer', id='layer', value=4)
            p(self.action_btn_parametric("Print Split Low", {'type': self.type, 'split_low': 1, 'file': path, 'layer': '#layer'}))
            p(self.action_btn_parametric("Print Split High", {'type': self.type, 'split_high': 1, 'file': path, 'layer': '#layer'}))
            if g.error is not None:
                p(g.error)
        except Exception as e:
            self.error(str(e))
            p.div("Class GCode: " + str(e))
            p.pre(str(traceback.format_exc()))

        try:
            reader = m.GcodeReader(path)
            p.div(web.img(reader.to_image_dataurl()))
        except Exception as e:
            self.error(str(e))
            p.div("Class GcodeReader:" + str(e) + urllib.parse.quote( str(type(e)) ))
        p.pre('', id='result')
        return p.nxui()

    def list_svgs(self):
        path = self.args.get('GCODE_PATH', None)
        if path is None:
            path = '.'
        files = [f for f in os.listdir(path) if os.path.isfile(path + '/' + f) and f.endswith(".svg")]
        return files

    def page_svgs(self, params={}):
        """
        curl https://sh.rustup.rs -sSf | sh
        git clone https://github.com/sameer/svg2gcode.git
        """
        p = base.Page(owner=self)
        for svg in self.list_svgs():
            p.div(web.a(svg, f'?type={self.type}&{self.type}=svg&f={svg}'))
        return p.nxui(params)

    def slice_svg(self, path):
        import nwebclient.machine as m
        reader = m.GcodeReader(path)
        try:
            from svg_to_gcode.svg_parser import parse_file
            from svg_to_gcode.compiler import Compiler, interfaces
            # Instantiate a compiler, specifying the interface type and the speed at which the tool should move. pass_depth controls
            # how far down the tool moves after every pass. Set it to 0 if your machine does not support Z axis movement.
            gcode_compiler = Compiler(interfaces.Gcode, movement_speed=1000, cutting_speed=300, pass_depth=5)
            curves = parse_file(path)  # Parse an svg file into geometric curves
            gcode_compiler.append_curves(curves)
            gcode_compiler.compile_to_file(path + '.gcode', passes=2)
        except ImportError:
            print("Error: Please install pip install svg-to-gcode")
            print("")
            print("  pip install svg-to-gcode")
            print("")
        #cmd = f'cargo run --release -- {path} --off "M4" --on "M5" -o out.gcode'
        #ProcessExecutor(cmd, cwd='/home/pi/repos/svg2gcode')

    def page_svg(self, params={}):
        p = base.Page(owner=self)
        f = params.get('f', None)
        path = self.args.get('GCODE_PATH', './') + f
        p.h1(f"SVG: {f}")
        p(util.file_get_contents(path).decode('utf-8'))
        p.div(web.a("Slice", f'?type={self.type}&{self.type}=svg&f={f}&svg_op=slice'))
        if params.get('svg_op', '') == 'slice':
            self.slice_svg(path)
        if os.path.isfile(path + '.gcode'):
            p.div("GCode exists")
        return p.nxui(params)

    def nxitems(self):
        return [
            {'title': "SVG", 'url': '/pysys/dispatcher?type='+self.type+'&gcode=svgs'},
            {'title': "GCodes", 'url': '/pysys/dispatcher?type=' + self.type + '&gcode=gcodes'}
        ]


class MqttLastMessages(BaseJobExecutor):

    type = 'lastmessages'
    client_id = 'MqttLastMessages'
    port = 1883

    def __init__(self, host='127.0.0.1', topic='main', maxsize=50):
        super().__init__()
        from queue import Queue
        self.queue = Queue(maxsize=maxsize)
        self.topic = topic
        self.host = host
        try:
            self.connect()
        except Exception as e:
            self.error(e)

    def connect(self):
        from paho.mqtt import client as mqtt_client
        print("[MqttSub] Connect to " + self.host + " Topic: " + self.topic)
        import paho.mqtt
        if paho.mqtt.__version__[0] > '1':
            client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, self.client_id, transport='tcp')
        else:
            client = mqtt_client.Client(self.client_id, transport='tcp')

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.info("Connected to MQTT Broker!")
                client.subscribe(self.topic)
            else:
                print("Failed to connect, return code %d\n", rc)

        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.queue.put(msg.payload.decode())

        client.on_connect = on_connect
        client.on_message = on_message
        client.connect_async(self.host, self.port, keepalive=6000)
        client.loop_start()

    def items(self):
        result_list = []
        while not self.queue.empty():
            result_list.append(str(self.queue.get()))
        for item in result_list:
            self.queue.put(item)
        return result_list

    def ips(self):
        res = set()
        for line in self.items():
            if line.startswith('nxudp'):
                a = line.split(' ')
                res.add(a[2]) # name:a[1]
        return list(res)

    def value(self, name):
        res = set()
        for line in self.items():
            n = name+':'
            if line.startswith(n):
                a = line[len(n):]
                res.add(a.strip())
        return res

    def execute(self, data):
        res = {}
        if 'guid' in data:
            res['guid'] = data['guid']
        if 'ips' in data:
            res['ips'] = self.ips()
        if 'var' in data:
            res['value'] = self.value(data['var'])
        else:
            res['items'] = list(self.items())
        return res

    def page(self, params={}):
        p = base.Page(owner=self)
        p.h1("MqttLastMessages")
        opts = {'title': 'MqttLastMessages'}
        for item in self.items():
            p.div(item)
        return p.nxui(opts)


class MqttSubscription(base.DictProxy):
    def __init__(self, topic):
        super().__init__({'topic': topic, 'last': None, 'changed': None})
    def handle_message(self, data):
        self['last'] = data
        self['changed'] = time.time()


class MqttSend(BaseJobExecutor):

    type = 'mqttsend'
    client_id = 'MqttSend'
    client = None
    subscriptions = {}
    port = 1883
    topic = 'main'
    host = '127.0.0.1'
    streams = []

    def __init__(self, host=None, topic=None, type=None, args: util.Args = {}):
        super().__init__()
        self.define_sig(dev.Param('message'), dev.Param('topic'))
        self.param_names['topic'] = 'MQTT-Topic an das gesendet wird, optional'
        self.param_names['message'] = ''
        self.subscriptions = {}
        self.streams = []
        if type is not None:
            self.type = type
        if args is not None:
            self.host = args.get('MQTT_HOST', self.host)
            self.port = args.get('MQTT_PORT', self.port)
        if topic is not None:
            self.topic = topic
        if host is not None:
            self.host = host
        self.connect()

    def __repr__(self):
        return f'MQTT({self.host}:{self.port}, subs: {len(self.subscriptions.keys())}, publish(topic, message))'

    def connect(self):
        try:
            from paho.mqtt import client as mqtt_client
            print("[MqttSend] Connect to " + self.host + " Topic: " + self.topic)
            self.client = Mqtt.create_client()

            def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    self.info("Connected to MQTT Broker for sending.")
                    #client.subscribe(self.topic)
                    pass
                else:
                    self.info("Failed to connect, return code "+str(rc))

            def on_message(client, userdata, msg):
                #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
                if msg.topic in self.subscriptions.keys():
                    self.handle_message(msg.payload.decode(), msg.topic)

            self.client.on_connect = on_connect
            self.client.on_message = on_message
            self.client.connect_async(self.host, self.port, keepalive=6000)
            self.client.loop_start()
        except Exception as e:
            self.error(str(e))
            self.client = None

    def handle_message(self, data, topic):
        self.info("handle_message" + str(data))
        if topic in self.subscriptions:
            self.subscriptions[topic].handle_message(data)
        self.emit_event('on_' + topic, message=data, line=data, topic=topic)

    def execute(self, data):
        topic = self.topic
        if 'subscribe' in data:
            return self.subscribe(data)
        elif 'stream_value' in data:
            return self.stream_value(data.get('topic', 'value'), data['job'], data.get('key', 'value'), data.get('time', 3600))
        if 'topic' in data:
            topic = data['topic']
        if 'message' in data and self.client is not None:
            self.publish(topic, data['message'])
            return {'success': True, 'message': 'From MQTT-Send'}
        else:
            return super().execute(data)

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def subscribe(self, data):
        topic = data['subscribe']
        self.client.subscribe(topic=topic)
        self.subscriptions[topic] = MqttSubscription(topic)
        self.define_event('on_' + topic)
        return self.success('ok')

    def stream_value(self, topic, job, key='value', time_s=3600):
        def stream_op():
            try:
                v = self.onParentClass(LazyDispatcher, lambda d: d.execute(job), {})
                if key is not None:
                    v = v.get(key)
                else:
                    v = json.dumps(v)
                self.info(f"Stream {v} in {topic}")
                self.publish(topic, v)
            except Exception as e:
                self.error(f"Stream Error: " + str(e))
        thread = self.periodic(time_s, stream_op)
        self.streams.append(dict(topic=topic, job=job, time=time_s, last=None, thread=thread))
        return self.success('ok, topic: ' + str(topic))

    def part_index(self, p: base.Page, params={}):
        p.prop("Connected", self.client is not None)
        p.prop("Topic", self.topic)
        p.hr()
        p.input('Topic', id='topic', title="MQTT Topic", value=self.topic)
        p.input('Message', id='message', title="MQTT Topic")
        p(self.action_btn_parametric("Subscribe", dict(type=self.type, topic='#topic', message='#message')))
        p.hr()
        p.div('Subscript to topic:')
        p.input('subscribe', id='subscribe')
        p(self.action_btn_parametric("Subscribe", {'type': self.type, 'subscribe': '#subscribe'}))
        p.right(web.a("Subscribtions", self.link(self.part_subscribtions)))
        p.hr()
        self.part_streamjob(p, params)

        # TODO create send job
        p.hr()
        p.pre('', id='result')

    def part_subscribtions(self, p: base.Page, params={}):
        web.pre(str(self.subscriptions))

    def part_streamjob(self, p: base.Page, params={}):
        p.div('Stream Job:')
        p("Topic: ")
        p.input('Topic', id='topic_s', title="MQTT Topic")
        p.input('Jpb', id='job', value='?type=')
        p.input('Key', id='key', value='value')
        p.input('time', id='time', value=3600)
        p(self.action_btn_parametric("Stream", dict(type=self.type, stream_value=1, topic='#topic_s', job='#job',
                                                    key='#key', time='#time')))
        p.ul(map(lambda s: f'{s["topic"]}  Job: {s["job"]}', self.streams))


class ProxyRunner(BaseJobExecutor):
    """

    """ 
    def __init__(self, pre_cmd=None, runner=None, runner_install=False, url=None, runner_cmd=None, base_data= {}, type=None):
        super().__init__()
        self.base_data = base_data
        if type is not None:
            self.type = type
        if pre_cmd is not None:
            os.system(pre_cmd)
        if runner is not None:
            self._start_runner(runner, runner_install)
        elif url is not None:
            self.url = url
        elif runner_cmd is not None:
            self._start_runner_cmd(runner_cmd)
        else:
            self.error("No Runner defined")
            self.error("    runner = nwebclient.runner:SerialExecutor")
            self.error("    url = http://192.168.178.2")
            self.error("    runner_cmd = docker run -p {port}:7070 --rm -it nxml")
            self.error("")

    def _start_runner_cmd(self, cmd):
        p = util.find_free_port()
        c = cmd.replace('{port}', str(p))
        self.info("Process: " + c)
        self.process = ProcessExecutor(c, start=True)
        self.url = 'http://127.0.0.1:' + str(p) + '/'

    def _start_runner(self, runner, runner_install=True):
        if runner_install:
            pass # TODO call static install
        p = util.find_free_port()
        cmd = sys.executable + '-m' + 'nwebclient.runner' + '--rest' + '--port ' + str(p)+'--executor' + runner
        self.process = ProcessExecutor(cmd, start=True)
        self.url = 'http://127.0.0.1:' + str(p) + '/'

    def execute(self, data):
        try:
            s = requests.post(self.url, data={**data, **self.base_data}).text
            return json.loads(s)
        except Exception as e:
            return self.fail(str(e))


class NxEspCommandExecutor(SerialExecutor):
    """
       nwebclient.runner:NxEspCommandExecutor
    """

    type = 'nxesp'

    cmds = {}
    action_list = []

    def __init__(self, port=None, start=True, args: util.Args = None, cam_prefix='rpicam-'):
        if port is None:
            start = False
        SerialExecutor.__init__(self, start, port=port)
        print("NxEspCommandExecutor on " + str(port))
        self.param_names['cmd'] = "NxEsp Command (e.g. setd)"
        self.cam_prefix = cam_prefix
        self.cmds = dict()
        self.cmds['setd'] = lambda a: self.setd(a)
        self.cmds['init'] = lambda a: self.init(a)
        self.cmds['cam_vid'] = lambda a: self.cam_vid(a)
        self.cmds['cam_photo'] = lambda a: self.cam_photo(a)
        self.cmds['cam_usb_photo'] = lambda a: self.cam_usb_photo(a)
        self.cmds['shutdown'] = lambda a: self.shutdown(a)
        self.cmds['reboot'] = lambda a: self.reboot(a)
        self.cmds['ip'] = lambda a: self.ip(a)
        self.cmds['n'] = self.n
        self.cmds['get_actions'] = lambda a: self.get_actions(a)
        from nwebclient import nx
        self.cmds['udp_send'] = nx.udp_send
        self.param_names['cmd'] = "Bearbeitet einen NxESP-Befehl"
        self.param_names['enable_esp_cmd'] = "Start einen Proxy auf Pot 80"
        self.param_names['action_add'] = "Fügt eine Aktion zur Ausführbaren Aktion hinzu, in der UI wird dafür ein Button angezeigt"
        self.action_list = [
            #{"title": "Video", "type": "nxesp", "cmd": "cam_vid ;"},
            #{"title": "Foto", "type": "nxesp", "cmd": "cam_photo ;"},
            #{"title": "Aus", "type": "nxesp", "cmd": "setd 10 0 ;"},
            #{"title": "An", "type": "nxesp", "cmd": "setd 10 1 ;"},
            #{"title": "Shutdown", "type": "nxesp", "cmd": "shutdown ;"}
        ]
        self.define_sig(dev.Param('cmd', ''))
        self.define_sig(dev.Param('line', ''))
        if args is not None:
            cfg = args.env('nxesp', {})
            for action in cfg.get('exposed', []):
                self.action_list.append(action)

    def add_command(self, name, op):
        """
         :param op: function(a: array)
        """
        self.cmds[name] = op

    def actions(self):
        # nweb.json nxesp: {"exposed": [...]}
        return self.action_list

    def get_actions(self, args):
        return json.dumps(self.actions())

    def on_conected(self):
        super().on_conected()
        for a in self.actions():
            self.publish(a)
        self.onParentClass(LazyDispatcher, lambda p: self.read_gpio(p))

    def publish_command(self, title, cmd):
        a = {"title": title, "command": cmd}
        self.publish(a)

    def publish(self, obj):
        self.serial.write((json.dumps(obj) + '\n').encode())

    def read_gpio(self, p: LazyDispatcher):
        for r in p.instances:
            if isinstance(r, GpioExecutor):
                self.publish_command("An",  "setd "+str(r.pin)+" 1 ;")
                self.publish_command("Aus", "setd " + str(r.pin) + " 0 ;")

    def on_line(self, line):
        self.info("Received line: " + line)
        self.command(line)
        super().on_line(line)

    def commands(self):
        return self.cmds.keys()

    def command(self, line):
        """
            line e.g. "setd 17 1"
        """
        self.info("Executing: " + str(line))
        line = line.strip()
        for cmd in self.cmds:
            if line.startswith(cmd):
                self.info("Do: " + cmd)
                i = line.index(cmd)
                trimed_line = line[i:].strip()
                a = trimed_line.split(' ')
                return self.run_command(a)
        result = self.run_on_runner(line)
        if result is None:
            return 'Error: Unknown Command.'
        else:
            return result

    def run_on_runner(self, line):
        parts = line.split(' ')

        def on_parent(dispatcher):
            if dispatcher.canExecute({'type': parts[0]}):
                r = dispatcher.get_runner(parts[0])
                data = {
                    'parent': self,
                    'nxesp_command': line
                }
                # TODO create data object
                a = parts[1:]
                if len(r.param_names.keys()) > 2:
                    # r.param_names.keys()  TODO for bis len(r.param_names.keys())-2
                    pass
                return r.to_text(r.execute(data))
            else:
                return None
        return self.onParentClass(LazyDispatcher, on_parent)

    def run_command(self, parts):
        c = parts[0]
        args = parts[1:]
        self.info("run_command: " + c + " with " + ' '.join(args))
        if c in self.cmds:
            fn = self.cmds[c]
            return fn(args)
        else:
            self.info("Unknown Command: " + str(c))
            return "Unknown Command: " + str(c)

    def n(self, args):
        from nwebclient import nx
        if nx.get_name() == args[0]:
            args.pop(0)
            self.run_command(args)

    def init(self, args):
        from nxbot import GpioExecutor
        type = 'pin' + str(args[0])
        exec = GpioExecutor(pin=int(args[0]), dir=args[1])
        self.onParentClass(LazyDispatcher, lambda d: d.loadRunner(type, exec))

    def setd(self, args):
        t = 'pin' + str(args[0])
        self.onParentClass(LazyDispatcher, lambda d: d.execute({'type': t, 'args': args}))
        return ''

    def cam_vid(self, args):
        #cmd = 'raspivid -o /home/pi/video.h264 -t 30000'
        cmd = self.cam_prefix + 'vid -o /home/pi/video.h264 -t 30000'
        ProcessExecutor(cmd)
        return 'raspivid'

    def cam_photo(self, args):
        # https://www.raspberrypi.com/documentation/computers/camera_software.html#getting-started
        #cmd = 'raspistill -o /home/pi/current.jpg'
        cmd = self.cam_prefix + 'still -t 1000 -o /home/pi/current.jpg'
        ProcessExecutor(cmd, on_line=lambda s: self.info(s))
        return 'raspistill'

    def cam_usb_photo(self, args):
        # https://raspberrypi-guide.github.io/electronics/using-usb-webcams
        cmd = 'fswebcam -r 1280x720 --no-banner /home/pi/current.jpg'
        ProcessExecutor(cmd, on_line=lambda s: self.info(s))
        return 'usb_photo'

    def shutdown(self, args):
        cmd = 'sudo shutdown -t now'
        ProcessExecutor(cmd)
        return 'shutdown'

    def reboot(self, args):
        cmd = 'sudo reboot'
        ProcessExecutor(cmd)
        return 'reboot'

    def ip(self, args):
        from nwebclient import nx
        return nx.get_ip()

    def setupRestApp(self, app):
        super().setupRestApp(app)
        app.add_url_rule('/pysys/' + self.type, self.type, view_func=lambda: self.page_nxesp())
        # web.all_params()

    def page_nxesp(self):
        return "NxESP"

    def write_to(self, p: base.Page, summary=False):
        p.div("NxEsp Command Executor")
        p.div("Commands: " + ','.join(self.cmds.keys()))
        p.input('cmd')
        p.input('exec', type='button', value="Ausführen")
        p.h4("Actions:")
        for action in self.actions():
            p.div(self.action_btn(action))

    def part_index(self, p:base.Page, params={}):
        p.h1("NxEsp Commando")
        opts = {'title': 'NxESP'}
        self.write_to(p)

    def execute(self, data):
        if 'cmd' in data:
            return {'result': self.command(data['cmd'])}
        if 'line' in data:
            return {'result': self.command(data['line'])}
        elif 'enable_esp_cmd' in data:
            self.p80 = ProcessExecutor(sys.executable + ' -m nwebclient.runner --executor nwebclient.runner:NxEspCmdProxy --rest --port 80')
        elif 'action_add' in data:
            self.action_list.append(data['action_add'])
            return {'success': True, 'action_count': len(self.action_list)}
        return super().execute(data)


class NxEspCmdProxy(BaseJobExecutor):
    """
        python3 -m nwebclient.runner --executor nwebclient.runner:NxEspCmdProxy --rest --port 80
    """
    def setupRestApp(self, app):
        super().setupRestApp(app)
        app.add_url_rule('/cmd', 'nxesp', view_func=lambda: self.page_cmd())
    def page_cmd(self):
        from flask import request
        cmd = request.args.get('cmd')
        result = requests.get('http://127.0.0.1:7070', params={'type': 'nxesp', 'cmd': cmd}).json()
        return result.get('result', 'Error: CMD. NxEspCmdProxy')


class FileSend(BaseJobExecutor):
    type = 'file'
    def __init__(self, file):
        super().__init__()
        self.file = file

    def is_image(self):
        return self.file.endswith('.png') or self.file.endswith('.jpg')

    def to_data_uri(self):
        try:
            with open(self.file, 'rb') as f:
                binary_fc = f.read()  # fc aka file_content
                base64_utf8_str = base64.b64encode(binary_fc).decode('utf-8')
                ext = self.file.split('.')[-1]
                return f'data:image/{ext};base64,{base64_utf8_str}'
        except:
            return "about:to_data_uri-error"

    def write_to(self, p: base.Page, summary=False):
        if self.is_image():
            p('<img src="'+self.to_data_uri()+'" style="width:100%;" />')

    def page(self, params={}):
        p = base.Page(owner=self)
        p.h1("Send File")
        self.write_to(p)
        return p.nxui()

    def execute(self, data):
        return {'src': self.to_data_uri()}


class BluetoothSerial(ProcessExecutor):

    def __init__(self, discoverable=True):
        self.mqtt = ticker.MqttPub()
        self.info("Bluetooth Serial, requires npy system bluetooth-serial-enable")
        super().__init__(cmd='sudo rfcomm watch hci0', start=True, restart=True)
        if discoverable:
            ProcessExecutor(cmd='sudo bluetoothctl discoverable on')
        Thread(target=lambda: self.rfcommWatcher()).start()

    def exists(self, path):
        """Test whether a path exists.  Returns False for broken symbolic links"""
        try:
            os.stat(path)
        except OSError:
            return False
        return True

    def rfcommWatcher(self):
        while True:
            self.info("rfcomm watch")
            if self.exists('/dev/rfcomm0'):
                self.info("rfcomm exists")
                if not self.is_port_processed('/dev/rfcomm0'):
                    self.on_connection('/dev/rfcomm0')
            time.sleep(10)

    def is_port_processed(self, port):
        for c in self.childs():
            if isinstance(c, SerialExecutor):
                if c.port == port:
                    return True
        return False

    def prn(self, msg):
        super().prn(msg)
        self.mqtt.publish(msg)

    def on_new_line(self, line):
        # Waiting for connection on channel 1
        # Connection from A0:D7:22:6B:24:6D to /dev/rfcomm0
        # Press CTRL-C for hangup
        # Disconnected
        # Waiting for connection on channel 1
        self.info(line)
        if line.strip().startswith('Connection'):
            a = line.split('to')
            dev = a[1].strip()
            self.info("Connection: " + dev)
            self.on_connection(dev)

    def on_connection(self, dev):
        self.info("creating NxEspCommandExecutor")
        self.addChild(NxEspCommandExecutor(dev))
        
    def execute(self, data):
        return super().execute(data)
        # TODO info about /dev/rfcommN


class MessageSaver(BaseJobExecutor):

    type = 'message_saver'

    def __init__(self, host='127.0.0.1', port=1883, topic='ar', connect=True):
        super().__init__()
        self.param_names['emit'] = "Sendet"
        self.param_names['save'] = "Speichert"
        self.param_names['load'] = "Lädt"
        self.param_names['clear'] = "Löscht alle Nachrichten"
        self.param_names['set'] = "Setzt Einstellungen"
        self.host = host
        self.topic = topic
        self.port = port
        self.recording = True
        self.messages = []
        self.extra_delay = None
        self.start = None
        self.client = None
        if connect is True:
            self.connect()

    def connect(self):
        self.client = Mqtt({'MQTT_HOST': self.host}, topic=self.topic, on_message=lambda m: self.on_message(m))
        return {'success': True, 'result': "connected"}

    def get_time(self):
        if self.start is None:
            self.start = time.time()
        return time.time() - self.start

    def on_message(self, message):
        if self.recording is True:
            self.messages.append({
                'time': self.get_time(),
                'message': message
            })

    def emit(self):
        self.recording = False
        for m in self.messages:
            if self.client is not None:
                self.client.publish(self.topic, m['message'])
            if self.extra_delay is not None:
                time.sleep(self.extra_delay)
        return {'success': True, 'result': "Messages Send"}

    def set(self, data):
        if 'extra_delay' in data:
            self.extra_delay = float(data['extra_delay'])
            self.info("Extra Delay: " + str(self.extra_delay))
        return {'success': True, 'result': 'set'}

    def execute(self, data):
        if 'clear' in data:
            self.messages = {}
            return {'success': True, 'result': "No Messages"}
        elif 'save' in data:
            with open(data['save'], 'w') as f:
                json.dump(self.messages, f)
            return {'success': True, 'result': "File written"}
        elif 'emit' in data:
            return self.emit()
        elif 'emit_async' in data:
            util.run_async(lambda: self.emit())
            return {'success': True, 'result': 'thread started'}
        elif 'load' in data:
            self.messages = util.load_json_file(data['load'])
            return {'success': True, 'result': "Messages: " + str(len(self.messages))}
        elif 'start' in data:
            self.recording = True
            return {'success': True, 'result': "start"}
        elif 'stop' in data:
            self.recording = False
            return {'success': True, 'result': "stopped"}
        elif 'set' in data:
            return self.set(data)
        elif 'connect' in data:
            return self.connect()
        return super().execute(data)

    def setupRestApp(self, app):
        super().setupRestApp(app)
        app.add_url_rule('/pysys/message_saver', 'message_saver', view_func=lambda: self.page_ops())

    def btn_exec(self, title, op):
        return web.button_js(title, 'exec_job({"type":"'+self.type+'", "'+op+'":1});')

    def btn_exec_job(self, title, data):
        return web.button_js(title, 'exec_job('+json.dumps(data)+');')

    def page_ops(self):
        p = base.Page(owner=self)
        p.div("Message-Count: " + str(len(self.messages)))
        p += self.btn_exec("Emit", 'emit')
        p += self.btn_exec("Emit (Async)", 'emit_async')
        p += self.btn_exec("Clear", 'clear')
        p += self.btn_exec("Start", 'start')
        p += self.btn_exec("Stop", 'stop')
        p += self.btn_exec_job("Set Delay", {'type': self.type, 'set': 1, 'extra_delay': 0.4})
        p += self.btn_exec_job("Save", {'type': self.type, 'save': '/home/pi/ar.json'})
        p += self.btn_exec_job("Load", {'type': self.type, 'load': '/home/pi/ar.json'})
        return p.nxui()


class NxMessageProcessor(BaseJobExecutor):

    ips = {}

    def __init__(self, host='127.0.0.1', port=1883, topic='main', connect=True, args: util.Args = {}):
        super().__init__('message_processor')
        self.ips = {}
        self.host = host
        self.topic = topic
        self.port = port
        self.client = None
        if connect is True:
            self.connect()

    def connect(self):
        from paho.mqtt import client as mqtt_client
        print("[MqttSub] Connect to " + self.host + " Topic: " + self.topic)

        self.client = Mqtt.create_client('NxMessageProcessor')

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.info("Connected to MQTT Broker!")
                client.subscribe(self.topic)
            else:
                print("Failed to connect, return code %d\n", rc)

        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.on_message(client, msg.payload.decode())

        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect_async(self.host, self.port, keepalive=6000)
        self.client.loop_start()
        return {'success': True, 'result': "connected"}

    def on_message(self, client, message):
        # nxudp Rpi4 192.168.178.44 info from rpi upi cron
        if message.startswith('nxudp'):
            self.on_nxudp(message.split(' '))

    def on_nxudp(self, array):
        self.ips[array[2]] = {'title': array[1]}

    def write_to(self, p: base.Page, summary=False):
        for ip in self.ips.keys():
            p.div(ip)

    def part_index(self, p: base.Page, params={}):
        with p.section("NxMessageProcessor"):
            p.p("Nimmt eine Nachricht per MQTT entgegen und sendet sie an die NxESP Pipeline")
            self.write_to(p)
            # TODO display more

    def execute(self, data):
        # len(data) == 1
        return self.ips


class Tokenizer(BaseJobExecutor):
    """

     See: https://docs.python.org/3/library/tokenize.html#tokenize.generate_tokens
    """

    type = 'tokenizer'

    def execute(self, data):
        if 'input' in data:
            return self.tokenize(data)
        elif 'parse' in data:
            return self.ast(data['parse']);
        super().execute(data)

    def tokenize(self, data):
        from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
        names = {0: 'ENDMARKER', 1: 'NAME', 2: 'NUMBER', 3: 'STRING', 4: 'NEWLINE', 5: 'INDENT', 6: 'DEDENT',
                 7: 'LPAR', 8: 'RPAR', 9: 'LSQB'}
        # RSQB = 10, COLON = 11, COMMA = 12, SEMI = 13, PLUS = 14, MINUS = 15, STAR = 16, SLASH = 17,
        # VBAR = 18, AMPER = 19, LESS = 20, GREATER = 21, EQUAL = 22, DOT = 23, PERCENT = 24, LBRACE = 25, RBRACE = 26
        # EQEQUAL = 27, NOTEQUAL = 28, LESSEQUAL = 29, GREATEREQUAL = 30, TILDE = 31, CIRCUMFLEX = 32
        # LEFTSHIFT = 33, RIGHTSHIFT = 34, DOUBLESTAR = 35, PLUSEQUAL = 36, MINEQUAL = 37, STAREQUAL = 38
        # SLASHEQUAL = 39, PERCENTEQUAL = 40, AMPEREQUAL = 41, VBAREQUAL = 42, CIRCUMFLEXEQUAL = 43
        # LEFTSHIFTEQUAL = 44, RIGHTSHIFTEQUAL = 45, DOUBLESTAREQUAL = 46, DOUBLESLASH = 47, DOUBLESLASHEQUAL = 48
        # AT = 49, ATEQUAL = 50, RARROW = 51, ELLIPSIS = 52, COLONEQUAL = 53, EXCLAMATION = 54, OP = 55, AWAIT = 56
        # ASYNC = 57, TYPE_IGNORE = 58, TYPE_COMMENT = 59, SOFT_KEYWORD = 60, FSTRING_START = 61, FSTRING_MIDDLE = 62
        # FSTRING_END = 63, COMMENT = 64 NL = 65, ERRORTOKEN = 66, ENCODING = 67, N_TOKENS = 68, NT_OFFSET = 256
        s = data['input']
        tokens = []
        g = tokenize(BytesIO(s.encode('utf-8')).readline)
        for toknum, tokval, _, _, _ in g:
            tokens.append({'token': tokval, 'toknum': toknum})
        data['tokens'] = tokens
        data['success'] = True
        return data

    def ast(self, source):
        import ast
        return self.success('ok', value=ast.dump(ast.parse(source), indent=4))

    def part_index(self, p: base.Page, params={}):
        p(web.textarea('', name='text', id='text'))
        p(self.action_btn_parametric("Tokenize", {'type': self.type, 'input': '#text'}))
        p(self.action_btn_parametric("Parse", {'type': self.type, 'parse': '#text'}))
        p.pre('', id='result')


class NamedJobs(BaseJobExecutor):
    """

        Job-Def:
            job_name: {
              **job_data,
              tags: [],
              canvas_name: {
                display: button|value|html,  Bei html wird job_data[html] angezeigt
                x: int,
                y: int,
                refresh: 1000    in ms
              }
            }
    """

    type = 'named'

    name_key = 'named_jobs'

    def __init__(self, args: util.Args = {}, name_key='named_jobs', jobs={}):
        super().__init__()
        self.args = args
        self.name_key = name_key
        if name_key is None:
            self.jobs = jobs
        else:
            self.jobs = self.args.get(self.name_key, {})
        nw = getattr(self.getRoot(), 'nweb', None)
        if nw is not None:
            self.init_nweb(nw)
        self._process_jobs()

    def _process_jobs(self):
        for k in self.jobs.keys():
            self.define_sig(dev.PStr('name', k))
            if 'cron' in self.jobs[k]:
                self.periodic(int(self.jobs[k]['cron']), lambda: self.execute_by_name(k))

    def __str__(self):
        return f'Named({len(self.jobs)})'

    def init_nweb(self, nweb):
        try:
            for d in nweb.docs('tag=Named-Job'):
                self.jobs[d.name] = json.loads(d.content())
        except Exception as e:
            self.error("init_nweb " + str(e))

    def tags(self):
        res = set()
        for job in self.jobs.values():
            for t in job.get('tags', []):
                res.add(t)
        return res

    def by_tag(self, tag):
        res = list()
        for job in self.jobs.values():
            if tag in job.get('tags', []):
                res.append(job)
        return res

    def page_tags(self, params={}):
        p = base.Page(owner=self)
        p.h1("Named Jobs: Tags")
        p.ul(map(lambda t: web.a(t, f'?type={self.type}&{self.type}=tag&tag={t}'), self.tags()))
        return p.nxui()

    def page_tag(self, params={}):
        p = base.Page(owner=self)
        p.h1("Named Jobs")
        for job in self.by_tag(params['tag']):
            self.show_job(p, job)
        return p.nxui()

    def show_job(self, p, job):
        with p.dv(_class='part_box'):
            p.h3(job)
            p.pre(json.dumps(self.jobs[job]))
            p(self.exec_btn("Execute " + job, type=self.type, name=job))

    def page_index(self, params={}):
        p = base.Page(owner=self)
        p.h1("Named Jobs")
        p.div("In nweb.json unter "+self.name_key+": {name: {jobdef}, ...} anlegen.")
        self.info("Named Jobs: " + str(self.jobs))
        for job in self.jobs.keys():
            self.show_job(p, job)
        p.pre('', id='result')
        p.hr()
        p.div(web.a("Canvas", f'?type={self.type}&{self.type}=canvas'))
        p.div(web.a("Tags", f'?type={self.type}&{self.type}=tags'))
        self.list_canvases(p)
        return p.nxui()

    def list_canvases(self, p):
        for name in self.jobs.keys():
            if isinstance(self.jobs[name], dict) and 'display' in self.jobs[name] and isinstance(self.jobs[name]['display'], dict):
                p.div(web.a(name, f'?type={self.type}&{self.type}=canvas&canvas={name}'))

    def get_canvas_jobs(self, key='canvas'):
        res = []
        for k in self.jobs.keys():
            if self.jobs[k].get(key, None) is not None:
                self.jobs[k]['named_job_name'] = k
                res.append(self.jobs[k])
        return res

    def to_part(self, job, display):
        guid = util.guid()
        attrs = {'style': '', 'id': 'p' + guid, 'class': ''}
        if 'class' in display:
            attrs += ' ' + display['class']
        kind = display.get('display', 'button')
        if kind == 'button':
            html = self.action_btn(job)
        elif kind == 'value':
            r = self.owner().execute(job)
            r = r if r is not None else {}
            k = display.get('display_value_key', 'value')
            html = display.get('pre', '') + str(r.get(k, '-'))
            if 'refresh' in display:
                r = 'document.getElementById("p'+guid+'").innerHTML = r["'+k+'"]; '
                n = job['named_job_name']
                html += web.script(web.js_interval(display['refresh'], 'exec_job({"type": "named", "name": "'+n+'"}, function(r) {'+r+'})'))
        elif kind == 'html':
            html = job.get('html', '')
        if 'x' in display:
            attrs['style'] += f'position: absolute; left: {display["x"]}px;'
        if 'y' in display:
            attrs['style'] += f'top: {display["y"]}px;'
        if 'background-color' in display:
            attrs['style'] += f'background-color: {display["background-color"]};'
        if 'style' in display:
            attrs['style'] += display['style']
        return web.div(html, **attrs)

    def page_canvas(self, params={}):
        p = base.Page(owner=self)
        k = params.get('canvas', 'canvas')
        jobs = self.get_canvas_jobs(k)
        with p.dv(_class='page_canvas'):
            for itm in jobs:
                p(self.to_part(itm, itm[k]))
        p.pre('', id='result')
        return p.simple_page(params)

    def execute_by_name(self, name):
        o = self.owner()
        if isinstance(o, LazyDispatcher):
            return o.execute(self.jobs[name])
        else:
            return {'success': False, 'message': "No Job with name"}

    def add(self, name, data):
        self.jobs[name] = data
        return self.success('added')

    def execute(self, data):
        if 'add' in data:
            return self.add(data.get('name', 'new_job'), data['data'])
        elif 'name' in data:
            return self.execute_by_name(data['name'])
        return super().execute(data)


class FileList(BaseJobExecutor):

    def __init__(self, path, type='filelist'):
        super().__init__(type)
        self.path = path

    def page_index(self, params={}):
        p = base.Page(owner=self)
        p.h1("File")
        for f in glob.glob(self.path + '**'):
            p.div(str(f))
            # kompletter Pfad
        return p.nxui()


class FailoverRunner(BaseJobExecutor):
    """
      Wählt auf mehreren Runnern einen aus der den Job erfolgreich ausführt

      nxwebclient.runner:FailoverRunner('fo1', [])
    """

    def __init__(self, type='failover', runners=[]):
        super().__init__()
        self.type = type
        self.fail_count = 0
        self.runners = map(self.map_runner, runners)

    def map_runner(self, runner):
        if isinstance(runner, str):
            pass
        return runner

    def execute_on_runner(self, runner, data):
        if isinstance(runner, str):
            parent = self.getParentClass(LazyDispatcher)
            data['type'] = runner
            return parent.execute(data)
        return runner.execute(data)

    def execute(self, data):
        for r in self.runners:
            res = self.execute_on_runner(r, data)
            success = res.get('success', False)
            if success:
                return res
            else:
                self.fail_count += 1
        return self.fail('No Runner left.')

    def part_index(self, p: base.Page, params={}):
        p.ul(self.runners)
        p.prop("Fail Count", self.fail_count)


class ApiExecutor(BaseJobExecutor):
    """
     Prüft vor dem ausführen eines Runners ob ein gültiger API-Key übergeben wurde
    """

    def __init__(self, runner=None, keys=None, args: util.Args = {}):
        super().__init__()
        if runner is None:
            self.runner = AutoDispatcher()
        else:
            self.runner = runner
        if keys is None and args.get('api_keys') is not None:
            self.keys = args.get('api_keys')
        else:
            self.keys = []

    def log_request(self, key):
        pass

    def is_valid_key(self, key, data={}):
        return key in self.keys

    def execute(self, data={}):
        if 'api_key' in data:
            if self.is_valid_key(data['api_key'], data):
                self.log_request(data['api_key'])
                return self.runner.execute(data)
            else:
                return self.fail('Invalid API-Key')
        else:
            return self.fail('API-Key (api_key) Required. No Key found.')


class SystemSetup(BaseJobExecutor):
    """

        add_ssh_host: { "Host": "parent"}

    """
    type = 'systemsetup'
    def execute(self, data):
        try:
            if 'add_ssh_host' in data:
                return self.add_ssh_host(data['add_ssh_host'])
            if 'write_file' in data:
                return self.write_file(data['write_file'])
        except Exception as e:
            return self.error(str(e))

    def ensure_ssh_dir(self):
        p = expanduser('~/.ssh')
        if not os.path.isdir(p):
            os.mkdir(p)

    def create_host_config(self, data):
        res = "\n"
        for key in data.keys():
            if key != 'Host':
                res += '  '
            res += key + " " + data[key] + "\n"
        return res

    def update_host_key(self, hostname):
        cmd = f'ssh-keyscan -H {hostname} >> ~/.ssh/known_hosts'
        ProcessExecutor(cmd)

    def add_ssh_host(self, data):
        self.ensure_ssh_dir()
        p = expanduser('~/.ssh/config')
        if not os.path.isfile(p):
            util.file_put_contents(p, self.create_host_config(data))
            self.update_host_key(data['Hostname'])
        else:
            c = util.file_get_contents(p)
            if data['Host'] not in c:
                util.file_append_contents(self.create_host_config(data))
        return self.success('added')

    def write_file(self, data):
        file = expanduser(data['filename'])
        content = data['content']
        util.file_put_contents(file, content)
        return self.success('written')


class MultiJob:
    """
        nwebclient.ticker:NWebJobFetch

        job_state_group_id

        TODO upload möglich

    """

    stages = []
    state_group_id = 'B05AA14479FBED44BD688748791A4BE5'
    result_group_id = None # TODO
    executor = None
    result = None

    def __init__(self):
        self.stages = []
        self.nweb = NWebClient(None)
        self.init_stages()
        self.cpu = ticker.Cpu()
        self.cpu.add(ticker.NWebJobFetch(delete_jobs=False))
        self.cpu.add(ticker.JobExecutor(executor=JobRunner(self)))
        self.cpu.add(ticker.Ticker(interval=180, fn= lambda: self.downloadResults()))
        self.result = ticker.NWebJobResultUploader(nwebclient=self.nweb)
        self.cpu.loopAsync()

    def downloadResults(self):
        for d in self.nweb.group(self.result_group_id).docs():
            if self.working_on(d.guid()):
                self.intern_execute(json.loads(d.content))

    def set_stages(self):
        self.stage(self.stage2, ['response'])
        self.stage(self.stage1, [])  # Muss an ende

    def stage(self, method, keys):
        self.stages.append({'method': method, 'keys': keys})
        return self

    def canExecuteStage(self, keys, data):
        for key in data:
            if key not in data:
                return False
        return True

    def stage1(self, data):
        # call self.executor.execute()
        return data

    def stage2(self, data):
        # call self.executor.execute()
        return data

    def publishGuid(self, guid):
        d = self.nweb.getOrCreateDoc(self.state_group_id, 'multi_runner_guids')
        c = d.content()
        if c == '':
            d.setContent(json.dumps([guid]))
        else:
            array = json.loads(c)
            if not guid in array:
                array.append(guid)
                d.setContent(json.dumps(array))

    def working_on(self, guid):
        d = self.nweb.getOrCreateDoc(self.state_group_id, 'multi_runner_guids')
        c = d.content()
        if c != '':
            array = json.loads(c)
            return guid in array
        else:
            return False

    def intern_execute(self, data):
        for stage in self.stages:
            if self.canExecuteStage(stage['keys']):
                m = stage['method']
                self.info("Executing Stage " + str(m))
                m(data)
                break

    def execute(self, data):
        self.publishGuid(data['guid'])
        self.intern_execute(data)
        self.nweb.deleteDoc(data['guid'])


restart_process = None

def restart(args):
    global restart_process
    newargs = args.argv[1:]
    newargs.remove('--install')
    newargs = [sys.executable, '-m', 'nwebclient.runner', '--sub'] + newargs
    print("Restart: " + ' '.join(newargs))
    #subprocess.run(newargs, stdout=subprocess.PIPE)
    with subprocess.Popen(newargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
        restart_process = p
        for line in p.stdout:
            print(line, end='') # process line here
    exit()


def list_runners():
    import inspect
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    print("Executors: ")
    for c in clsmembers:
        if issubclass(c[1], BaseJobExecutor):
            print("  " + str(c[0]))


def usage(exit_program=False):
    print("Usage: "+sys.executable+" -m nwebclient.runner --install --ticker 1 --executor module:Class --in in.json --out out.json")
    print("")
    print("Options:")
    print("  --install           Installiert die Abhaegigkeiten der Executoren")
    print("  --rest              Startet den Buildin Webserver")
    print("  --mqtt              Verbindet MQTT")
    print("  --ticker 1          Startet einen nwebclient.ticker paralell")
    print("  --executor          Klasse zum Ausführen der Jobs ( nwebclient.runner.AutoDispatcher )")
    print("                          - nwebclient.runner.AutoDispatcher")
    print("                          - nwebclient.runner.MainExecutor")
    print("  --disable-ui")
    print("")
    list_runners()
    if exit_program:
        exit()


def configure_ticker(args, runner: JobRunner):
    if args.hasFlag('ticker'):
        cpu = ticker.create_cpu(args).add(ticker.JobExecutor(executor=runner))
        if args.hasFlag('nweb-jobs'):
            cpu.add(ticker.NWebJobFetch(supported_types=runner.jobexecutor.supported_types(), delete_jobs=True, limit=1))
            #ticker.NWebJobResultUploader()
            # TODO fetch und push  "job_fetch_group_id"
        cpu.loopAsync()


def configure_nweb(args, runner: JobRunner):
    try:
        import nweb
        import sqlite3
        if 'NPY_DB' in args:
            db = sqlite3.connect(args['NPY_DB'], check_same_thread=False)
            runner.nweb = nweb.NWeb(args, db)
            runner.nweb.create_settings_table()
    except Exception as e:
        pass

def main_install(executor, args):
    print("Install")
    util.load_class(executor, create=False).pip_install()
    pks = os.environ.get('PIP_PKGS', None)
    if pks is not None:
        pargs = [sys.executable, '-m', 'pip', pks]
        print("PIP: " + ' '.join(pargs))
        with subprocess.Popen(pargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=1,
                              universal_newlines=True) as p:
            for line in p.stdout:
                print(line, end='')  # process line here
    if not args.hasFlag('--exit'):
        restart(args)


def arg_cloud(args):
    from nwebclient import nx
    if 'cloud' in args and ('cloud_ssid' not in args or args['cloud_ssid'] == nx.get_ssid()):
        nc = NWebClient(None)
        d = nc.group('F30C94D566C931AF09D946F2F6665611').doc_by_name(nx.get_name())
        if d is not None:
            print("NWEB:CloudConfig: Update /etc/nweb.json")
            d.save('/etc/nweb.json')
            args = util.Args(read_nxd=('-no-nxd' not in args))
    return args


def setup_system(setup_args=[]):
    r = SystemSetup()
    for step in setup_args:
        r.execute(step)


def run(args: util.Args, executor=None):
    global jobrunner
    global current
    args = arg_cloud(args)
    if args.help_requested():
        usage(exit_program=True)
    if args.env('setup', None) is not None:
        setup_system(args['setup'])
    if args.hasFlag('list'):
        list_runners()
        exit()
    if 'nxd' in args:
        args.merge_yml(args['nxd'])
    if executor is None:
        executor = args.getValue('executor')
    if executor is None:
        print("No executor found. Using AutoDispatcher")
        executor = AutoDispatcher()
    print("Executor: " + str(executor))
    if args.hasFlag('cfg') and isinstance(executor, LazyDispatcher):
        executor.loadDict(args.env(args.getValue('name', 'runners'), {}))
    if args.hasFlag('install'):
        main_install(executor, args)
    else:
        jobrunner = util.load_class(executor, create=True, run_args=args)
        current = JobRunner(jobrunner, args)
        configure_nweb(args, current)
        configure_ticker(args, current)
        if args.hasFlag('rest'):
            if args.hasFlag('mqtt'):
                current.execute_mqtt(args)
            current.execute_rest(port=args.getValue('port', 7070), run=args.getValue('nxrun', True))
        elif args.hasFlag('mqtt'):
            current.execute_mqtt(args, True)
        elif args.hasFlag('queue'):
            current.execute_queue()
        else:
            current.execute_file(args.getValue('in', 'input.json'), args.getValue('out', 'output.json'))


def main(executor=None):
    try:
        args = util.Args()
        print("nwebclient.runner Use --help for more Options")
        run(args, executor)
    except KeyboardInterrupt:
        print("")
        print("Exit nwebclient.runner")
        if not restart_process is None:
            print("Close Sub")
            restart_process.terminate()

        
if __name__ == '__main__':
    main()
            
#import signal
#def sigterm_handler(_signo, _stack_frame):
#    # Raises SystemExit(0):
#    sys.exit(0)
#
#    signal.signal(signal.SIGTERM, sigterm_handler)
