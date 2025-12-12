"""
Module de modélisation avancée pour la version SaaS d'iperform.
Fonctions de régression, classification, clustering adaptées au secteur télécom.
"""
import numpy as np
import pandas as pd
from typing import Union, Optional, Tuple
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

def forecast_m_advanced(
    df: pd.DataFrame,
    date_col: str = 'date',
    target_col: str = 'revenu',
    features: Optional[list] = None,
    model_type: str = 'RandomForest',
    test_size: float = 0.2,
    random_state: int = 42
) -> dict:
    """
    Projection mensuelle avancée avec modèles de machine learning.
    
    Args:
        df (pd.DataFrame): DataFrame avec colonnes de date et de features.
        date_col (str): Nom de la colonne date.
        target_col (str): Colonne cible à prédire.
        features (list): Liste des colonnes features. Si None, utilise des features temporelles.
        model_type (str): 'Linear', 'Ridge', 'Lasso', 'RandomForest', 'GradientBoosting'
        test_size (float): Proportion des données pour le test.
        random_state (int): Graine pour la reproductibilité.
    
    Returns:
        dict: {
            'model': modèle entraîné,
            'score_train': R² sur train,
            'score_test': R² sur test,
            'mae': Mean Absolute Error,
            'forecast_function': fonction pour prédire un jour donné
        }
    """
    # Copie du DataFrame
    data = df.copy()
    
    # Convertir la date si nécessaire
    if not pd.api.types.is_datetime64_any_dtype(data[date_col]):
        data[date_col] = pd.to_datetime(data[date_col])
    
    # Créer des features temporelles si aucune n'est fournie
    if features is None:
        data['day_of_month'] = data[date_col].dt.day
        data['day_of_week'] = data[date_col].dt.dayofweek
        data['month'] = data[date_col].dt.month
        data['is_weekend'] = (data[date_col].dt.dayofweek >= 5).astype(int)
        features = ['day_of_month', 'day_of_week', 'month', 'is_weekend']
    
    # Supprimer les lignes avec des NaN
    data = data.dropna(subset=[target_col] + features)
    
    # Séparer features et target
    X = data[features]
    y = data[target_col]
    
    # Standardiser les features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=features)
    
    # Séparer train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=test_size, random_state=random_state
    )
    
    # Choisir le modèle
    models = {
        'Linear': LinearRegression(),
        'Ridge': Ridge(alpha=1.0),
        'Lasso': Lasso(alpha=1.0),
        'RandomForest': RandomForestRegressor(n_estimators=100, random_state=random_state),
        'GradientBoosting': GradientBoostingRegressor(n_estimators=100, random_state=random_state)
    }
    
    if model_type not in models:
        raise ValueError(f"Modèle {model_type} non supporté. Choisissez parmi {list(models.keys())}")
    
    model = models[model_type]
    model.fit(X_train, y_train)
    
    # Évaluer
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    score_train = r2_score(y_train, y_train_pred)
    score_test = r2_score(y_test, y_test_pred)
    mae = mean_absolute_error(y_test, y_test_pred)
    
    # Fonction de prédiction pour un jour donné
    def predict_for_date(date_str: str, **kwargs) -> float:
        """Prédit la valeur pour une date donnée."""
        date = pd.to_datetime(date_str)
        input_data = {}
        for feat in features:
            if feat == 'day_of_month':
                input_data[feat] = date.day
            elif feat == 'day_of_week':
                input_data[feat] = date.dayofweek
            elif feat == 'month':
                input_data[feat] = date.month
            elif feat == 'is_weekend':
                input_data[feat] = 1 if date.dayofweek >= 5 else 0
            else:
                # Pour les autres features, utiliser la valeur moyenne ou celle fournie
                if feat in kwargs:
                    input_data[feat] = kwargs[feat]
                else:
                    input_data[feat] = X[feat].mean()
        
        input_df = pd.DataFrame([input_data])
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]
        return float(prediction)
    
    return {
        'model': model,
        'scaler': scaler,
        'features': features,
        'score_train': score_train,
        'score_test': score_test,
        'mae': mae,
        'forecast_function': predict_for_date
    }

def cluster_customers(
    df: pd.DataFrame,
    features: list,
    n_clusters: int = 3,
    random_state: int = 42
) -> Tuple[pd.DataFrame, object]:
    """
    Clusterise les clients en segments (ex: haut revenu, faible usage, etc.).
    
    Args:
        df (pd.DataFrame): DataFrame avec les features clients.
        features (list): Colonnes à utiliser pour le clustering.
        n_clusters (int): Nombre de clusters.
        random_state (int): Graine pour la reproductibilité.
    
    Returns:
        Tuple[pd.DataFrame, KMeans]: DataFrame avec colonne 'cluster', et modèle entraîné.
    """
    from sklearn.cluster import KMeans
    
    data = df[features].copy()
    data = data.dropna()
    
    # Standardiser
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    
    # Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    clusters = kmeans.fit_predict(data_scaled)
    
    df_with_clusters = df.copy()
    df_with_clusters['cluster'] = np.nan
    df_with_clusters.loc[data.index, 'cluster'] = clusters
    
    return df_with_clusters, kmeans

def detect_anomalies(
    df: pd.DataFrame,
    target_col: str,
    method: str = 'IQR',
    threshold: float = 1.5
) -> pd.DataFrame:
    """
    Détecte les anomalies dans une série temporelle.
    
    Args:
        df (pd.DataFrame): DataFrame avec la série.
        target_col (str): Colonne à analyser.
        method (str): 'IQR' ou 'ZScore'
        threshold (float): Seuil pour la détection.
    
    Returns:
        pd.DataFrame: DataFrame avec colonne 'is_anomaly'
    """
    data = df.copy()
    data['is_anomaly'] = False
    
    if method == 'IQR':
        Q1 = data[target_col].quantile(0.25)
        Q3 = data[target_col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        data['is_anomaly'] = (data[target_col] < lower_bound) | (data[target_col] > upper_bound)
    
    elif method == 'ZScore':
        mean = data[target_col].mean()
        std = data[target_col].std()
        z_scores = (data[target_col] - mean) / std
        data['is_anomaly'] = z_scores.abs() > threshold
    
    else:
        raise ValueError("Méthode non supportée. Choisissez 'IQR' ou 'ZScore'")
    
    return data