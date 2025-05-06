# scrape_and_process.py
import pandas as pd
import numpy as np
import os

def load_and_clean_data(filepath="hotel_bookings.csv"):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Archivo {filepath} no encontrado.")

    df = pd.read_csv(filepath)

    # Crear columna de fecha combinando año, mes y día
    df['date'] = pd.to_datetime(dict(year=df['arrival_date_year'],
                                     month=df['arrival_date_month'].map({
                                         'January':1, 'February':2, 'March':3, 'April':4, 'May':5,
                                         'June':6, 'July':7, 'August':8, 'September':9,
                                         'October':10, 'November':11, 'December':12
                                     }),
                                     day=df['arrival_date_day_of_month']))
    df['hotel'] = df['hotel'].str.lower()

    # Agrupar por hotel y fecha
    df = df.groupby(['hotel', 'date'])['adr'].mean().reset_index()
    df.rename(columns={'hotel': 'hotel_name', 'adr': 'price'}, inplace=True)

    return df

def fill_missing_dates(df):
    hotels = df['hotel_name'].unique()
    full_range = pd.date_range(start=df['date'].min(), end=df['date'].max())

    complete_data = []

    for hotel in hotels:
        hotel_df = df[df['hotel_name'] == hotel].set_index('date')
        hotel_df = hotel_df.reindex(full_range)
        hotel_df['hotel_name'] = hotel
        complete_data.append(hotel_df)

    full_df = pd.concat(complete_data)
    full_df.reset_index(inplace=True)
    full_df.rename(columns={'index': 'date'}, inplace=True)

    return full_df

def impute_prices(df):
    imputations = 0
    hotel_stats = {}

    for hotel in df['hotel_name'].unique():
        hotel_df = df[df['hotel_name'] == hotel].copy()
        prices = hotel_df['price'].values

        for i in range(len(prices)):
            if np.isnan(prices[i]):
                window = []
                for j in range(i - 3, i + 4):
                    if 0 <= j < len(prices) and j != i and not np.isnan(prices[j]):
                        window.append(prices[j])

                if len(window) >= 3:
                    prices[i] = np.mean(window)
                else:
                    prices[i] = np.nanmean(prices)

                imputations += 1
                hotel_stats[hotel] = hotel_stats.get(hotel, 0) + 1

        df.loc[df['hotel_name'] == hotel, 'price'] = prices

    hotel_missing_df = pd.DataFrame.from_dict(hotel_stats, orient='index', columns=['missing_count'])
    hotel_missing_df = hotel_missing_df.sort_values(by='missing_count', ascending=False)

    return df, imputations, hotel_missing_df

def compute_statistics(df):
    df.sort_values(by=['hotel_name', 'date'], inplace=True)
    df['moving_avg_7d'] = df.groupby('hotel_name')['price'].transform(lambda x: x.rolling(window=7, min_periods=1).mean())
    return df

# TEST LOCAL
if __name__ == "__main__":
    df = load_and_clean_data()
    df = fill_missing_dates(df)
    df, total_imputations, missing_report = impute_prices(df)
    df = compute_statistics(df)

    print("🧮 Estadísticas listas.")
    print(df.head(10))
