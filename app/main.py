from read import read_html_trades
from rules import eighty_percent_rule_check, group_overlapping_trades


def main():
    # Input: Assume we are using an HTML file for now
    file_path = "trade_history.html"

    trades = read_html_trades(file_path)

    overlapping_trades = group_overlapping_trades(trades)
    result = eighty_percent_rule_check(overlapping_trades)

    print("\n\nTrades")
    for trade in trades:
        print(trade)
    print("\n\nOverlapping Trades")
    for trade in overlapping_trades:
        print(trade)
    gross_profit = sum(trade.profit for trade in overlapping_trades)
    print(f"\nGross Profit: {gross_profit:.2f}")
    print(result)


if __name__ == "__main__":
    main()
