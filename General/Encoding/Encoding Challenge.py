from pwn import *
import json
import binascii
import base64
import codecs
import sys
conn=remote('socket.cryptohack.org', 13377, level='debug')
# line= r.recvline().decode()
# line_js=json.loads(line)
# print(line_js)
def dec(t,e):
    if t == "base64":
        return base64.b64decode(e).decode()
    if t == "hex":
        return binascii.unhexlify(e).decode()
    if t == "rot13":
        return codecs.decode(e, 'rot_13')
    if t == "bigint":
        return binascii.unhexlify(e.replace("0x","")).decode()
    if t == "utf-8":
        c = ""
        for i in e:
            c += chr(i)
        return c
def json_recv():
    line = conn.recvline().decode()
    return json.loads(line)
def json_send(r):
    result = json.dumps(r)
    conn.sendline(result.encode())
while True :

    received = json_recv()
    # print(type(received))
    if "flag" in received:
        print(received["flag"])
        sys.exit(0)
    t = received["type"]
    # print(t)
    e = received["encoded"]
    to_send = {
        "decoded": dec(t,e)
    }

    json_send(to_send)