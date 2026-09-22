data = [3, 8, 1, 6, 9]

result = []

for x in data:

    if x % 2 == 0:

        result.append(x)

print(*result)