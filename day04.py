data = open('data/day04.txt').read().splitlines()


count1 = 0
count2 = 0
for d in data:
    first, second = d.split(',')
    firstRange = [int(x) for x in first.split('-')]
    secondRange = [int(x) for x in second.split('-')]
    if ((firstRange[0] <= secondRange[0] and secondRange[1] <= firstRange[1]) or
        (secondRange[0] <= firstRange[0] and firstRange[1] <= secondRange[1])):
        count1 += 1
    if ((secondRange[0] <= firstRange[0] <= secondRange[1]) or
        (firstRange[0] <= secondRange[0] <= firstRange[1])):
        count2 += 1

print(f"Solution 1: {count1}")
print(f"Solution 2: {count2}")