from datetime import timedelta

from trade import Trade


# ---------------------------------------------------------------------
def group_overlapping_trades(trades, time_window_minutes=5):
    """
    Groups trades that overlap or are within
    a time window into overlapping trades.
    """
    overlapping_trades = []
    current_group = [trades[0]]  # Start with the first trade

    for trade in trades[1:]:
        last_trade_in_group = current_group[-1]

        if trade.open <= last_trade_in_group.close + timedelta(
            minutes=time_window_minutes
        ):
            # Merge overlapping trades
            total_profit = sum(t.profit for t in current_group) + trade.profit
            earliest_open = min(t.open for t in current_group + [trade])
            latest_close = max(t.close for t in current_group + [trade])
            current_group = [Trade(total_profit, earliest_open, latest_close)]
        else:
            # Save the current group and start a new one
            overlapping_trades.append(current_group[0])
            current_group = [trade]

    overlapping_trades.append(current_group[0])
    return overlapping_trades


# ---------------------------------------------------------------------
def eighty_percent_rule_check(overlapping_trades):
    """
    Checks if the 80% rule is satisfied:
    Max overlapping trades < (Gross Profit + X) * 0.8
    Returns the smallest X that satisfies the rule or passes the check.
    """
    gross_profit = sum(trade.profit for trade in overlapping_trades)
    max_overlapping_profit = max(trade.profit for trade in overlapping_trades)

    # Solve for X: max_overlapping_profit < (gross_profit + X) * 0.8
    required_x = (max_overlapping_profit / 0.8) - gross_profit

    if required_x <= 0:
        return "80% Rule Passed."
    return f"80% Rule Failed. Required: {(required_x + 0.01):.2f} profit."
