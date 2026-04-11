from pwn import xor

iv  = bytes.fromhex("52e370621ab612e366422ae066b48c8f")
b1  = bytes.fromhex("40f7f0b2d970fd4e3f3ab2596f326410")
b2  = bytes.fromhex("94070e81d78332252e95e714be5fb754")

b1d = bytes.fromhex("319109126ed969d0052075d513d7e7ba")
b2d = bytes.fromhex("1fc38682e814a27f086593784e13456d")

p1 = xor(b1d, iv)
p2 = xor(b2d, b1)

plaintext = p1 + p2
print(plaintext.decode())
