# crypto{M1x1n6_r0und5_4r3_1nv3r71bl3!}

from binascii import unhexlify
msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'
iv1_hex = 'e42758d6d218013ea63e3c49'
iv2_hex = 'a99f9a7d097daabd2aa2a235'
msg_enc_hex = 'f3afbada8237af6e94c7d2065ee0e221a1748b8c7b11105a8cc8a1c74253611c94fe7ea6fa8a9133505772ef619f04b05d2e2b0732cc483df72ccebb09a92c211ef5a52628094f09a30fc692cb25647f'
flag_enc_hex = 'b6327e9a2253034096344ad5694a2040b114753e24ea9c1af17c10263281fb0fe622b32732'
iv1 = unhexlify(iv1_hex)
iv2 = unhexlify(iv2_hex)
msg_enc = unhexlify(msg_enc_hex)
flag_enc = unhexlify(flag_enc_hex)

def bytes_to_words(b):
    return [int.from_bytes(b[i:i+4], 'little') for i in range(0, len(b), 4)]

def rotate(x, n):
    return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)

def word(x):
    return x % (2 ** 32)

def words_to_bytes(w):
    return b''.join([i.to_bytes(4, 'little') for i in w])

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

class ChaCha20:
    def __init__(self):
        self._state = []
    def _inner_block(self, state):
        self._quarter_round(state, 0, 4, 8, 12)
        self._quarter_round(state, 1, 5, 9, 13)
        self._quarter_round(state, 2, 6, 10, 14)
        self._quarter_round(state, 3, 7, 11, 15)
        self._quarter_round(state, 0, 5, 10, 15)
        self._quarter_round(state, 1, 6, 11, 12)
        self._quarter_round(state, 2, 7, 8, 13)
        self._quarter_round(state, 3, 4, 9, 14)
    def _quarter_round(self, x, a, b, c, d):
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 16)
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 12)
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 8)
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 7)
    
    def _setup_state(self, key, iv):
        self._state = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
        self._state.extend(bytes_to_words(key))
        self._state.append(self._counter)
        self._state.extend(bytes_to_words(iv))
    def decrypt(self, c, key, iv):
        return self.encrypt(c, key, iv)
    def encrypt(self, m, key, iv):
        c = b''
        self._counter = 1
        for i in range(0, len(m), 64):
            self._setup_state(key, iv)
            for _ in range(10):
                self._inner_block(self._state)
            c += xor(m[i:i+64], words_to_bytes(self._state))
            self._counter += 1
        return c
    
def rotr(x, n):
    return ((x >> n) | ((x << (32 - n)) & 0xffffffff)) & 0xffffffff

def inv_quarter_round(x, a, b, c, d):
    a2, b2, c2, d2 = x[a], x[b], x[c], x[d]
    b1 = rotr(b2, 7) ^ c2
    c1 = (c2 - d2) & 0xffffffff
    a1 = (a2 - b1) & 0xffffffff
    d1 = rotr(d2, 8) ^ a2
    b0 = rotr(b1, 12) ^ c1
    c0 = (c1 - d1) & 0xffffffff
    a0 = (a1 - b0) & 0xffffffff
    d0 = rotr(d1, 16) ^ a1
    x[a], x[b], x[c], x[d] = a0, b0, c0, d0

def inv_inner_block(state):
    inv_quarter_round(state, 3, 4, 9, 14)
    inv_quarter_round(state, 2, 7, 8, 13)
    inv_quarter_round(state, 1, 6, 11, 12)
    inv_quarter_round(state, 0, 5, 10, 15)
    inv_quarter_round(state, 3, 7, 11, 15)
    inv_quarter_round(state, 2, 6, 10, 14)
    inv_quarter_round(state, 1, 5, 9, 13)
    inv_quarter_round(state, 0, 4, 8, 12)

def recover_key(msg, msg_enc):
    ks = xor(msg_enc[:64], msg[:64])
    state = bytes_to_words(ks)
    for _ in range(10):
        inv_inner_block(state)
    return words_to_bytes(state[4:12])

def main():
    key = recover_key(msg, msg_enc)
    print("Recovered key:", key.hex())
    cipher = ChaCha20()
    flag = cipher.decrypt(flag_enc, key, iv2)
    print("Flag:", flag.decode())

if __name__ == "__main__":
    main()