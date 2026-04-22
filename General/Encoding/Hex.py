hex_string = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"
b = bytes.fromhex(hex_string).decode()
a = "Hello World"
a_bytes = str.encode(a) 
a_hex = a_bytes.hex() 
c = bytes.fromhex(a_hex).decode() 
print(c)