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
    outcome, scatter_count = slot.spin_reels()
    spin_win, wins_detail = slot.evaluate_lines(outcome)

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
    if scatter_count >= 3:
        print(f"\n✨ {scatter_count} ⭐ SCATTERS! BONUS TRIGGERED: 10 FREE SPINS! ✨")
        bonus_spins = 10
        bonus_total_win = 0
        fs_count = 0

        while bonus_spins > 0:
            bonus_spins -= 1
            fs_count += 1
            print(f"\n🎲 Bonus Spin {fs_count}:")
            outcome_fs, scat_fs = slot.spin_reels()
            base_win_fs, wins_fs = slot.evaluate_lines(outcome_fs)
            win_fs = base_win_fs * 2
            bonus_total_win += win_fs

            for row in range(3):
                row_data = [(sym if sym != "-" else " ") for sym in outcome_fs[row]]
                print(" | ".join(f"{s:^5}" for s in row_data))

            if wins_fs:
                for (line_num, sym, count, pay) in wins_fs:
                    print(f"  >> Line {line_num}: {count} × {sym} pays {pay * 2} credits (2x)")
            else:
                print("  No line wins.")

            if scat_fs >= 3:
                bonus_spins += 10
                print("  ⭐ Bonus Re-Triggered! +10 more spins!")

        print(f"\n🎉 BONUS COMPLETE: Total Bonus Winnings = {bonus_total_win} credits")
        spin_win += bonus_total_win

    elif scatter_count == 2:
        print("⚡ Two scatters appeared... one short of the bonus!")

    balance += spin_win
    print(SPIN_HEADER)
    print(f"💰 Total Win This Spin: {spin_win} credits")
    print(f"🏦 Final Balance: {balance} credits")
    print(SPIN_HEADER)

    save_balance(balance)
    time.sleep(0.5)