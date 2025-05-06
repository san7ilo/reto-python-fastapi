# database.py
import sqlite3
import pandas as pd

DB_NAME = 'hotels.db'

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hotel_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_name TEXT,
            date DATE,
            price FLOAT,
            moving_avg_7d FLOAT
        )
    ''')

    conn.commit()
    conn.close()
    print("🗃️ Base de datos y tabla creada correctamente.")

def insert_data(df: pd.DataFrame):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Insertar filas
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO hotel_prices (hotel_name, date, price, moving_avg_7d)
            VALUES (?, ?, ?, ?)
        ''', (row['hotel_name'], row['date'].strftime('%Y-%m-%d'), row['price'], row['moving_avg_7d']))

    conn.commit()
    conn.close()
    print(f"📦 {len(df)} registros insertados en 'hotel_prices'.")

# TEST LOCAL
if __name__ == "__main__":
    from scrape_and_process import load_and_clean_data, fill_missing_dates, impute_prices, compute_statistics

    df = load_and_clean_data()
    df = fill_missing_dates(df)
    df, _, _ = impute_prices(df)
    df = compute_statistics(df)

    create_database()
    insert_data(df)
