# Supply Chain ML · Predicción de Entregas Tardías

Proyecto de análisis y predicción sobre datos reales de supply chain (SCMS Delivery History).

## Stack
SQL (DuckDB) · Python · scikit-learn · Power BI · Streamlit

## Estructura
- `01_sql_analysis/` — Queries SQL de negocio
- `02_eda/` — Análisis exploratorio
- `03_modelo/` — Modelo de ML
- `04_dashboard/` — Dashboard Power BI
- `05_pipeline/` — Scoring automatizado

## Resultados del Modelo v1 (Random Forest)

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| AUC-ROC | 0.813 | Buena capacidad de discriminación |
| Recall (Tarde) | 0.85 | Detecta 85% de las entregas tardías reales |
| Precision (Tarde) | 0.24 | 1 de cada 4 alertas es atraso real |

**Decisión de diseño:** se priorizó recall sobre precision con `class_weight='balanced'`,
porque en supply chain el costo de no anticipar un atraso supera al de una falsa alarma.

**Matriz de confusión:** detecta 202 de 237 atrasos reales (solo 35 escapados).