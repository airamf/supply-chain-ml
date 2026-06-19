import duckdb

con = duckdb.connect('supply_chain.duckdb')

# ───────────────────────────────────────────────────────────
# QUERY 1 · Volumen y valor por país de destino
# ───────────────────────────────────────────────────────────
print("═" * 60)
print("1. TOP 10 PAÍSES POR VALOR TOTAL DE ÓRDENES")
print("═" * 60)
q1 = con.execute("""
    SELECT
        country,
        COUNT(*)                          AS total_ordenes,
        ROUND(SUM(line_item_value), 0)    AS valor_total_usd,
        ROUND(AVG(unit_price), 2)         AS precio_unit_prom
    FROM orders
    GROUP BY country
    ORDER BY valor_total_usd DESC
    LIMIT 10
""").df()
print(q1.to_string(index=False))

# ───────────────────────────────────────────────────────────
# QUERY 2 · Performance por modo de envío
# ───────────────────────────────────────────────────────────
print("\n" + "═" * 60)
print("2. DISTRIBUCIÓN POR MODO DE ENVÍO")
print("═" * 60)
q2 = con.execute("""
    SELECT
        shipment_mode,
        COUNT(*)                        AS total,
        ROUND(AVG(line_item_value), 0)  AS valor_prom,
        ROUND(AVG(unit_price), 2)       AS precio_prom
    FROM orders
    WHERE shipment_mode IS NOT NULL
    GROUP BY shipment_mode
    ORDER BY total DESC
""").df()
print(q2.to_string(index=False))

# ───────────────────────────────────────────────────────────
# QUERY 3 · Días de entrega (convirtiendo fechas de texto)
# ───────────────────────────────────────────────────────────
print("\n" + "═" * 60)
print("3. DÍAS PROMEDIO ENTRE PROGRAMADO Y ENTREGADO")
print("═" * 60)
q3 = con.execute("""
    SELECT
        shipment_mode,
        COUNT(*) AS ordenes_validas,
        ROUND(AVG(
            DATE_DIFF('day',
                STRPTIME(scheduled_delivery_date, '%d-%b-%y'),
                STRPTIME(delivered_to_client_date, '%d-%b-%y')
            )
        ), 1) AS dias_prom_diferencia
    FROM orders
    WHERE scheduled_delivery_date IS NOT NULL
      AND delivered_to_client_date IS NOT NULL
    GROUP BY shipment_mode
    ORDER BY dias_prom_diferencia DESC
""").df()
print(q3.to_string(index=False))

# ───────────────────────────────────────────────────────────
# QUERY 4 · Top proveedores por volumen
# ───────────────────────────────────────────────────────────
print("\n" + "═" * 60)
print("4. TOP 10 PROVEEDORES POR CANTIDAD DE ÓRDENES")
print("═" * 60)
q4 = con.execute("""
    SELECT
        vendor,
        COUNT(*)                        AS total_ordenes,
        ROUND(SUM(line_item_value), 0)  AS valor_total_usd
    FROM orders
    GROUP BY vendor
    ORDER BY total_ordenes DESC
    LIMIT 10
""").df()
print(q4.to_string(index=False))

con.close()
print("\n✓ Análisis completado")