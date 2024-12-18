from trade import Trade
from bs4 import BeautifulSoup
from datetime import datetime


def read_html_trades(html_file_path):
    """
    Reads an HTML file and extracts trades from the 'Positions' table into a list of Trade objects.
    """
    profit_trades = []

    with open(html_file_path, "r", encoding="utf-16") as file:
        soup = BeautifulSoup(file, "html.parser")

        # Locate all tables in the HTML
        tables = soup.find_all("table")

        for table in tables:
            rows = table.find_all("tr")
            # for row in rows:
            #     print(row)
            # Locate the "Positions" and "Orders" header rows
            positions_row = None
            orders_row = None
            for i, row in enumerate(rows):
                if positions_row is None and "<b>Positions</b>" in str(row):
                    positions_row = i
                elif "<b>Orders</b>" in str(row):
                    orders_row = i
                    break  # Stop once the "Orders" row is found

            # Ensure both rows were found
            if positions_row is None and orders_row is None:
                return profit_trades
                # Extract the rows between the "Positions" and "Orders"
            for row in rows[positions_row + 2 : orders_row - 1]:
                cols = [col.text.strip() for col in row.find_all("td")]
                open_time = datetime.strptime(
                    cols[0].strip(), "%Y.%m.%d %H:%M:%S"
                )
                close_time = datetime.strptime(
                    cols[9].strip(), "%Y.%m.%d %H:%M:%S"
                )
                profit = float(cols[-1].strip())

                # Only include trades with a profit
                if profit > 0:
                    profit_trades.append(Trade(profit, open_time, close_time))

    return profit_trades
