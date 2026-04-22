import socket
import json

HOST = "socket.cryptohack.org"
PORT = 13422
BLOCK_SIZE = 16
def send_recv(s, data):
    s.sendall((json.dumps(data) + "\n").encode())
    buf = b""
    while b"\n" not in buf:
        chunk = s.recv(4096)
        if not chunk:
            raise ConnectionError("Server closed connection")
        buf += chunk
    line = buf.split(b"\n")[0]
    return json.loads(line.decode("utf-8", errors="ignore"))

def oracle(s, ct):
    res = send_recv(s, {
        "option": "unpad",
        "ct": ct.hex()
    })
    return res["result"]

def score_guess(s, ct, tries=3):
    score = 0
    for _ in range(tries):
        if oracle(s, ct):
            score += 1
    return score

def encrypt(s):
    ct = send_recv(s, {"option": "encrypt"})
    return bytes.fromhex(ct["ct"])

def split_blocks(data):
    return [data[i:i+BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]

def recover_blocks(s, prev_block, curr_block):
    intermediate = [0] * BLOCK_SIZE
    plaintext = [0] * BLOCK_SIZE
    crafted = bytearray(BLOCK_SIZE)
    for i in range(15, -1, -1):
        pad = BLOCK_SIZE - i
        for j in range(i + 1, BLOCK_SIZE):
            crafted[j] = intermediate[j] ^ pad
        best_guess = None
        best_score = -1
        for guess in range(256):
            crafted[i] = guess
            test_ct = bytes(crafted) + curr_block
            score = score_guess(s, test_ct, tries=3)
            if score > best_score:
                best_score = score
                best_guess = guess
        intermediate[i] = best_guess ^ pad
        plaintext[i] = intermediate[i] ^ prev_block[i]
    return bytes(plaintext)

def main():
    s = socket.socket()
    s.connect((HOST, PORT))
    print(s.recv(4096).decode())
    ct = encrypt(s)
    blocks = split_blocks(ct)
    recovered = b""
    for i in range(1, len(blocks)):
        print(f"[+] Decrypting block {i}")
        pt = recover_blocks(s, blocks[i - 1], blocks[i])
        recovered += pt
    print("[+] Raw output:", recovered)
    res = send_recv(s, {
        "option": "check",
        "message": recovered.decode(errors="ignore")
    })
    print(res)

if __name__ == "__main__":
    main()