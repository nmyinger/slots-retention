# 🎰 Slot Machine with Retention-Focused Game Design

A 5-reel command-line slot machine designed to experiment with high-retention mechanics like bonus rounds, hit rates, and big win pacing.

## Features
- Bonus rounds with retriggers
- Big win detection and celebration
- Persistent balance between runs
- Simulated session metrics (RTP, hit rate, etc.)

## Usage
Clone repository: 
```bash
git clone https://github.com/nmyinger/slots-retention.git
cd slots-retention
```

Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Run the game:
```bash
python play_continuous_game.py
