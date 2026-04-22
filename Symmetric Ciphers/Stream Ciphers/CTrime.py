import requests
import string
import time

def encrypt(plain):
    url = 'http://aes.cryptohack.org/ctrime/encrypt/'
    rsp = requests.get(url + plain + '/')
    return rsp.json()['ciphertext']

alphabet = '}'+'!'+'_'+'@'+'?'+string.ascii_uppercase+string.digits+string.ascii_lowercase

def bruteforce():
    flag = b'crypto{'
    cipher = encrypt(flag.hex())
    mi = len(cipher)
    while True:
        for c in alphabet:
            cipher = encrypt((flag+c.encode()).hex())
            print(c, len(cipher))
            if mi == len(cipher):
                flag += c.encode()
                mi = len(cipher)
                print(mi, flag)
                break
            if c == alphabet[-1]:
                mi += 2
                break
            time.sleep(1)
        if flag.endswith(b'}'): 
            print(flag)
            break

bruteforce()
