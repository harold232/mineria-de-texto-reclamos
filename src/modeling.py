from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def entrenar_modelo(df):
    """Entrena un modelo de clasificación para predecir el resultado de un reclamo"""
    X = df[['AÑO', 'MES']]  # Selecciona más features relevantes después
    y = df['DE_RESULTADO'].apply(lambda x: 1 if x == "Favorable" else 0)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print(f"Precisión del modelo: {accuracy_score(y_test, y_pred):.2f}")
    
    return model
