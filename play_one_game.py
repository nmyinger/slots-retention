import slot_game_logic as slot
import os
import time

SAVE_FILE = "balance_save.txt"

SPIN_HEADER = "=" * 50


def load_balance():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 1000
    return 1000

def save_balance(balance):
    with open(SAVE_FILE, "w") as f:
        f.write(str(balance))

# Run one manual game spin
balance = load_balance()
bet_per_spin = 10  # Fixed bet: 10 lines x 1 credit
print("\n🎰 WELCOME TO RETENTION SLOT - ONE SPIN MODE 🎰")
print(SPIN_HEADER)
print(f"Initial Balance: {balance} credits")
print(f"Bet per Spin: {bet_per_spin} credits")
print(SPIN_HEADER)

if balance < bet_per_spin:
    print("⚠️  Insufficient balance to play. Please reset or top up.")
else:
    balance -= bet_per_spin
    spin_result = slot.play_spin()
    outcome = spin_result["outcome"]
    scatter_count = spin_result["scatter_count"]
    wins_detail = spin_result["wins_detail"]
    spin_win = spin_result["total_win"]

    print("\n🎞️  Reels:")
    print(SPIN_HEADER)
    for row in range(3):
        symbols_row = [(sym if sym != "-" else " ") for sym in outcome[row]]
        print(" | ".join(f"{s:^5}" for s in symbols_row))
    print(SPIN_HEADER)

    # Line wins
    if wins_detail:
        print("🏆 Line Wins:")
        for (line_num, sym, count, pay) in wins_detail:
            print(f"  >> Line {line_num}: {count} × {sym} pays {pay} credits")
    else:
        print("🙁 No line wins this spin.")

    # Bonus trigger
    if spin_result["bonus_triggered"]:
        bonus_total_win = spin_result["bonus_total_win"]
        bonus_spin_results = spin_result["bonus_spin_results"]
        print(
            f"\n✨ {scatter_count} ⭐ SCATTERS! BONUS TRIGGERED: "
            f"{slot.BONUS_INITIAL_SPINS} FREE SPINS! ✨"
        )

        for fs_count, bonus_spin in enumerate(bonus_spin_results, start=1):
            print(f"\n🎲 Bonus Spin {fs_count}:")
            outcome_fs = bonus_spin["outcome"]
            wins_fs = bonus_spin["wins_detail"]
            retriggered = bonus_spin["retriggered"]

            for row in range(3):
                row_data = [(sym if sym != "-" else " ") for sym in outcome_fs[row]]
                print(" | ".join(f"{s:^5}" for s in row_data))

            if wins_fs:
                for (line_num, sym, count, pay) in wins_fs:
                    line_pay = pay * slot.BONUS_MULTIPLIER
                    print(
                        f"  >> Line {line_num}: {count} × {sym} pays {line_pay} "
                        f"credits ({slot.BONUS_MULTIPLIER}x)"
                    )
            else:
                print("  No line wins.")

            if retriggered:
                print(f"  ⭐ Bonus Re-Triggered! +{slot.BONUS_RETRIGGER_SPINS} more spins!")

        print(f"\n🎉 BONUS COMPLETE: Total Bonus Winnings = {bonus_total_win} credits")

    elif scatter_count == 2:
        print("⚡ Two scatters appeared... one short of the bonus!")

    balance += spin_win
    print(SPIN_HEADER)
    print(f"💰 Total Win This Spin: {spin_win} credits")
    print(f"🏦 Final Balance: {balance} credits")
    print(SPIN_HEADER)

    save_balance(balance)
    time.sleep(0.5)
