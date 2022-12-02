data = open('data/day02.txt').read().splitlines()

# Rock: A & X
# Paper: B & Y
# Scissors: C & Z
shape_score = {'X': 1, 'Y': 2, 'Z': 3}


def outcome_score(opp, you):
    if (opp == 'A' and you == 'X') or (opp == 'B' and you == 'Y') or (opp == 'C' and you == 'Z'):
        return 3
    if (opp == 'A' and you == 'Z') or (opp == 'B' and you == 'X') or (opp == 'C' and you == 'Y'):
        return 0
    return 6


def game_score(opp, you):
    return outcome_score(opp, you) + shape_score[you]


def strategy_choice(opp, outcome):
    if (outcome == 'X' and opp == 'A') or (outcome == 'Y' and opp == 'C') or (outcome == 'Z' and opp == 'B'):
        return 'Z'
    if (outcome == 'X' and opp == 'B') or (outcome == 'Y' and opp == 'A') or (outcome == 'Z' and opp == 'C'):
        return 'X'
    return 'Y'


total1 = 0
total2 = 0
for d in data:
    opp, you = d.split()
    total1 += game_score(opp, you)
    you = strategy_choice(opp, you)
    total2 += game_score(opp, you)

print(f"Solution 1: {total1}")
print(f"Solution 2: {total2}")