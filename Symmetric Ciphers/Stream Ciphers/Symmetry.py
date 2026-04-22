import requests
import json
from binascii import *
import string

def encrypted_flag():
    url = "http://aes.cryptohack.org/symmetry/encrypt_flag/"
    r = requests.get(url)
    c = (json.loads(r.text))['ciphertext']
    iv = c[:32]
    ct = c[32:]
    return iv, ct

def get_encryption(pt_hex,iv_hex):
    url = "http://aes.cryptohack.org/symmetry/encrypt/"+pt_hex+"/"+iv_hex
    r = requests.get(url)
    try:
        ct = (json.loads(r.text))['ciphertext']
    except:
        ct = (json.loads(r.text))['error']
    return ct

iv,ct = encrypted_flag()
pt = b'crypto{'
while 1:
    for i in string.printable:
        e = get_encryption(hexlify(pt+i.encode()).decode(),iv)
        if e == ct[:2*(len(pt)+1)]:
            pt += i.encode()
            print(pt.decode())
            break
    if pt.decode().endswith('}'):
        print(pt.decode())
        break