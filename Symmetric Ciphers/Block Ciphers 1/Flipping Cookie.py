from pwn import *
from binascii import unhexlify, hexlify

cookie = "90398e3a0e00f68b1827edf38918e14196065f449be3aeb86e4114af54f40cbdecd1fba5f2a799c56cd2bcc3aaab7204"
original_iv = cookie[0:32]
ct2 = cookie[32:96]
raw = unhexlify(original_iv)
original = b"admin=False;exp"
desired  = b"admin=True;exp"
new_iv = xor(raw, original, desired)
print(ct2)
print("iv =", hexlify(new_iv).decode())
