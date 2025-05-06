# visualization.py
import matplotlib.pyplot as plt
import pandas as pd

def plot_hotel_trends(df: pd.DataFrame, hotel_name: str, output_file='hotel_price_trends.png'):
    # Filtrar datos por hotel
    hotel_df = df[df['hotel_name'] == hotel_name.lower()]

    if hotel_df.empty:
        raise ValueError(f"No se encontraron datos para el hotel: {hotel_name}")

    # Plotear líneas
    plt.figure(figsize=(12, 6))
    plt.plot(hotel_df['date'], hotel_df['price'], label='Precio Diario', color='skyblue', linewidth=2)
    plt.plot(hotel_df['date'], hotel_df['moving_avg_7d'], label='Promedio Móvil 7 días', color='orange', linewidth=2)

    plt.title(f"Tendencia de precios - {hotel_name.title()}")
    plt.xlabel("Fecha")
    plt.ylabel("Precio (€)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Guardar imagen
    plt.savefig(output_file)
    plt.close()
    print(f"📈 Gráfico generado y guardado como '{output_file}'")

# TEST LOCAL
if __name__ == "__main__":
    from scrape_and_process import load_and_clean_data, fill_missing_dates, impute_prices, compute_statistics
    df = load_and_clean_data()
    df = fill_missing_dates(df)
    df, _, _ = impute_prices(df)
    df = compute_statistics(df)

    # Cambia el nombre del hotel si quieres probar con otro
    plot_hotel_trends(df, hotel_name='city hotel')
