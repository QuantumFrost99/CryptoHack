i = 0
ans_found = False

while not ans_found:
    i = i + 1
    result = (int(i) * 3) % 13
    if result == 1:
        print(f"Multiplication Inverse = {i}")
        ans_found = True
    else:
        pass