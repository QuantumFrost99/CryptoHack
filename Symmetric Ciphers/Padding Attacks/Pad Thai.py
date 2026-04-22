import socket
import json

HOST = "socket.cryptohack.org"
PORT = 13421
BLOCK_SIZE = 16
def send_recv(s, data):
    s.send((json.dumps(data) + "\n").encode())
    return json.loads(s.recv(4096).decode())

def oracle(s, ct):
    res = send_recv(s, {"option": "unpad", "ct": ct.hex()})
    return res["result"]

def get_ct(s):
    res = send_recv(s, {"option": "encrypt"})
    return bytes.fromhex(res["ct"])

def split_blocks(data):
    return [data[i:i+BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]

def recover_block(s, prev_block, curr_block):
    intermediate = [0] * BLOCK_SIZE
    plaintext = [0] * BLOCK_SIZE
    crafted = bytearray(BLOCK_SIZE)
    for i in range(15, -1, -1):
        pad = BLOCK_SIZE - i
        for j in range(i+1, BLOCK_SIZE):
            crafted[j] = intermediate[j] ^ pad
        for guess in range(256):
            crafted[i] = guess
            test_ct = bytes(crafted) + curr_block
            if oracle(s, test_ct):
                if i == 15:
                    crafted2 = crafted.copy()
                    crafted2[i-1] ^= 1
                    if not oracle(s, bytes(crafted2) + curr_block):
                        continue
                intermediate[i] = guess ^ pad
                plaintext[i] = intermediate[i] ^ prev_block[i]
                break
    return bytes(plaintext)

def main():
    s = socket.socket()
    s.connect((HOST, PORT))
    print(s.recv(4096).decode())
    ct = get_ct(s)
    blocks = split_blocks(ct)
    recovered = b""
    for i in range(1, len(blocks)):
        print(f"[+] Decrypting block {i}")
        pt = recover_block(s, blocks[i-1], blocks[i])
        recovered += pt
    print("[+] Plaintext:", recovered)
    res = send_recv(s, {
        "option": "check",
        "message": recovered.decode()
    })
    print(res)

if __name__ == "__main__":
    main()