import duckdb
import pandas as pd

CSV_PATH = 'data/SCMS_Delivery_History_Dataset.csv'   # ← ajustá el nombre
DB_PATH = 'supply_chain.duckdb'

# Conectar (crea el archivo de base de datos local)
con = duckdb.connect(DB_PATH)

# Cargar el CSV como tabla. normalize_names pasa todo a snake_case
con.execute(f"""
    CREATE OR REPLACE TABLE orders AS
    SELECT * FROM read_csv_auto('{CSV_PATH}',
                                header=True,
                                normalize_names=True)
""")

# Verificaciones rápidas
total = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
print(f"✓ Tabla 'orders' creada con {total:,} registros\n")

print("Columnas disponibles:")
cols = con.execute("DESCRIBE orders").df()
print(cols[['column_name', 'column_type']].to_string(index=False))

con.close()