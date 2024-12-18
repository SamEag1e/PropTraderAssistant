# ---------------------------------------------------------------------
class Trade:
    # -----------------------------------------------------------------
    def __init__(self, profit, open_time, close_time):
        self.profit = profit
        self.open = open_time
        self.close = close_time

    # -----------------------------------------------------------------
    def __repr__(self):
        return f"Trade(profit={self.profit}, open={self.open}, close={self.close})"
