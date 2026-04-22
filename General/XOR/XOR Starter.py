result = []
s = "label"
key = 13
for c in s:
    code = ord(c) 
    xored = code ^ key 
    result.append(chr(xored))
result_string = "".join(result)
print(result_string)