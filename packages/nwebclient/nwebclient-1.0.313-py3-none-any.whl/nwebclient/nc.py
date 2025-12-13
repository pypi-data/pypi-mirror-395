
import sys
import os
import io
import time

from nwebclient import NWebClient
from nwebclient import util

class DocMap:
    def __init__(self, executor, meta_value_key, base, dict_map):
        self.count = 0
        self.executor = executor
        self.meta_value_key = meta_value_key
        self.base = base
        if isinstance(dict_map, str):
            self.dict_map = dict_map.split(':')
        else: 
            self.dict_map = ['title', 'mapped_title']
    def __call__(self, doc, nclient):
        data = self.base | doc.to_dict()
        if doc.is_image():
            doc.downloadThumbnail('docmap.jpg', 'm')
            data['image_filename'] = 'docmap.jpg'
        data[self.dict_map[1]] = data[self.dict_map[0]]
        result = self.executor(data)
        self.count += 1
        return result[self.meta_value_key]
                
def mapDocs(n, args):
    meta_ns = args.getValue('meta_ns')
    meta_name = args.getValue('meta_name')
    filterArgs = args.getValue('filter', 'kind=image')
    limit = int(args.getValue('limit', 1000))
    update = bool(args.getValue('update', True))
    meta_value_key = args.getValue('meta_value_key')
    executor = args.getValue('executor')
    dict_map = args.getValue('dict_map', None)
    base = args.getValue('base', None)
    print("Params:")
    print("  pwd             " + os.getcwd())
    print("  meta_ns:        " + meta_ns)
    print("  meta_name:      " + meta_name)
    print("  filter:         " + filterArgs)
    print("  limit:          " + str(limit))
    print("  update:         " + str(update))
    print("  meta_value_key: " + meta_value_key)
    print("  executor:       " + str(executor))
    print("  base:           " + str(base))
    print("  dict_map:       " + str(dict_map))
    print("")
    exe = util.load_class(executor, create=True)
    if base is None:
        base = {}
    else:
        base = util.load_json_file(base)
    fn = DocMap(exe, meta_value_key, base, dict_map)
    n.mapDocMeta(meta_ns=meta_ns, meta_name=meta_name, filterArgs=filterArgs, limit=limit, update=update, mapFunction=fn)


def create_archive(file='nweb.db', filter='kind=image', instance='default'):
    import sqlite3
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nweb_input (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guid VARCHAR(255),
        data BLOB)
    """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS nweb_result (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guid VARCHAR(255),
            ns VARCHAR(255),
            name VARCHAR(255),
            value VARCHAR(1024))
        """)
    nc = NWebClient(instance)
    for d in nc.docs(filter):
        if d.is_image():
            tuple_data = (d.guid(), d.getThumbnail('m'))
        else:
            tuple_data = (d.guid(), d.content())
        cursor.execute("INSERT INTO nweb_input (guid, data) VALUES (?,?)", tuple_data)
    connection.commit()
    cursor.close()
    connection.close()


def create_nweb_job(file='nweb.db', filter='kind=json', instance='default'):
    import sqlite3
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nweb_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            result TEXT) """)
    nc = NWebClient(instance)
    for d in nc.docs(filter):
        cursor.execute("INSERT INTO nweb_jobs (data, result) VALUES (?,?)", (d.content(), ''))
    connection.commit()
    cursor.close()
    connection.close()


def map_nweb_archive(file='nweb.db', ns='processed', name='value', mapFn=None):
    class InputDoc:
        def __init__(self, row):
            self._guid = row[1]
            self.data = row[2]
        def guid(self):
            return self._guid
        def downloadThumbnail(self, file='current.jpg', size='m'):
            with open(file, 'wb') as f:
                f.write(self.data)
    import sqlite3
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM nweb_input WHERE guid NOT in (SELECT guid FROM nweb_result)")
    i = 0
    for row in cursor.fetchall():
        try:
            doc = InputDoc(row)
            value = mapFn(doc, None)
            tuple_data = (doc.guid(), ns, name, value)
            cursor.execute("INSERT INTO nweb_result (guid, ns, name, value) VALUES (?,?,?,?)", tuple_data)
            # TODO delete input?
            connection.commit()
            print(f"{i} Processed.")
        except Exception as e:
            print("Error:" + str(e))
        i += 1
    print(f"Done")
    connection.close()



def read_archive_metadata(file, instance):
    import sqlite3
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    cursor.execute("SELECT guid, ns, name, value FROM nweb_result")
    nc = NWebClient(instance)
    i = 0
    for row in cursor.fetchall():
        d = nc.doc(row[0])
        d.setMetaValue(row[1], row[2], row[3])
        print(f"{i} Processing {d.name()}")
        i += 1
        time.sleep(0.1)
    cursor.close()
    connection.close()


def main():
    print("python -m nwebclient.nc")
    print("Params: ")
    print("  - dict_map Abbildung des JobResults auf nweb:meta")
    c = NWebClient(None)
    args = util.Args()
    if args.hasFlag('map'):
        mapDocs(c, args)
    elif args.hasFlag('create_archive'):
        create_archive()
    else:
        print(sys.argv)
        print(str(c.docs()))


if __name__ == '__main__': 
    main()
