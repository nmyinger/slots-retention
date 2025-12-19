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

        spin_result = slot.play_spin()
        spin_win = spin_result["total_win"]
        scatter_count = spin_result["scatter_count"]
        triggered_bonus = spin_result["bonus_triggered"]

        if spin_result["base_win"] > 0:
            hits += 1

        bonus_win = 0
        if triggered_bonus:
            bonus_triggers += 1
            bonus_win = spin_result["bonus_total_win"]
            bonus_spin_results = spin_result["bonus_spin_results"]

            print("\n✨✨✨ BONUS TRIGGERED! ✨✨✨", flush=True)
            print(
                f"➡️  Spin {total_spins}: {scatter_count} ⭐ SCATTERS! "
                f"Starting {slot.BONUS_INITIAL_SPINS} Free Spins\n",
                flush=True
            )
            input("Press Enter to start bonus spins...")

            for fs_count, bonus_spin in enumerate(bonus_spin_results, start=1):
                outcome_fs = bonus_spin["outcome"]
                wins_fs = bonus_spin["wins_detail"]
                retriggered = bonus_spin["retriggered"]

                print(f"  🎰 Bonus Spin {fs_count}", flush=True)
                print("  ┌───────────────────────────────┐")
                for row in range(3):
                    symbols_row = [(sym if sym != "-" else " ") for sym in outcome_fs[row]]
                    print("  │ " + " │ ".join(f"{s:^3}" for s in symbols_row) + " │", flush=True)
                print("  └───────────────────────────────┘", flush=True)

                if wins_fs:
                    for (line_num, sym, count, pay) in wins_fs:
                        line_pay = pay * slot.BONUS_MULTIPLIER
                        print(
                            f"     ✅ Line {line_num}: {count} × {sym} → "
                            f"{line_pay} credits ({slot.BONUS_MULTIPLIER}x)",
                            flush=True
                        )
                        if line_pay >= bet_per_spin * BIG_WIN_MULTIPLIER:
                            print("\n🌟🌟🌟 BIG BONUS WIN! 🌟🌟🌟", flush=True)
                            input("Press Enter to continue...")
                else:
                    print("     ❌ No line wins.", flush=True)

                if retriggered:
                    print(
                        f"     🔁 ⭐ Bonus Re-Triggered! +{slot.BONUS_RETRIGGER_SPINS} spins",
                        flush=True
                    )
                    input("Press Enter to continue...")

                time.sleep(SPIN_DELAY)

            bonus_total_win += bonus_win
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
