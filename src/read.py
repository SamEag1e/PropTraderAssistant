from datetime import datetime

from bs4 import BeautifulSoup

from trade import Trade


# ---------------------------------------------------------------------
def get_position_order_row(rows):
    """
    Locate the "Positions" and "Orders" header rows.
    """
    if rows is None:
        return (None, None)
    positions_row = None
    orders_row = None
    for i, row in enumerate(rows):
        if positions_row is None and "<b>Positions</b>" in str(row):
            positions_row = i
        elif "<b>Orders</b>" in str(row):
            orders_row = i
            break
    return (positions_row, orders_row)


# ---------------------------------------------------------------------
def get_html_trades(html_file_path):
    """
    Reads an HTML file and extracts trades from the
    'Positions' table into a list of Trade objects.
    """
    trades = []

    with open(html_file_path, "r", encoding="utf-16") as file:
        soup = BeautifulSoup(file, "html.parser")
        rows = soup.find_all("tr")

        positions_row, orders_row = get_position_order_row(rows)
        if None in (positions_row, orders_row):
            return trades

        # Extract the rows between the "Positions" and "Orders"
        for row in rows[positions_row + 2 : orders_row - 1]:
            cols = [col.text.strip() for col in row.find_all("td")]
            open_t = datetime.strptime(cols[0].strip(), "%Y.%m.%d %H:%M:%S")
            close_t = datetime.strptime(cols[9].strip(), "%Y.%m.%d %H:%M:%S")
            commission = float(cols[-3].strip())
            swap = float(cols[-2].strip())
            profit = float(cols[-1].strip()) + (commission + swap)

            trades.append(Trade(profit, open_t, close_t))

    return trades
