import slot_game_logic as slot
import os
import time

SAVE_FILE = "balance_save.txt"
SPIN_DELAY = 0.2
BIG_WIN_MULTIPLIER = 10


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

# Initialize session
balance = load_balance()
bet_per_spin = 10

total_spins = 0
total_bet = 0
total_win = 0
hits = 0
bonus_triggers = 0
bonus_total_win = 0

print("\n================ SLOT MACHINE SESSION START ================")
print(f"Starting Balance: {balance} credits")
print("Press Ctrl+C to stop at any time.")
print("===========================================================\n")

try:
    while True:
        start = time.time()

        if balance < bet_per_spin:
            print("\n[!] Balance too low to continue.", flush=True)
            break

        balance -= bet_per_spin
        total_bet += bet_per_spin
        total_spins += 1

        outcome, scatter_count = slot.spin_reels()
        spin_win, wins_detail = slot.evaluate_lines(outcome)

        if spin_win > 0:
            hits += 1

        bonus_win = 0
        triggered_bonus = False
        if scatter_count >= 3:
            bonus_triggers += 1
            triggered_bonus = True
            bonus_spins = 10
            fs_count = 0

            print("\n✨✨✨ BONUS TRIGGERED! ✨✨✨", flush=True)
            print(f"➡️  Spin {total_spins}: {scatter_count} ⭐ SCATTERS! Starting 10 Free Spins\n", flush=True)
            input("Press Enter to start bonus spins...")

            while bonus_spins > 0:
                bonus_spins -= 1
                fs_count += 1
                outcome_fs, scat_fs = slot.spin_reels()
                base_win_fs, wins_fs = slot.evaluate_lines(outcome_fs)
                win_fs = base_win_fs * 2
                bonus_win += win_fs

                print(f"  🎰 Bonus Spin {fs_count}", flush=True)
                print("  ┌───────────────────────────────┐")
                for row in range(3):
                    symbols_row = [(sym if sym != "-" else " ") for sym in outcome_fs[row]]
                    print("  │ " + " │ ".join(f"{s:^3}" for s in symbols_row) + " │", flush=True)
                print("  └───────────────────────────────┘", flush=True)

                if wins_fs:
                    for (line_num, sym, count, pay) in wins_fs:
                        print(f"     ✅ Line {line_num}: {count} × {sym} → {pay * 2} credits (2x)", flush=True)
                        if pay * 2 >= bet_per_spin * BIG_WIN_MULTIPLIER:
                            print("\n🌟🌟🌟 BIG BONUS WIN! 🌟🌟🌟", flush=True)
                            input("Press Enter to continue...")
                else:
                    print("     ❌ No line wins.", flush=True)

                if scat_fs >= 3:
                    bonus_spins += 10
                    print("     🔁 ⭐ Bonus Re-Triggered! +10 spins", flush=True)
                    input("Press Enter to continue...")

                time.sleep(SPIN_DELAY)

            bonus_total_win += bonus_win
            spin_win += bonus_win
            print(f"\n🎉 Bonus Complete! Total Bonus Win: {bonus_win} credits\n", flush=True)
            input("Press Enter to resume normal spins...\n")

        elif scatter_count == 2:
            print(f"⚠️  ALMOST! 2 scatter symbols landed on Spin {total_spins}. Need 3 to get free spins.", flush=True)
            input("Press Enter to continue...\n")

        total_win += spin_win
        balance += spin_win

        rtp = (total_win / total_bet) * 100 if total_bet else 0
        hit_rate = (hits / total_spins) * 100
        bonus_rate = (bonus_triggers / total_spins) * 100

        if not triggered_bonus and spin_win >= bet_per_spin * BIG_WIN_MULTIPLIER:
            print("\n💰💰💰 BIG WIN! 💰💰💰", flush=True)
            print(f"🎯 Spin {total_spins:>4} | Win: {spin_win:>4} | Balance: {balance:>5}", flush=True)
            print(f"📊 RTP: {rtp:.2f}% | Hit Rate: {hit_rate:.2f}% | Bonus Rate: {bonus_rate:.2f}%\n", flush=True)
            input("Press Enter to continue...\n")
        else:
            print(f"🎯 Spin {total_spins:>4} | Win: {spin_win:>4} | Balance: {balance:>5}", flush=True)
            print(f"📊 RTP: {rtp:.2f}% | Hit Rate: {hit_rate:.2f}% | Bonus Rate: {bonus_rate:.2f}%\n", flush=True)

        elapsed = time.time() - start
        delay = max(0, SPIN_DELAY - elapsed)
        time.sleep(delay)

except KeyboardInterrupt:
    print("\n\n🛑 Session manually stopped.", flush=True)

save_balance(balance)
print(f"💾 Final Balance Saved: {balance} credits")
print("================= SESSION END =================")