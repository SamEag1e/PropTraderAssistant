from read import get_html_trades
from rules import eighty_percent_rule_check, group_overlapping_trades


# ---------------------------------------------------------------------
def main():
    # Input: Assume we are using an HTML file for now
    file_path = "trade_history.html"

    trades = get_html_trades(file_path)

    profit_trades = [t for t in trades if t.profit > 0]
    overlapping_profit_trades = group_overlapping_trades(profit_trades)
    result = eighty_percent_rule_check(overlapping_profit_trades)

    print("\n\nProfit Trades")
    for trade in trades:
        print(trade)
    print("\n\nOverlapping Profit Trades")
    for trade in overlapping_profit_trades:
        print(trade)
    gross_profit = sum(trade.profit for trade in overlapping_profit_trades)
    print(f"\nGross Profit: {gross_profit:.2f}")
    print(result)


# ---------------------------------------------------------------------
if __name__ == "__main__":
    main()
