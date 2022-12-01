def calculate_totals(data):
    totals = []
    total = 0
    for d in data:
        d = d.strip()
        if len(d) == 0:
            totals.append(total)
            total = 0
            continue
        total += int(d)
    return totals


data = open("data/day01.txt").read().splitlines()

totals = calculate_totals(data)

print(f"Solution 1: {max(totals)}")

totals.sort()
print(f"Solution 1: {sum(totals[:3])}")