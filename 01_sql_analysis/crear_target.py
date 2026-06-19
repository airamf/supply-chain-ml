import duckdb

con = duckdb.connect('supply_chain.duckdb')

# Crear tabla enriquecida con la variable objetivo
con.execute("""
    CREATE OR REPLACE TABLE orders_ml AS
    SELECT
        *,
        DATE_DIFF('day',
            STRPTIME(scheduled_delivery_date, '%d-%b-%y'),
            STRPTIME(delivered_to_client_date, '%d-%b-%y')
        ) AS dias_entrega,
        -- 1 si llegó DESPUÉS de lo programado, 0 si llegó a tiempo o antes
        CASE
            WHEN DATE_DIFF('day',
                STRPTIME(scheduled_delivery_date, '%d-%b-%y'),
                STRPTIME(delivered_to_client_date, '%d-%b-%y')
            ) > 0 THEN 1
            ELSE 0
        END AS entrega_tarde
    FROM orders
    WHERE scheduled_delivery_date IS NOT NULL
      AND delivered_to_client_date IS NOT NULL
""")

# Ver el balance de clases (clave para el modelo)
print("═" * 50)
print("BALANCE DE LA VARIABLE OBJETIVO")
print("═" * 50)
balance = con.execute("""
    SELECT
        entrega_tarde,
        COUNT(*) AS cantidad,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS porcentaje
    FROM orders_ml
    GROUP BY entrega_tarde
    ORDER BY entrega_tarde
""").df()
print(balance.to_string(index=False))

# Tasa de tardanza por modo de envío
print("\n" + "═" * 50)
print("% TARDANZA POR MODO DE ENVÍO")
print("═" * 50)
tardanza = con.execute("""
    SELECT
        shipment_mode,
        COUNT(*) AS total,
        SUM(entrega_tarde) AS tardes,
        ROUND(100.0 * SUM(entrega_tarde) / COUNT(*), 1) AS pct_tarde
    FROM orders_ml
    GROUP BY shipment_mode
    ORDER BY pct_tarde DESC
""").df()
print(tardanza.to_string(index=False))

total = con.execute("SELECT COUNT(*) FROM orders_ml").fetchone()[0]
print(f"\n✓ Tabla 'orders_ml' creada con {total:,} registros y variable objetivo")

con.close()