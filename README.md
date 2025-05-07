# 🏨 Sistema de Análisis de Precios de Hoteles con FastAPI

Este proyecto implementa un sistema completo de análisis de tarifas hoteleras usando Python, FastAPI, Pandas, SQLite y Matplotlib.

---

## 📦 Tecnologías Usadas
- **FastAPI**: Framework para construir APIs modernas.
- **SQLite**: Base de datos embebida para persistencia local.
- **Pandas**: Limpieza, transformación y análisis de datos.
- **Matplotlib**: Visualización de datos.
- **Uvicorn**: Servidor ASGI para ejecutar FastAPI.

---

## 📁 Estructura del Proyecto
```
hotel_price_analysis/
│
├── scrape_and_process.py # Limpieza y procesamiento de datos desde CSV
├── database.py # Creación y carga de datos a SQLite
├── visualization.py # Gráficas de precios históricos
├── main.py # API FastAPI con endpoints
├── hotel_bookings.csv # Dataset original (manual desde Kaggle)
├── hotels.db # Base de datos SQLite generada
├── hotel_price_trends.png # Gráfico de precios generado
├── requirements.txt # Dependencias del entorno
└── README.md # Documentación del proyecto
```

---

## 🚀 Instalación y Ejecución

### 1. Clona el repositorio
```bash
git clone <url_del_repo>
cd hotel_price_analysis
```

### 2. Crea un entorno virtual y activa
```bash
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4. Descarga el dataset desde Kaggle
🔗 [Hotel Booking Demand (Kaggle)](https://www.kaggle.com/jessemostipak/hotel-booking-demand)

Coloca el archivo hotel_bookings.csv en la raíz del proyecto.

### 5. Procesa los datos y genera la base de datos
```bash
python database.py
```

### 6. Ejecuta el servidor FastAPI
```bash
uvicorn main:app --reload
```

## 🌐 Endpoints Disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | / | Prueba de funcionamiento |
| GET | /hotels | Lista de hoteles con estadísticas |
| GET | /hotels/{hotel_name} | Detalle y métricas de un hotel |
| GET | /statistics/global | Estadísticas globales |
| GET | /trends/{hotel_name} | Genera gráfico de precios |

Accede a Swagger UI:
http://127.0.0.1:8000/docs

## 📊 Resultados y Visualización
- Se calculan precios diarios y promedio móvil de 7 días.
- Los resultados se almacenan en SQLite.
- Se genera un gráfico de líneas para un hotel con tendencia de precios.

## 🧠 Créditos
- Datos: Kaggle (Hotel Booking Demand)
