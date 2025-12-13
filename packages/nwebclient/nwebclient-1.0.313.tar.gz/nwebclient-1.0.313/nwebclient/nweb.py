
import json
from os.path import exists
import sqlite3
from sqlite3.dbapi2 import Cursor
import hashlib
import datetime
import requests

def loadConfig():
    cfg_files = ['./nweb.json', '/etc/nweb.json']
    for cfg_file in cfg_files:
        if exists(cfg_file):
            with open(cfg_file) as f:
                return json.load(f)
    return {
        'NPY_URL': ''
    }


nweb_cfg = loadConfig()

def nw_dbconnect(cfg=None):
    """
      Liefert eine Python-DBAPI Connection zurueck
    """
    if cfg is None:
        cfg = nweb_cfg
    if 'DB_HOST' in cfg:
        h = cfg['DB_HOST']
        u = cfg['DB_USER']
        from mysql import connector
        return connector.connect(host=h, user=u, password=cfg['DB_PASSWORD'], database=cfg['DB_NAME'])
    elif 'DB_SQLITE' in cfg:
        return sqlite3.connect(cfg['DB_SQLITE'], check_same_thread=False)
    else:
        raise Exception("No Database Configuration")


def nw_gtoken():
    """
       Generiert einen Token für den Zugriff aud die ?????-API
    """
    hstr = datetime.datetime.now().strftime('%Y-%m-%d') + nweb_cfg['V4_INNER_SECRET']
    return hashlib.md5(hstr.encode()).hexdigest()

def nweb_req(path):
    from flask import request
    try:
        id = request.cookies['PHPSESSID']
        url = nweb_cfg['url'] + path # Alternativ NWEB_URL ?
        cookies = {'PHPSESSID': id}
        r = requests.get(url, cookies=cookies, verify=False)
        return r.json()
    except Exception as e:
        return {'success': False, 'message': "Request Error", 'path': path, 'exception': str(e)}