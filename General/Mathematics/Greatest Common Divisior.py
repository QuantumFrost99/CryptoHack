def findgcd(a, b):
    if a == 0:
        return b
    return findgcd(b % a, a)

value = findgcd(66528, 52920)
print(value)

