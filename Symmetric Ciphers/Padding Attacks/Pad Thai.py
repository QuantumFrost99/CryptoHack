# crypto{if_you_ask_enough_times_you_usually_get_what_you_want}

# #!/usr/bin/env python3

# from Crypto.Util.Padding import unpad
# from Crypto.Cipher import AES
# from os import urandom

# # from utils import listener

# FLAG = 'crypto{?????????????????????????????????????????????????????}'

# class Challenge:
#     def __init__(self):
#         self.before_input = "Let's practice padding oracle attacks! Recover my message and I'll send you a flag.\n"
#         self.message = urandom(16).hex()
#         self.key = urandom(16)

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
#         return {"result": good}

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


# # import builtins; builtins.Challenge = Challenge  #hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
# # listener.start_server(port=13421)

import socket
import json

HOST = "socket.cryptohack.org"
PORT = 13421

BLOCK_SIZE = 16


# --- socket helpers ---
def send_recv(s, data):
    s.send((json.dumps(data) + "\n").encode())
    return json.loads(s.recv(4096).decode())


# --- oracle ---
def oracle(s, ct):
    res = send_recv(s, {"option": "unpad", "ct": ct.hex()})
    return res["result"]


# --- get ciphertext ---
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

        # Fix already solved bytes
        for j in range(i+1, BLOCK_SIZE):
            crafted[j] = intermediate[j] ^ pad

        # brute force
        for guess in range(256):
            crafted[i] = guess

            test_ct = bytes(crafted) + curr_block

            if oracle(s, test_ct):
                # avoid false positive for last byte
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

    # read banner
    print(s.recv(4096).decode())

    ct = get_ct(s)
    blocks = split_blocks(ct)

    recovered = b""

    for i in range(1, len(blocks)):
        print(f"[+] Decrypting block {i}")
        pt = recover_block(s, blocks[i-1], blocks[i])
        recovered += pt

    print("[+] Plaintext:", recovered)

    # send to check
    res = send_recv(s, {
        "option": "check",
        "message": recovered.decode()
    })

    print(res)


if __name__ == "__main__":
    main()