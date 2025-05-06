# main.py
from fastapi import FastAPI, HTTPException
from scrape_and_process import load_and_clean_data, fill_missing_dates, impute_prices, compute_statistics
from pydantic import BaseModel
import sqlite3
import pandas as pd
from visualization import plot_hotel_trends
import os

# Inicializa FastAPI
app = FastAPI(title="Hotel Price Analysis API 🚀")

DB_NAME = 'hotels.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

# 🔹 Ruta raíz de prueba
@app.get("/")
def root():
    return {"mensaje": "FastAPI operativo 🔥"}

# 🔹 Lista de hoteles y estadísticas generales
@app.get("/hotels")
def list_hotels():
    conn = get_connection()
    query = """
    SELECT hotel_name, COUNT(*) AS registros,
           ROUND(AVG(price), 2) AS promedio,
           ROUND(MIN(price), 2) AS minimo,
           ROUND(MAX(price), 2) AS maximo
    FROM hotel_prices
    GROUP BY hotel_name
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")

# 🔹 Detalle de un hotel específico
@app.get("/hotels/{hotel_name}")
def hotel_details(hotel_name: str):
    conn = get_connection()
    query = """
    SELECT * FROM hotel_prices
    WHERE hotel_name = ?
    ORDER BY date ASC
    """
    df = pd.read_sql_query(query, conn, params=(hotel_name.lower(),))
    conn.close()

    if df.empty:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")

    return {
        "hotel_name": hotel_name,
        "registros": len(df),
        "precio_promedio": round(df['price'].mean(), 2),
        "precio_máximo": round(df['price'].max(), 2),
        "precio_mínimo": round(df['price'].min(), 2)
    }

# 🔹 Estadísticas globales
@app.get("/statistics/global")
def global_stats():
    conn = get_connection()
    query = "SELECT * FROM hotel_prices"
    df = pd.read_sql_query(query, conn)
    conn.close()

    return {
        "total_registros": len(df),
        "hoteles": df['hotel_name'].nunique(),
        "precio_promedio_global": round(df['price'].mean(), 2),
        "precio_máximo_global": round(df['price'].max(), 2),
        "precio_mínimo_global": round(df['price'].min(), 2)
    }

# 🔹 Gráfico de tendencias por hotel
@app.get("/trends/{hotel_name}")
def trends(hotel_name: str):
    conn = get_connection()
    query = "SELECT * FROM hotel_prices WHERE hotel_name = ? ORDER BY date ASC"
    df = pd.read_sql_query(query, conn, params=(hotel_name.lower(),))
    conn.close()

    if df.empty:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")

    plot_hotel_trends(df, hotel_name)
    return {"mensaje": f"Gráfico generado para {hotel_name}", "archivo": "hotel_price_trends.png"}
