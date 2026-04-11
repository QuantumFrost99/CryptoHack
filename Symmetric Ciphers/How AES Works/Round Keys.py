from pwn import *
state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]

def add_round_key(s, k):
    return (xor(sum(s, []), sum(k, []))).decode()

# def add_round_key(s, k):
#     l1 = [byte for row in state for byte in row]
#     l2 = [byte for row in round_key for byte in row]
#     l3 = []
#     for i in range(0,len(l1)):
#         value = l1[i] ^ l2[i]
#         l3.append(value)
#     for i in l3:
#         print(chr(i),end="")

print(add_round_key(state, round_key))
