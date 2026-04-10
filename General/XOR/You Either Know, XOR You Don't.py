from pwn import xor

value = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
key = "myXORkey"

data = bytes.fromhex(value)
nkey = key.encode("utf-8")

xored = bytes(
    data[i] ^ nkey[i % len(nkey)]
    for i in range(len(data))
)

print(xored.decode())

# # Key Extraction
# flag = "crypto{"
# nflag = flag.encode("utf-8")

# fkey = xor(data[6],nflag[6])
# print(fkey)