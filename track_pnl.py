import pandas as pd
from pathlib import Path

def load_trades(log_path):
    if not log_path.exists():
        return pd.DataFrame()
    df = pd.read_csv(log_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df['action'] = df['action'].str.upper()
    return df

def calculate_pnl(df):
    pnl_data = []
    positions = {}

    for _, row in df.iterrows():
        sym = row['symbol']
        action = row['action']
        size = row['shares'] if 'shares' in row else row['size']
        price = row['price'] if 'price' in row else row['entry']

        if sym not in positions:
            positions[sym] = []

        if action == 'BUY':
            positions[sym].append({'size': size, 'price': price})
        elif action == 'SELL' and positions[sym]:
            buy = positions[sym].pop(0)
            pnl = (price - buy['price']) * size
            pnl_data.append({'symbol': sym, 'pnl': pnl})

    return pd.DataFrame(pnl_data)

def print_summary(bot_name, pnl_df):
    if pnl_df.empty:
        print(f"\n{bot_name}: No trades found.")
        return
    total_pnl = pnl_df['pnl'].sum()
    print(f"\n{bot_name} Summary:")
    print(pnl_df.groupby('symbol')['pnl'].sum())
    print(f"Total PnL: {total_pnl:.2f}")

# === File paths
turtle_log = Path("../Turtle-Trading-Bot/trade_log.csv")
forex_log = Path("../forex-trading-bot/trade_log.csv")

# === Load and process
turtle_df = load_trades(turtle_log)
forex_df = load_trades(forex_log)

turtle_pnl = calculate_pnl(turtle_df)
forex_pnl = calculate_pnl(forex_df)

# === Print output
print_summary("Turtle Bot", turtle_pnl)
print_summary("Forex Bot", forex_pnl)
