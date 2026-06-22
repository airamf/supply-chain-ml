import duckdb

con = duckdb.connect('supply_chain.duckdb')

# Exportar solo las columnas que vamos a usar + el target
con.execute("""
    COPY (
        SELECT
            shipment_mode,
            country,
            vendor,
            sub_classification,
            product_group,
            unit_price,
            line_item_quantity,
            entrega_tarde
        FROM orders_ml
        WHERE shipment_mode IS NOT NULL
    ) TO 'data/dataset_modelo.csv' (HEADER, DELIMITER ',')
""")

print("✓ Exportado: data/dataset_modelo.csv")
con.close()