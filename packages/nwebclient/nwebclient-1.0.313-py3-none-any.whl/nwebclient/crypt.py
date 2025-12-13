from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import os
import hashlib
import codecs
import binascii
import base64
from cryptography.fernet import Fernet


def encrypt_message(message, password: str):
    hlib = hashlib.md5()
    hlib.update(password.encode('utf-8'))
    key = base64.urlsafe_b64encode(hlib.hexdigest().encode('utf-8'))
    fernet = Fernet(key)
    return fernet.encrypt(message.encode('utf-8')).decode('utf-8')


def decrypt_message(message, password: str):
    hlib = hashlib.md5()
    hlib.update(password.encode('utf-8'))
    key = base64.urlsafe_b64encode(hlib.hexdigest().encode('utf-8'))
    fernet = Fernet(key)
    return fernet.decrypt(message).decode('utf-8')


def generate_key_pair(save_to_file=True):
    """
      Erstellt einen Public-Private Schlüsselpar und speichert es als Datei private_key.pem und public_key.pem
    """
    result = {}
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()

    pem = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    result['private_key'] = pem
    if save_to_file:
        with open('private_key.pem', 'wb') as f:
            f.write(pem)
    pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    if save_to_file:
        with open('public_key.pem', 'wb') as f:
            f.write(pem)
    result['public_key'] = pem
    return result


def encrypt(message, public_key_file="public_key.pem"):
    """
      Verschlüsselt einen kurzen Text mit dem Öffentlchen Schlüssel
      256-Byte Limit
    """
    with open(public_key_file, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())
    return public_key.encrypt(message,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(), label=None))


def encryptFile(in_file, out_file, public_key_file="public_key.pem"):
    """
      Erwartet einen public_key.pem und legt den Schuessel fuer die Datei in {out_file}.key per RSA verschuesselt ab
    """
    key = Fernet.generate_key()
    ekey = encrypt(key, public_key_file=public_key_file)
    hexlify = codecs.getencoder('hex')
    hkey=hexlify(ekey)[0]
    fernet = Fernet(key)
    with open(in_file, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(out_file, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    with open(out_file+".key", 'wb') as encrypted_file:
        encrypted_file.write(ekey)
    

def decrypt(encrypted, key_filename="private_key.pem"):
    """
      Asynchrones Decrypt
      Erwartet eine private_key.pem (oder im Parameter key_filename angegeben)
    """
    with open(key_filename, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(),password=None, backend=default_backend())
    return private_key.decrypt(encrypted, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))


def decryptFile(in_file, out_file, key_filename="private_key.pem"):
    """
      Entschlüsselt eine Datei
    """
    with open(in_file+".key", 'rb') as encrypted_file:
        ekey = encrypted_file.read()
    key = decrypt(ekey, key_filename=key_filename)
    fernet = Fernet(key)
    with open(in_file, 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(out_file, 'wb') as dec_file:
        dec_file.write(decrypted)
    #binary_string = binascii.unhexlify(hex_string)
    #with open("private_key.pem", "rb") as key_file:
    #    private_key = serialization.load_pem_private_key(key_file.read(),password=None, backend=default_backend())
    #with open(in_file, "rb") as f:
    #    content = private_key.decrypt(f.read(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))
    #with open(out_file, 'wb') as f:
    #    f.write(content) 


if __name__ == '__main__':
    print("crypt")
