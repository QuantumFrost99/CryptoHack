# #!/usr/bin/env python3

# from Crypto.Util.Padding import unpad
# from Crypto.Cipher import AES
# from os import urandom
# from random import SystemRandom

# # from utils import listener

# FLAG = 'crypto{??????????????????????????????????????????}'
# rng = SystemRandom()


# class Challenge:
#     def __init__(self):
#         self.before_input = "That last challenge was pretty easy, but I'm positive that this one will be harder!\n"
#         self.message = urandom(16).hex()
#         self.key = urandom(16)
#         self.query_count = 0
#         self.max_queries = 12_000

#     def update_query_count(self):
#         self.query_count += 1
#         if self.query_count >= self.max_queries:
#             self.exit = True

#     def get_ct(self):
#         iv = urandom(16)
#         cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
#         ct = cipher.encrypt(self.message.encode("ascii"))
#         return {"ct": (iv+ct).hex()}

#     def check_padding(self, ct):
#         ct = bytes.fromhex(ct)
#         iv, ct = ct[:16], ct[16:]
#         cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
#         pt = cipher.decrypt(ct)  # does not remove padding
#         try:
#             unpad(pt, 16)
#         except ValueError:
#             good = False
#         else:
#             good = True
#         self.update_query_count()
#         return {"result": good | (rng.random() > 0.4)}

#     def check_message(self, message):
#         if message != self.message:
#             self.exit = True
#             return {"error": "incorrect message"}
#         return {"flag": FLAG}

#     #
#     # This challenge function is called on your input, which must be JSON
#     # encoded
#     #
#     def challenge(self, msg):
#         if "option" not in msg or msg["option"] not in ("encrypt", "unpad", "check"):
#             return {"error": "Option must be one of: encrypt, unpad, check"}

#         if msg["option"] == "encrypt": return self.get_ct()
#         elif msg["option"] == "unpad": return self.check_padding(msg["ct"])
#         elif msg["option"] == "check": return self.check_message(msg["message"])


# # import builtins; builtins.Challenge = Challenge # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
# # listener.start_server(port=13422)

import socket
import json

HOST = "socket.cryptohack.org"
PORT = 13422

BLOCK_SIZE = 16


# ----------------------------
# Safe socket communication
# ----------------------------
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


# ----------------------------
# Noisy oracle (fail-fast)
# ----------------------------
def oracle(s, ct):
    res = send_recv(s, {
        "option": "unpad",
        "ct": ct.hex()
    })
    return res["result"]


# ----------------------------
# scoring wrapper (KEY FIX)
# ----------------------------
def score_guess(s, ct, tries=3):
    score = 0
    for _ in range(tries):
        if oracle(s, ct):
            score += 1
    return score


# ----------------------------
# encrypt
# ----------------------------
def encrypt(s):
    ct = send_recv(s, {"option": "encrypt"})
    return bytes.fromhex(ct["ct"])


# ----------------------------
# split blocks
# ----------------------------
def split_blocks(data):
    return [data[i:i+BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]


# ----------------------------
# padding oracle attack (FIXED)
# ----------------------------
def recover_blocks(s, prev_block, curr_block):
    intermediate = [0] * BLOCK_SIZE
    plaintext = [0] * BLOCK_SIZE

    crafted = bytearray(BLOCK_SIZE)

    for i in range(15, -1, -1):
        pad = BLOCK_SIZE - i

        # enforce known padding
        for j in range(i + 1, BLOCK_SIZE):
            crafted[j] = intermediate[j] ^ pad

        best_guess = None
        best_score = -1

        for guess in range(256):
            crafted[i] = guess
            test_ct = bytes(crafted) + curr_block

            # ----------------------------
            # KEY FIX: score-based selection
            # ----------------------------
            score = score_guess(s, test_ct, tries=3)

            if score > best_score:
                best_score = score
                best_guess = guess

        # finalize best guess
        intermediate[i] = best_guess ^ pad
        plaintext[i] = intermediate[i] ^ prev_block[i]

    return bytes(plaintext)


# ----------------------------
# main
# ----------------------------
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