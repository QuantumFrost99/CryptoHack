result = []
s = "label"
key = 13
for c in s:
    code = ord(c) # convert character to integer(acsii)
    xored = code ^ key # XOR with the key
    result.append(chr(xored))
result_string = "".join(result)
print(result_string)


