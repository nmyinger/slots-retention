import random

symbols = ["J", "Q", "K", "A", "7", "BAR", "W", "⭐", "-"]

scatter_stops = [2, 2, 2, 2, 1]
base_counts = {
    "J": 10,
    "Q": 10,
    "K": 7,
    "A": 7,
    "7": 5,
    "BAR": 4,
    "W": 3
}

reels = []
for i in range(5):
    counts = base_counts.copy()
    counts["⭐"] = scatter_stops[i]
    total_symbols = sum(counts.values())
    counts["-"] = 50 - total_symbols if total_symbols < 50 else 0
    strip = [sym for sym, cnt in counts.items() for _ in range(cnt)]
    random.shuffle(strip)
    reels.append(strip)

paylines = [
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2],
    [0, 1, 2, 1, 0],
    [2, 1, 0, 1, 2],
    [0, 0, 1, 2, 2],
    [2, 2, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [2, 1, 1, 1, 2],
    [1, 0, 0, 0, 1]
]

paytable = {
    "J": {3: 5, 4: 10, 5: 20},
    "Q": {3: 5, 4: 10, 5: 20},
    "K": {3: 10, 4: 25, 5: 50},
    "A": {3: 10, 4: 25, 5: 50},
    "7": {3: 15, 4: 50, 5: 100},
    "BAR": {3: 20, 4: 100, 5: 200},
    "W": {3: 50, 4: 200, 5: 500}
}

def spin_reels():
    outcome = [[None]*5 for _ in range(3)]
    scatter_count = 0
    for reel_index, strip in enumerate(reels):
        start = random.randrange(len(strip))
        for row in range(3):
            sym = strip[(start + row) % len(strip)]
            outcome[row][reel_index] = sym
            if sym == "⭐":
                scatter_count += 1
    return outcome, scatter_count

def evaluate_lines(outcome):
    total_win = 0
    wins_detail = []
    for li, pattern in enumerate(paylines, start=1):
        line_symbols = [outcome[row][ri] for ri, row in enumerate(pattern)]
        first_sym = line_symbols[0]
        if first_sym in ("-", "⭐"):
            continue
        base_symbol, count = None, 0
        best_pay, best_symbol = 0, None

        if first_sym == "W":
            wild_count = 1
            for s in line_symbols[1:]:
                if s == "W":
                    wild_count += 1
                else:
                    break
            if wild_count >= 3 and wild_count in paytable["W"]:
                best_pay = paytable["W"][wild_count]
                best_symbol = "W"

        for sym in line_symbols:
            if sym in ("-", "⭐"):
                break
            if sym == "W" and base_symbol is None:
                continue
            if base_symbol is None:
                base_symbol, count = sym, 1
            elif sym == base_symbol or sym == "W":
                count += 1
            else:
                break

        if base_symbol:
            leading_wilds = 0
            for sym in line_symbols:
                if sym == "W":
                    leading_wilds += 1
                elif sym in ("-", "⭐"):
                    leading_wilds = 0
                    break
                else:
                    break
            count += leading_wilds
            if count >= 3 and count in paytable.get(base_symbol, {}):
                pay = paytable[base_symbol][count]
                if pay > best_pay:
                    best_pay = pay
                    best_symbol = base_symbol

        if best_pay > 0:
            total_win += best_pay
            wins_detail.append((li, best_symbol, count, best_pay))
    return total_win, wins_detail