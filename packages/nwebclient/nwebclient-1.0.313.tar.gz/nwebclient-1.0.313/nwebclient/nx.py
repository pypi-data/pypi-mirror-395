"""
  High Level Computer functions

  npy

"""

import json
from json.decoder import JSONDecodeError
import os
import os.path
import socket
import time
from threading import Thread
import requests

from nwebclient import util
from nwebclient import runner
from nwebclient import NWebClient


def get_ip():
    def linux_ip():
        cmd = 'ip -j address'
        for itm in json.loads(runner.ProcessExecutor(cmd).waitForEnd().text()):
            if itm['ifname'] != 'lo':
                return itm['addr_info'][0]['local']
        return "127.0.0.7"
    try:
        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith('127'):
            ip = linux_ip()
        return ip
    except:
        try:
            return linux_ip()
        except:
            return "127.0.0.8"


def get_name():
    return socket.gethostname()

def get_ssid():
    s = runner.ProcessExecutor('iwgetid').waitForEnd().stdout
    if len(s) > 0:
        a = s[0].strip().split('ESSID:')
        if len(a) > 0:
            return a[1].replace('"', '')
    return ''

def udp_send(data, ip='255.255.255.255', port=4242):
    bindata = data.encode('ascii')
    #interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
    #allips = [ip[-1][0] for ip in interfaces]
    #for ip in allips:
    #    sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM,  socket.IPPROTO_UDP)  # UDP
    #    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #    sock.bind((ip, 0))
    #    if isinstance(data, list):
    #        data = ' '.join(data)
    #    print("sending: " + data)
    #    sock.sendto(data.encode('ascii'), (ip, port))
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        if ip == '255.255.255.255':
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(bindata, (ip, port))
    

def system(args):
    help_system()
    args.dispatch(
        bluetooth_serial_enable=lambda args: system_bluetooth_serial_enable(args)
    )

def system_exec(cmd):
    print("Executing: " + cmd)
    os.system(cmd)


def system_bluetooth_serial_enable(args):
    print("")
    f = '/etc/systemd/system/dbus-org.bluez.service'
    print("Configure: " + f)
    if not os.path.isfile(f):
        print("Bluetooth Config not exists. File: " + f)
        return;
    os.system(f"cp {f} {f}.bak")
    lines = util.file_get_lines(f)
    def line_transform(line):
        if line.startswith('ExecStart='):
            return 'ExecStart=/usr/lib/bluetooth/bluetoothd -C\nExecStartPost=/usr/bin/sdptool add SP'
        else:
            return line
    lines = map(line_transform, lines)
    util.file_put_contents(f, '\n'.join(lines))
    print("Config rewrite done.")
    print("   bluetoothctl pairable on")
    system_exec("systemctl daemon-reload")
    system_exec("systemctl restart bluetooth.service")
    system_exec("bluetoothctl discoverable on")
    print("")
    print(" Verify: sudo service bluetooth status")
    print(" Usage: nwebclient.runner:BluetoothSerial")
    # sudo rfcomm watch hci0


class IpUdpSender(runner.BaseJobExecutor):
    """
       "send_ip": "nwebclient.nx:IpUdpSender"
    """

    type = 'send_ip'
    interval = 60
    name = 'npy'
    ip = None

    def __init__(self, name=None, start=True):
        super().__init__()
        self.var_names.append('ip')
        self.ip = get_ip()
        if name is None:
            self.name = get_name()
        else:
            self.name = name
        if start:
            self.start_thread()

    def start_thread(self):
        self.thread = Thread(target=lambda: self.loop())
        self.thread.start()

    def udp_send(self):
        udp_send('nxudp ' + self.name + ' ' + str(get_ip()) + " from-npy IpUdpSender")

    def loop(self):
        while True:
            try:
                time.sleep(self.interval)
                self.udp_send()
            except Exception as e:
                self.error("IpUdpSender: " + str(e))

    def execute(self, data):
        self.udp_send()
        return {}


class NxSystemRunner(runner.LazyDispatcher):
    def __init__(self):
        super().__init__('type')
    def prn(self, msg):
        pass
    def execute(self, data):
        if 'enable_send_ip' in data:
            self.loadRunner('send_ip', IpUdpSender())
            return {'success': True}
        else:
            return super().execute(data)

def run(args):
    """
     Startet einen Runner Job
    """
    url = args.env('default_runner_url', 'http://127.0.0.1:7070/')
    response = requests.get(url, args.to_dict())
    try:
        result = response.json()
        print(json.dumps(result, indent=2))
    except JSONDecodeError:
        print("Invalid JSON")
        print(response.text)

def enqueue_job(args):
    nc = NWebClient(None)
    print("Sending to " + str(nc))
    jg = nc.group('98234B940511500B314C972590E3D7B4')
    f = args.shift()
    print("Loading JSON: " + f)
    jd = util.load_json_file(f)
    if jd.get('type') == 'multi':
        for item in jd.get('jobs'):
            jg.create_doc('enq-job', json.dumps(item), 'json')
    else:
        jg.create_doc('enq-job', util.file_get_contents(f), 'json')


def help_system():
    print("npy system - Linux System Configuration")
    print("")
    print("  sudo npy system bluetooth-serial-enable")
    print("")
    print("sudo required")

def help_serv():
    print("npy-server")


def help(topic=''):
    if isinstance(topic, util.Args) and topic.first() == 'system':
        help_system()
    elif isinstance(topic, util.Args) and topic.first() == 'serv':
        help_serv()
    else:
        print('Topic: ' + str(topic))
        print('Usage: ')
        print('  npy send_ip       Macht die IP per UDP Broadcast bekannt')
        print('  npy ip            IP die aktuelle IP-Adresse aus')
        print('  npy run           Startet einen Job')
        print('  npy system        siehe npy help system')
        print('  npy serv          Startet einen Runner (--rest)')
        print('')
        print('Help: npy help topic')
        print('')
        print('Tipps:')
        print('  Cron-Job')
        print('    */10  * * * * npy send_ip')
        print('')


def serv(args):
    args.argv.append('--rest')
    runner.run(args)

def main():
    args = util.Args()
    args.shift()
    if args.help_requested():
        return help()
    else:
        r = NxSystemRunner()
        if args.hasShortFlag('send_ip') or args.hasName('send_ip'):
            udp_send('nxudp npy' + str(get_ip()) + " from-npy")
        elif args.hasShortFlag('ip') or args.hasName('ip'):
            print(get_ip())
        elif r.support_type(args.first()):
            args.cfg = {'type': args.first()}
            res = r.execute(args)
            print(r.to_text(res))
        else:
            args.dispatch(
                system=system,
                run=run,
                enqueue_job=enqueue_job,
                serv=serv,
                help=help
            )


if __name__ == '__main__':
    main()
