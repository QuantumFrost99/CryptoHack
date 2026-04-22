import base64

hex_string = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
byte_string = bytes.fromhex(hex_string)
b64_string = base64.b64encode(byte_string)
print(b64_string)