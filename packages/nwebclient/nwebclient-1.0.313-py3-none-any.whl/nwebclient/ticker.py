"""
  Doku: https://gitlab.com/bsalgert/nwebclient/-/wikis/ticker

  @deprecated
"""

import time
import os
import os.path
import sys
import threading 
import requests
import json
import base64
import random
import traceback
from collections import deque

from nwebclient import web as w
from nwebclient import base as b
from nwebclient import NWebClient
from nwebclient import util
from nwebclient.base import action

class Process(b.Base, b.Named):
    name = 'process'
    cpu = None
    def __init__(self, name='Process'):
        super().__init__()
        self.name = name
    def tick(self):
        pass
    def configure(self, arg):
        pass
    def cmd(self, args):
        if len(args)>1 and args[0]==self.name and args[1]=='info':
            self.printInfo()
        return False
    def printInfo(self, p = print):
        p("[Process] name: " + str(self.name))
        attrs = dir(self)
        for a in attrs:
            if not a.startswith('__') and not a in ['cpu']:
                v = getattr(self, a, '-')
                if not type(v).__name__ == 'method':
                    p("[Process] {0}: {1} ({2})".format(a, str(v), str(type(v).__name__)))
    def __str__(self):
        return "Process({0}, {1})".format(self.name, self.__class__.__name__)
    def __repr__(self):
        return "Process({0}, {1})".format(self.name, self.__class__.__name__)
    def htmlContent(self, params={}):
        return '<div>Parents: '+str(self.getParents())+'</div>'
    def toHtml(self, params={}):
        p = b.Page()
        p.h1("Prozess: "+ self.name + '('+self.className()+')')
        p('<pre>')
        self.printInfo(p=p)
        p('</pre>')
        p(self.htmlContent(params))
        p.pre(self.getHtmlTree()).hr()
        p.pre("ID: "+str(id(self)))
        return p.simple_page()


class CmdEcho(Process):
    """
       nwebclient.ticker.CmdEcho
       
       Printet CMD-Befehle auf stdout
    """
    
    def __init__(self):
        super().__init__('CmdEcho')
        self.buffer = deque([], 10)
    def cmd(self, args):
        s = ' '.join(map(lambda x: str(x), args))
        self.buffer.append(s)
        print("CMD: " + s)
        return super().cmd(args)
    def htmlContent(self, params={}):
        s = b.Page().div("Buffer:")
        for line in self.buffer:
            s.pre(line)
        return str(s)
    

class CmdOps(Process):
    """
       nwebclient.ticker.CmdOps
       
       /proc?name=CmdOps&exec=cmd
    """
    def __init__(self):
        super().__init__('CmdOps')
    def queue_job(self, job_name):
        print("[CmdOps] queue_job")
        self.cpu.jobs.append(util.Args().env('named_jobs')[job_name])
        return True
    def cmd(self, args):
        if len(args)>=1:
            op = args[0]
            if op == 'add':
                load_from_arg(self.cpu, args[1])
                return True
            if op == 'queue_job':
                return self.queue_job(args[1])
            if op == 'print':
                print(args[1])
                return True
        return super().cmd(args)
    def toHtml(self, params={}):
        s = b.Page()
        s.ul(["add class:params", "queue_job job_def", "print message"])
        if 'exec' in params:
            self.cpu.cmd(params['exec'].split(' '))
            return "Done."
        return str(s)+'<form><input type="text" name="exec" /><input type="hidden" name="name" value="'+params['name']+'" /><input type="submit" name="submit" value="Exec" /></form>'
    

class CmdExec(Process):
    def __init__(self):
        super().__init__('CmdExec')
    def configure(self, arg):
        self.cpu.cmd(arg.split(' '))    


class Ticker(Process):
    last = 0
    interval = 10
    fn = None
    ticks = 0
    def __init__(self, name = 'ticker', interval = 15, fn = None, wait=True):
        super().__init__(name) 
        self.interval = interval
        self.fn = fn
        if wait:
            self.last = int(time.time())
    def tick(self):
        t = int(time.time())
        dur = t - self.last;
        if dur > self.interval:
            self.last = t
            self.ticks = self.ticks + 1
            self.execute()
    def secondsTilNext(self):
        t = int(time.time())
        dur = t - self.last;
        return self.interval - dur
    def cmd(self, args):
        if len(args)>=2 and args[0]==self.name and args[1]=='set_interval':
            self.interval = int(args[2])
            return True
        return super().cmd(args)
    def execute(self):
        if not self.fn is None:
            self.fn()
    def __str__(self):
        return super().__str__() + " interval="+str(self.interval)
    def htmlContent(self, params={}):
        s = ''
        if 'interval' in params:
            self.interval = int(params['interval'])
            s += '<div>Interval aktualisiert</div>'
        url = '?name=' + self.name
        s += "<div>Noch "+str(self.secondsTilNext())+" Sekunden bis zur naechsten Ausfuehrung</div>"
        s += '<div> <a href="'+url+'&interval=1800">Set to 1800 (30min)</a> <a href="'+url+'&interval=900">Set to 900 (15min)</a> </div>'
        return s

        
class PiepTicker(Ticker):
    msg = 'piep'
    def __init__(self, interval = 60):
        super().__init__(name='piep', interval=interval) 
    def execute(self):
        print(self.msg)
        

class InfoTicker(Ticker):
    msg = 'piep'
    def __init__(self, interval = 180):
        super().__init__(name='info_ticker', interval=interval) 
    def execute(self):
        print("Job-Count:     " + str(len(self.cpu.jobs)))
        print("Process-Count: " + str(len(self.cpu.processes)))
        #print("Child-Count:   " + str(len(self.cpu.__childs)))


class FileExtObserver(Ticker):
    def __init__(self, name = 'ext_observer', ext='.sdjob', interval = 15):
        super().__init__(name=name, interval=interval) 
        self.ext = ext
    def configure(self, arg):
        if arg != '':
            self.ext = arg
    def processFile(self, filename):
        pass
    def execute(self):
        print("FileExtObserver")
        filelist = [ f for f in os.listdir('.') if f.endswith(self.ext) ]
        for f in filelist:
            print(self.name + ": Found file: "+ f + " with ext=" + self.ext)
            self.processFile(f)
            
            
class JobFileLoader(FileExtObserver):
    def __init__(self, name = 'job_observer', ext='.job.json', interval = 65):
        super().__init__(name=name, ext=ext, interval=interval) 
    def processFile(self, filename):
        data = util.load_json_file(filename)
        self.cpu.jobs.append(data)


class UrlDownloader(Ticker):
    """
      Laedt periodisch eine URL in eine Datei
    """
    def __init__(self, name = 'UrlDownloader', interval = 3600, url='https://bsnx.net/4.0/', filename='data.txt', fail_on_exists = True):
        super().__init__(name, interval) 
        self.url = url
        self.filename = filename
        self.fail_on_exists = fail_on_exists
    def execute(self):
        res = requests.get(self.url)
        if not (os.path.isfile(self.filename) and self.fail_on_exists):
            with open(self.filename, 'w') as f:
                f.write(self.filename)


class JobFetcher(Ticker):
    def __init__(self, name = 'UrlDownloader', interval=120, url=None):
        super().__init__(name, interval) 
        self.url = url 
    def execute(self):
        res = requests.get(self.url)
        job = json.loads(res.text)
        self.cpu.jobs.append(job)


class TypeJobExecutor(Ticker):
    def __init__(self, name = 'jobtype', interval = 61, executor= None):
        super().__init__(name, interval) 
        self.executor = executor
    def execute(self):
        if len(self.cpu.jobs)>0:
            if self.cpu.jobs[0].type == self.name:
                current = self.cpu.jobs.pop(0)
                result = self.executor(current)
                self.cpu.cmd(['jobresult', result, current])
                print(str(result))
                
                
class JobExecutor(Ticker):
    """
      add nwebclient.ticker.JobExecutor
    """

    def __init__(self, name = 'jobexec', interval = 63, executor= None):
        super().__init__(name, interval) 
        self.executor = executor
        if self.executor is None:
            from nwebclient import runner
            self.executor = runner.JobRunner(runner.AutoDispatcher())
        self.addChild(self.executor)

    def execute(self):
        if len(self.cpu.jobs)>0:
            current = self.cpu.jobs.pop(0)
            result = self.executor(current)
            self.cpu.cmd(['jobresult', result, current])

    def htmlContent(self, params={}):
        return '<div>JobExecutor.htmlContent()</div>'
                
                
class TypeMapJobExecutor(Ticker):
    def __init__(self, name = 'jobtype', interval = 64, executor= None):
        super().__init__(name, interval) 
        self.executor = executor
    def execute(self):
        if len(self.cpu.jobs)>0:
            if self.cpu.jobs[0].type == self.name:
                current = self.cpu.jobs.pop(0)
                result = self.executor(current)
                self.cpu.jobs.append(result)
                

class NWebJobFetch(Ticker):
    """ 
      NWebFetch(NWebClient(...), 42)  
      
      npy-ticker nwebclient.sd.JobFetch:42
      
      Cfg: job_fetch_group_id
    """
    key = None
    supported_types = None
    reject_types = None
    default_can_process = True
    delete_jobs = True
    limit = None
    def __init__(self, interval = 91, nwebclient=None, group=None, supported_types=None, delete_jobs = True, limit = None):
        super().__init__("NWebFetch", interval)
        if nwebclient is None:
            self.debug("Reading from nweb.json")
            nwebclient = NWebClient(None)
        self.nweb = nwebclient
        if group is None:
            group = util.Args().val('job_fetch_group_id')
        self.group = group
        self.supported_types = supported_types
        self.reject_types = None
        self.default_can_process = True
        self.delete_jobs = delete_jobs
        self.limit = limit
    def configure(self, arg):
        params = b.Params(arg)
        if 'group' in params:
            self.group = int(params['group'])
        if 'interval' in params:
            self.interval = int(params['interval'])
        if 'supported_types' in params:
            self.supported_types = params['supported_types'].split(',')
        if 'reject_types' in params:
            self.reject_types = params['reject_types'].split(',')
        #from nwebclient import NWebClient
        #self.nweb = NWebClient()
        #self.group = arg

    def execute(self):
        self.debug("Fetching Jobs...")
        docs = self.nweb.docs('group_id='+str(self.group))
        counter = 0
        for doc in docs:
            self.download(doc)
            counter += 1
            if self.limit is not None and counter > self.limit:
                self.info("Job Download Limit, Stopping Download...")
                break
    def canProcess(self, data):
        if self.reject_types is not None and 'type' in data:
            if data['type'] in self.reject_types:
                return False
        if self.supported_types is not None and 'type' in data:
            if data['type'] in self.supported_types:
                return True
        return self.default_can_process
    def download(self, doc):
        self.log("Start Download")
        content = doc.content()
        data = json.loads(content)
        if self.canProcess(data):
            self.cpu.jobs.append(data)
            if not ('keep' in data and data['keep'] == True) and self.delete_jobs:
                self.nweb.deleteDoc(doc.id())
        else:
            self.log("Not Processing Job")
    def log(self, message):
        print("JobFetch: "+str(message))
        

class NWebJobResultUploader(Process):
    def __init__(self, nwebclient=None, group=None):
        super().__init__("NWebJobResultUploader") 
        if nwebclient is None:
            self.debug("Reading from nweb.json")
            nwebclient = NWebClient(None)
        self.nweb = nwebclient
        if group is None:
            group = util.Args().val('job_result_group_id')
        self.group = group
    def upload(self, data):
        self.nweb.createDoc(data['guid'], json.dumps(data), self.group, kind='json', guid=data['guid'])

    def cmd(self, args):
        if len(args)>=2 and args[0]=='jobresult':
            self.info("Upload to group: " + str(self.group))
            s = json.dumps(args[1])
            name = 'job_result'
            if 'type'in args[1]:
                name = name+'_'+args[1]['type']
            if 'name'in args[1]:
                name = str(args[1].name)+'_result'
            self.nweb.createDoc(name, s, self.group, kind='json', guid=args[1].get('guid', ''))
            self.info("Upload Done.")
            return True
        return super().cmd(args)


class UrlPostShTicker(Ticker):
    """
      Sendet Daten an einen POST-Endpoint
      
      nwebclient.ticker.UrlPostShTicker
      
      Sh URL wie folgt: https://bsnx.net/4.0/w/d/514419/sh/3bab31c346b631a34c4fe7689f551330
    """
    SETTINGS = ['ticker_sh_url']
    uptime_counter = 0
    def __init__(self, name = 'UrlPostShTicker', interval = 3600, url=None):
        super().__init__(name, interval, wait=False) 
        if url is None:
            url = util.Args().val('ticker_sh_url')
        self.url = url  
    def execute(self):
        self.uptime_counter = self.uptime_counter + self.interval
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        requests.post(self.url, data={'uptime': str(self.uptime_counter)+"s up, "+current_time})
        
        
class PeriodicalCronJob(Ticker):
    """
      Settings: named_jobs
    """
    enabled = True
    def __init__(self, name = 'PeriodicalCronJob', interval = 3600, named_job_name=None):
        super().__init__(name, interval)
        self.named_job_name = named_job_name
    def configure(self, arg):
        print("[PeriodicalCronJob] configure with "+ str(arg))
        self.named_job_name = arg
        if self.name == 'PeriodicalCronJob':
            self.name = arg
        if self.interval == 3600:
            self.interval = random.randrange(1800, 3900)
    def cmd(self, args):
        if len(args)>=2 and args[0]==self.name: 
            if args[1]=='enable':
                self.enabled = True
            if args[1]=='disable':
                self.enabled = False
        return super().cmd(args)
    @action(title="Enable")
    def enable(self):
        self.enabled = True
    @action(title="Disable")
    def disable(self):
        self.enabled = False
    def execute(self):
        jobs = util.Args().env('named_jobs')
        if self.named_job_name in jobs:
            if self.enabled:
                print("[PeriodicalCronJob] Job "+self.named_job_name+" queued.")
                self.cpu.jobs.append(jobs[self.named_job_name])
        else:
            print("[PeriodicalCronJob] Error: Job "+ self.named_job_name + "not found.")
    

class WebProcess(Process):
    """ 
       from nwebclient.ticker import WebProcess
       w = WebProcess(port=9999)
    """
    web = None

    def __init__(self, port = 9080, host=None, start=True, process_routes=True):
        super().__init__('WebProcess')
        self.port = port
        self.process_routes = process_routes
        if host is None:
            self.host = util.Args().env('webprocess_host', '127.0.0.1')
        else:    
            self.host = host
        if start:
            self.startServer()

    def addChild(self, child):
        super().addChild(child)
        name = getattr(child, 'name', None)
        if name is not None:
            self.register(name, child)
        return child

    def startServer(self):
        f = lambda: self.startAsync()
        self.thread = threading.Thread(target=f)
        self.thread.start()

    def index(self):
        s = b.Page().h1("Prozesse")
        s.ul(map(lambda p: '<a href="proc?name='+p.name+'">'+str(p)+'</a>', self.cpu.processes))
        s.hr().div('Jobs: ' + str(len(self.cpu.jobs)))
        s.ul(['<a href="registry">Ticker-Registry</a>','<a href="root">Root</a>', '<a href="nws">Module</a>'])
        s.hr().div('nweb web ui; Python' +sys.version)
        return s.simple_page()

    def proc(self):
        from flask import request
        name = request.args.get('name')
        params = request.args.to_dict()
        p = self.cpu[name]
        if p is None:
            return "Error: Process not found."
        return str(p.toHtml(params=params))

    def prop(self):
        from flask import request
        name = request.args.get('name')
        p = self.cpu[name]
        return str(getattr(p, request.args.get('prop'), ''))

    def registry(self):
        s = b.Page().h1("Ticker Registry")
        s.ul(map(lambda t: t.name, b.Plugins('nweb_ticker')))
        return s.simple_page()

    def obj(self):
        import ctypes
        from flask import request
        x = int(request.args.get('id'))
        a = ctypes.cast(x, ctypes.py_object).value
        w = b.WebObject(a, request.args.to_dict())
        self.addChild(w)
        return w.page()

    def register(self, name, method):
        route = '/pysys/' + name
        if name == 'index':
            route = '/'
        if isinstance(method, b.WebPage):
            from flask import request
            self.web.add_url_rule(route, name, lambda: method.page(request.args.to_dict()))
        else:
            self.web.add_url_rule(route, name, lambda: method())
        return self

    def page_not_found(self, e):
        from flask import request
        return "Error: 404, Path:" + request.path

    def createApp(self):
        from flask import Flask
        app = Flask(self.name)
        self.web = app
        if self.process_routes:
            self.register('index', self.index)
            self.register('prop', self.prop)
            self.register('proc', self.proc)
            self.register('registry', self.registry)
            w.route_root(self.web, self.cpu) # self.register('root', self.root)
            self.register('obj', self.obj)
            app.add_url_rule('/pysys/status', 'status', lambda: "ok")
            app.add_url_rule('/pysys/processes', 'processes', lambda: str(self.cpu.processes))
            app.add_url_rule('/pysys/job-count', 'job_count', lambda: str(len(self.cpu.jobs)))
        app.register_error_handler(404, lambda e: self.page_not_found(e))      
        self.addChild(w.NwFlaskRoutes())
        return app

    def startAsync(self):
        app = self.createApp()
        app.run(port=self.port, host=self.host)
          

class MqttSub(Process):
    MODULES = ['paho-mqtt']
    topic = 'main'
    host = '127.0.0.1'
    port = 1883
    client_id = f'python-mqtt-{random.randint(0, 1000)}'

    def __init__(self, name='MQTT', topic='main', host='127.0.0.1'):
        super().__init__(name)  
        self.topic = topic
        self.host = host
        self.connect()

    def connect(self):
        from paho.mqtt import client as mqtt_client
        print("[MqttSub] Connect to " + self.host + " Topic: " + self.topic)
        client = mqtt_client.Client(self.client_id, transport='tcp')
        #client.username_pw_set(username, password)
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
                client.subscribe(self.topic)
            else:
                print("Failed to connect, return code %d\n", rc)
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.cpu.cmd(msg.payload.decode().split(' '))
        #def on_log(client, userdata, level, buf):
        #    print("MQTT Log")
        client.on_connect = on_connect
        client.on_message = on_message
        #client.on_log = on_log
        client.connect_async(self.host, self.port, keepalive=6000)
        client.loop_start()
        

class MqttPub(Process):
    """ Sendet alle CMD-Strings an MQTT """
    MODULES = ['paho-mqtt']
    topic = 'main'
    host = '127.0.0.1'
    port: int = 1883
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    client = None

    def __init__(self, name='MQTT', topic='main', host = '127.0.0.1'):
        super().__init__(name)  
        self.topic = topic
        self.host = host
        if self.host is not None:
            self.start_client()

    def start_client(self):
        from paho.mqtt import client as mqtt_client
        try:
            self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, self.client_id, transport='tcp')
            self.client.connect(self.host, self.port)
        except Exception as e:
            print("MQTT Error: " + str(e))

    def __call__(self, topic, msg):
        self.publish(msg, topic)

    def cmd(self, args):
        msg = ' '.join(args)
        self.publish(msg)
        return super().cmd(args)

    def publish(self, msg, topic=None):
        if topic is None:
            t = self.topic
        else:
            t = topic
        if self.client is not None:
            self.client.publish(t, msg)
        else:
            print("NO-MQTT-SEND: " + t + ": " + msg)
        

class Buffer(Process):
    """ 
      Speicher Nachrichten zwischen und ruft onFull auf wenn Voll oder nach einem TimeOut
    """
    buf = []
    lastAddTime = 0

    def __init__(self, name='Buffer', size=100, timeout = 180):
        super().__init__(name)  
        self.size = size
        self.timeout = timeout
        self.lastAddTime = int(time.time())

    def tick(self):
        if self.timeout < int(time.time())-self.lastAddTime and len(self.buf)>0:
            self.onFull()

    def onFull(self):
        print("BufferOverflow")

    def clear(self):
        self.buf = []

    def cmd(self, args):
        self.buf.append(' '.join(args))
        self.lastAddTime = int(time.time())
        if len(self.buf)>=self.size:
            self.onFull()
        return super().cmd(args)

    
class NWebDataDoc(Buffer):

    def __init__(self, name='NWebDataDoc', size=100, timeout = 180, url='https://bsnx.net/4.0/', guid=None, token=None):
        super().__init__(name,size,timeout)  
        if guid is None:
            print("GUID must be to an Document")
        self.url = url
        self.guid = guid
        self.token = token

    def sendData(self, data):
        url = self.url + 'w/d/' + self.guid + '/set'
        d = {
            'content': data,
            'token': self.token
        }
        response = requests.post(url, data=d)

    def onFull(self):
        data = json.dumps(self.buf)
        self.sendData(data)
        self.clear()

        
class NWebDataDocPop(Ticker):
    """
      DataDoc
    """

    def __init__(self, name='ticker', interval=120, url='https://bsnx.net/4.0/', guid=None, token=None):
        super().__init__(name, interval) 
        self.url = url
        self.guid = guid
        self.token = token

    def is_json(self,myjson):
        try:
            json.loads(myjson)
        except ValueError as e:
            return False
        return True

    def execute(self):
        res = requests.get(self.url+'w/d/'+self.guid+'/pop', params={'token':self.token})
        if self.is_json(res.text):
            array = json.loads(res.text)
            for item in array:
                self.cpu.cmd(item.split(' '));
        else:
            print("NWebDataDocPop: Invalid JSON")


class Cpu(b.Base):
    processes = []
    sleep_time = 1
    jobs = []

    def __init__(self, *args):
        super().__init__()
        for arg in args:
            self.add(arg)

    def __iter__(self):
        return self.processes.__iter__()

    def add(self, process):
        process.cpu = self
        self.addChild(process)
        self.processes.append(process)
        return self

    def tick(self):
        for p in self.processes:
            try: 
                p.tick()
            except Exception as e:
                print("[CPU] Error in Tick Process "+ p.name + ": " + str(e) )
                print(traceback.format_exc());
        if self.sleep_time > 0:
            time.sleep(self.sleep_time)

    def cmd(self, args):
        res = False
        for p in self.processes:
            try:
                res = p.cmd(args) or res
            except Exception as e:
                print("[CPU] Error in CMD Process "+ p.name + ": " + str(e) )
                return False
        return res

    def loop(self):
        while True:
            self.tick()

    def loopAsync(self):
        f = lambda: self.loop()
        x = threading.Thread(target=f)
        x.start()
        return x

    def runTicks(self, count=100) :
        for i in range(count):
             self.tick()

    def __getitem__(self, name):
        for p in self.processes:
            if p.name == name:
                return p
        return None

    def __str__(self):
        s = "Cpu("
        for p in self.processes:
            s = s + ' ' + str(p)
        s += ')'
        return s


def load_class(cl):
    d = cl.rfind(".")
    classname = cl[d+1:len(cl)]
    m = __import__(cl[0:d], globals(), locals(), [classname])
    return getattr(m, classname)


def load_from_arg(cpu, arg):
    try:
        a = arg.split(':')
        a.append('')
        cls = load_class(a[0])
        c = cls()
        cpu.add(c)
        c.configure(''.join(a[1:]))
    except Exception as e:
        print("[nwebclient.ticker] load_from_arg faild for " +str(arg)+", Error: " +str(e))
        print(traceback.format_exc())


def create_cpu(arg):
    params = arg.val('ticker', [])
    if '1'==params:
        params = arg.env('ticker', [])
    cpu = Cpu()
    for param in params:
        print("[CPU] Loading: " + str(param))   
        load_from_arg(cpu, param)
    return cpu


def help():
    print("Help")


def main():
    print("npy-ticker")
    print("npy-ticker namespace.Proc:cfg ...")
    print("")
    print("  nwebclient.ticker.WebProcess")
    print("  nwebclient.ticker.CmdOps")
    print("")
    args = util.Args()
    if args.help_requested:
        return help()
    cpu = create_cpu(args)
    for arg in sys.argv[1:]:
        print("[nwebclient.ticker] Loading: " + str(arg))   
        load_from_arg(cpu, arg)
    print(str(cpu))
    print("[nwebclient.ticker] Looping...")
    cpu.loop()
    

if __name__ == '__main__':  # npy-ticker vom python-package bereitgestellt
    main()
