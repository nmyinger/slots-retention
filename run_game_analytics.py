import slot_game_logic as slot
import time

# Set a number of spins to simulate
total_spins = 1000000

# Stats trackers
balance = 100000000
bet_per_spin = 10  # Fixed at 10 credits per spin (10 lines x 1 credit)
total_bet = 0
total_win = 0
hits = 0
bonus_triggers = 0
bonus_wins = 0

start_time = time.time()

for spin in range(1, total_spins + 1):
    balance -= bet_per_spin
    total_bet += bet_per_spin

    spin_result = slot.play_spin()
    spin_win = spin_result["total_win"]

    if spin_result["base_win"] > 0:
        hits += 1
    
    if spin_result["bonus_triggered"]:
        bonus_triggers += 1
        bonus_wins += spin_result["bonus_total_win"]

    total_win += spin_win
    balance += spin_win

end_time = time.time()

effective_rtp = (total_win / total_bet) * 100
hit_frequency = (hits / total_spins) * 100
bonus_freq = (bonus_triggers / total_spins) * 100

print("--- Slot Game Simulation Analysis ---")
print(f"Total Spins: {total_spins}")
print(f"Total Bet: {total_bet} credits")
print(f"Total Win: {total_win} credits")
print(f"Final Balance: {balance} credits")
print(f"Effective RTP: {effective_rtp:.2f}%")
print(f"Hit Frequency: {hit_frequency:.2f}%")
print(f"Bonus Trigger Rate: {bonus_freq:.2f}%")
print(f"Average Bonus Win: {bonus_wins / bonus_triggers if bonus_triggers > 0 else 0:.2f} credits")
print(f"Simulation Time: {end_time - start_time:.2f} seconds")
