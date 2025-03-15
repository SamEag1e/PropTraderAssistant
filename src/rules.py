from datetime import timedelta
import copy


# ---------------------------------------------------------------------
def group_overlapping_trades(trades, time_window_minutes=5):
    """
    Groups trades based on the updated overlapping trade rule.
    """
    overlapping_trades = []
    current_group = None

    for trade in trades:
        # Skip all trades until the first profit trade
        if current_group is None and trade.profit <= 0:
            continue

        if current_group is None:
            # Start the first group with the first profit trade
            current_group = copy.deepcopy(trade)
            continue

        # Check if the current trade is within the time window
        last_close = current_group.close
        if trade.open <= last_close + timedelta(minutes=time_window_minutes):
            # Extend the group's close time
            current_group.close = max(current_group.close, trade.close)

            if trade.profit > 0:
                # Add profit only if the trade is profitable
                current_group.profit += trade.profit
            continue
        # End the current group and start a new one
        overlapping_trades.append(current_group)
        current_group = copy.deepcopy(trade) if trade.profit > 0 else None

    # Add the final group if it exists
    if current_group:
        overlapping_trades.append(current_group)

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


# ---------------------------------------------------------------------
def fast_scalp_profit_rule(trades, max_duration_seconds=30, max_percentage=20):
    """
    Checks if the sum of profitable trades opened and closed within a short time window
    (e.g., <= 30 seconds) is less than a specified percentage of gross profit.

    If the rule is not passed, calculates the required x such that:
    sum_fast_scalp_trades < (gross_profit + required_x) * (max_percentage / 100)

    Returns the result of the check or the required additional profit to pass the rule.
    """
    # Calculate the sum of profits for trades opened and closed within the time window
    sum_fast_scalp_trades = sum(
        trade.profit
        for trade in trades
        if trade.profit > 0
        and (trade.close - trade.open).total_seconds() <= max_duration_seconds
    )

    # Calculate the total gross profit (sum of all profitable trades)
    gross_profit = sum(trade.profit for trade in trades if trade.profit > 0)

    # Solve for X: sum_fast_scalp_trades < (gross_profit + X) * (max_percentage / 100)
    required_x = (
        sum_fast_scalp_trades / (max_percentage / 100)
    ) - gross_profit

    if required_x <= 0:
        return "Fast Scalp Profit Rule Passed."
    return f"Fast Scalp Profit Rule Failed. Required: {(required_x + 0.01):.2f} profit."
