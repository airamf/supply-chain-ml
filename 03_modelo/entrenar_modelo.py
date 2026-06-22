"""
Entrena un Random Forest para predecir entregas tardías.
Maneja el desbalance de clases (88.5% vs 11.5%) con class_weight.
"""
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

# ── 1. Cargar datos ────────────────────────────────────
df = pd.read_csv('data/dataset_modelo.csv')
print(f"Registros: {len(df):,}")

cat_features = ['shipment_mode', 'country', 'vendor',
                'sub_classification', 'product_group']
num_features = ['unit_price', 'line_item_quantity']
target = 'entrega_tarde'

X = df[cat_features + num_features]
y = df[target]

# ── 2. Split estratificado (mantiene la proporción de clases) ──
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train: {len(X_train):,} · Test: {len(X_test):,}")

# ── 3. Preprocesamiento ────────────────────────────────
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore', min_frequency=10), cat_features),
    ('num', StandardScaler(), num_features)
])

# ── 4. Pipeline completo ───────────────────────────────
pipeline = Pipeline([
    ('prep', preprocessor),
    ('model', RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        class_weight='balanced',   # clave por el desbalance
        random_state=42,
        n_jobs=-1
    ))
])

# ── 5. Entrenar ────────────────────────────────────────
print("\nEntrenando...")
pipeline.fit(X_train, y_train)

# ── 6. Evaluar ─────────────────────────────────────────
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

print("\n" + "═" * 55)
print("REPORTE DE CLASIFICACIÓN")
print("═" * 55)
print(classification_report(y_test, y_pred,
      target_names=['A tiempo', 'Tarde']))

print("MATRIZ DE CONFUSIÓN")
print(confusion_matrix(y_test, y_pred))

auc = roc_auc_score(y_test, y_proba)
print(f"\n★ AUC-ROC: {auc:.3f}")

# ── 7. Guardar modelo ──────────────────────────────────
joblib.dump(pipeline, 'models/modelo_entregas_v1.pkl')
print("\n✓ Modelo guardado en models/modelo_entregas_v1.pkl")