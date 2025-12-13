
import sqlite3
import io
import sys
import os.path

nxfiles_sql = """CREATE TABLE IF NOT EXISTS nxfiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255),
        prompt VARCHAR(255),negativ_prompt VARCHAR(255), guidance_scale FLOAT,
        data BLOB, 
        extra VARCHAR(255) DEFAULT '',
        ext VARCHAR(10) DEFAULT 'jpg',
        c_key VARCHAR(255) DEFAULT '')
"""

def sdb_write(data, prompt = '', negativ_prompt = '', guidance_scale = 5, name='data', dbfile='data.db', extra = None, c_key = ''):
    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        cursor.execute(nxfiles_sql)
        sqlite_insert_blob_query = """ INSERT INTO nxfiles
                     (name, prompt, negativ_prompt, guidance_scale, data, extra,      c_key) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        data_tuple = (name, prompt, negativ_prompt, guidance_scale, data, str(extra), c_key)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Data Stored.")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            
def write_crypt(data, prompt, negativ_prompt, guidance_scale, name='data', dbfile='data.db', extra = None, public_key = None):
    from cryptography.fernet import Fernet
    from nwebclient import crypt
    key = Fernet.generate_key()
    if len(public_key)< 30:
        with open("public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())
    else:
        public_key = serialization.load_pem_public_key(public_key, backend=default_backend())
    ekey = public_key.encrypt(message,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(), label=None))
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    sdb_write(data, prompt, negativ_prompt, guidance_scale, name, dbfile, extra = None, c_key=str(ekey))

def sdb_write_pil(img, prompt, negativ_prompt, guidance_scale, name='data', dbfile='data.db', extra = None):
    #img = Image.open("p67b2.jpg")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    #img.close()
    sdb_write(img_byte_arr.read(), prompt, negativ_prompt, guidance_scale, name, dbfile, extra)

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    #print("Stored blob data into: ", filename, "\n")
    
def inc(i=1000, dbfile='data.db'):
    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        cursor.execute("UPDATE nxfiles SET id = id + "+ str(i))
        sqliteConnection.commit()
        print("Inc")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to inc", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def sdb_extract(dbfile='data.db'):
    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        sql_fetch_blob_query = """SELECT id, name, data from nxfiles"""
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1])
            name = row[1]
            id = row[0]
            data = row[2]
            filename = name+"_"+str(id)+".jpg"
            print("Write File: " + filename)
            writeTofile(data, filename)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def extract_from(id,dbfile='data.db'):
    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        sql_fetch_blob_query = """SELECT id, name, data from nxfiles WHERE id >= ?"""
        cursor.execute(sql_fetch_blob_query, [id])
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1])
            name = row[1]
            id = row[0]
            data = row[2]
            filename = name+"_"+str(id)+".jpg"
            print("Write File: " + filename)
            writeTofile(data, filename)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            
def show(dbfile='data.db'):
    if not os.path.isfile(dbfile):
        print("File "+dbfile+" not exists")
        return
    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        sql = """SELECT name, id from nxfiles WHERE id = (SELECT MIN(id) FROM nxfiles)"""
        cursor.execute(sql)
        record = cursor.fetchall()
        for row in record:
            print("From: "+str(row[0]) + " ID: "+str(row[1]))
        sql = """SELECT name, id from nxfiles WHERE id = (SELECT MAX(id) FROM nxfiles)"""
        cursor.execute(sql)
        record = cursor.fetchall()
        for row in record:
            print("To: "+str(row[0]) + " ID: "+str(row[1]))
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    
            
def count(dbfile='data.db'):
    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        sql = """SELECT COUNT(id) from nxfiles"""
        cursor.execute(sql)
        record = cursor.fetchall()
        for row in record:
            print(""+str(row[0]))
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            
def clear(dbfile='data.db'):
    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        sql = """DELETE FROM nxfiles"""
        cursor.execute(sql)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            
def inc(dbfile='data.db'):
    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        sql = """UPDATE nxfiles SET id = id + 1000"""
        cursor.execute(sql)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            
def sortin(dbfile='data.db'):
    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        sql_fetch_blob_query = """SELECT id, name, data from nxfiles"""
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1])
            name = row[1]
            id = row[0]
            data = row[2]
            i = 0
            if not os.path.isdir(name):
                os.mkdir(name)
            filename = name+"/"+name+'_'+str(id)+".jpg"
            while os.path.isfile(filename):
                i = i+1
                filename = name+"/"+'_'+name+'_'+str(id+i)+".jpg"
            print("Write File: " + filename)
            writeTofile(data, filename)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            
def upload(group_id, dbfile='data.db'):
    print("Uploading...")
    from nwebclient import NWebClient
    n = NWebClient(None)
    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        sql_fetch_blob_query = """SELECT id, name, data from nxfiles"""
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1])
            name = row[1]
            id = row[0]
            data = row[2]
            #writeTofile(data, filename)
            n.createFileDoc(name, group_id, data)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            
def get(id, dbfile='data.db'):
    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        sql_fetch_blob_query = """SELECT id, name, data from nxfiles WHERE id = ?"""
        cursor.execute(sql_fetch_blob_query, [id])
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1])
            name = row[1]
            id = row[0]
            data = row[2]
            writeTofile(data, name)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    

def show_usage():
    print("")
    print(" show        Zeigt eine Zusammenfassung der Daten an")
    print(" extract     Extrahiert alle Dateien")
    print(" from        Extrahiert ab einer id")
    print(" count       Gibt die Anzahl der Datensätze aus")
    print(" clear       Löscht alle Daten in der Datenbank")
    print(" sortin      Sortiert die extrahierten Dateien anhand der Namen in Verzeichnisse")
    print(" inc         Erhöht alle IDs")
    print(" add         Fügt eine Datei hinzu")
    print(" get         Extrahiert eine Datei")
    print(" upload {group_id}     Laedt zu einer nweb Instanz hoch")
    print("")
    

def main():
    print("SDB")
    print("Usage nx-sdb (show|extract|from|count|clear|sortin|inc|add|get|upload)")
    print("Use --help to show usage information")
    show_usage()
    #print(str(sys.argv)) # 0-path
    if len(sys.argv)>1:
        op = sys.argv[1]
        if op == 'count':
            count()
        elif op=='extract':
            sdb_extract()
        elif op=='inc':
            inc()
        elif op =='from':
            print("Extract from id:"+str(sys.argv[2]))
            extract_from(int(sys.argv[2]))
        elif op =='sortin':
            sortin()
        elif op =='inc':
            inc(int(sys.argv[2]))
        elif op == 'add':
            sdb_write(open(sys.argv[2], 'r'), name=sys.argv[2])
        elif op == 'get':
            get(sys.argv[2])
        elif op == 'upload':
            upload(sys.argv[2])
        elif op == '--help':
            show_usage()
        else:
            print("Error: Unknown Operation")
    else:
        show()
   
# complete -W "show extract from count clear sortin inc" nx-sdb
if __name__ == '__main__': # nx-sdb vom python-package bereitgestellt
    main()