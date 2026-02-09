import mysql.connector
from mysql.connector import Error

# Database connection function
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='bakery_busness'
    )

def export_orders_to_text():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM orders_improved_table ORDER BY order_ID DESC"
        cursor.execute(query)
        orders = cursor.fetchall()

        if not orders:
            print("No orders found to export.")
            return

        # Define column headers
        headers = [
            "order_ID", "order_identification_number", "items_count",
            "order_desc", "user_id", "Total_ammount", "DATE", "TIME", "LAST_UPDATE"
        ]

        # Determine max width per column for neat alignment
        col_widths = {h: len(h) for h in headers}
        for order in orders:
            for h in headers:
                value = str(order[h]) if order[h] is not None else ""
                # Consider multi-line text length
                for line in value.splitlines():
                    col_widths[h] = max(col_widths[h], len(line))

        # Create horizontal separator
        separator = "+".join("-" * (col_widths[h] + 2) for h in headers)

        with open("orders_export.txt", "w", encoding="utf-8") as f:
            # Write headers
            header_row = "|".join(f" {h.ljust(col_widths[h])} " for h in headers)
            f.write(header_row + "\n")
            f.write(separator + "\n")

            # Write each order
            for order in orders:
                # Split multi-line order_desc
                desc_lines = str(order["order_desc"]).splitlines() if order["order_desc"] else [""]
                max_lines = max(1, len(desc_lines))
                for i in range(max_lines):
                    row = []
                    for h in headers:
                        if h == "order_desc":
                            val = desc_lines[i] if i < len(desc_lines) else ""
                        else:
                            val = str(order[h]) if i == 0 else ""
                        row.append(val.ljust(col_widths[h]))
                    f.write("| " + " | ".join(row) + " |\n")
                f.write(separator + "\n")

        print("Orders exported successfully to orders_export.txt")

    except Error as e:
        print(f"Error fetching orders: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    export_orders_to_text()
