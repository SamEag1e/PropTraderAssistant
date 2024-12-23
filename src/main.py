from read import get_html_trades
from rules import (
    eighty_percent_rule_check,
    group_overlapping_trades,
    fast_scalp_profit_rule,
)


# ---------------------------------------------------------------------
def main():
    # Input: Assume we are using an HTML file for now
    file_path = "trade_history.html"

    trades = get_html_trades(file_path)

    overlapping_profit_trades = group_overlapping_trades(trades)

    print("\nAll Trades")
    for trade in trades:
        print(trade)
    print("\nOverlapping Profit Trades")
    for trade in overlapping_profit_trades:
        print(trade)
    gross_profit = sum(trade.profit for trade in overlapping_profit_trades)
    print(f"\nGross Profit: {gross_profit:.2f}")
    print(eighty_percent_rule_check(overlapping_profit_trades))
    print(fast_scalp_profit_rule(trades))


# ---------------------------------------------------------------------
if __name__ == "__main__":
    main()
