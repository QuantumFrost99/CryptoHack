hex_string = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"
b = bytes.fromhex(hex_string).decode()
print(b)

# To convert a text to hexadecimal
a = "Hello World"
a_bytes = str.encode(a) # First we have to convert the text to bytes
print(a_bytes)
a_hex = a_bytes.hex() # Then we convert the bytes to hexadecimal
print(a_hex)

# Converting the hexadecimal back to text
c = bytes.fromhex(a_hex).decode() # decode converts the bytes to text
print(c)