value1 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
value2 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
value3 = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

key1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
key2 = "911404e13f94884eabbec925851240a52fa381ddb79700dd6d0d"
key3 = "504053b757eafd3d709d6339b140e03d98b9fe62b84add0332cc"

key4 = "f688e5c46b71dfe30b5d460bd7e366406de3338adb14c4c401df"
key5 = "679ce12554e557ada0e38f2e52f126e54240b2576c83c4196cd2"

pairs = [key5[i:i+2] for i in range(0,len(key5),2)]
pairs2 = [value3[i:i+2] for i in range(0,len(value3),2)]

flag_list = [format(int(pairs[i],16) ^ int(pairs2[i],16),"02x") for i in range(0,26)]
flag = "".join(flag_list)

flag_text = bytes.fromhex(flag).decode()
print(flag_text)