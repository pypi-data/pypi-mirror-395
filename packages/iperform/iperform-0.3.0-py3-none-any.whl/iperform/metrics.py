import numpy as np
import pandas as pd
import math
from typing import Union

from scipy.stats import norm
from statsmodels.tsa.stattools import adfuller # Test de Dickey-Fuller augmenté (ADF)
from sklearn.metrics import mean_absolute_error, mean_squared_error

from pmdarima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX

#-----------------------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------------------

def p_model(
    df,
    n,
    endog,
    exog=None,
    model=None,
    alpha=0.05,
    trend='c'
    ):
    """
    Retourne les composants nécessaires pour les métriques probabilistes.
    
    Paramètres :
    - df : DataFrame complet
    - n : int, taille du test
    - endog : str, colonne cible
    - exog : str ou None, colonne exogène
    - model : SARIMAXResults ou None
    - alpha : float, niveau de signification
    - trend : str, type de régression
    
    Retourne :
    - y_test, y_pred, lower, upper, sigma (tous pd.Series, index alignés)
    """
    # Split
    train = df.iloc[:-n].copy()
    test = df.iloc[-n:].copy()
    
    y_train = train[endog]
    y_test = test[endog]
    
    # Entraîner le modèle si non fourni
    if model is None:
        # Préparer exogènes
        X_train = train[[exog]] if exog is not None else None
        
        # Auto ARIMA
        auto_model = auto_arima(
            y=y_train,
            X=X_train,
            d=1,
            seasonal=False,
            trace=False,
            error_action='ignore',
            suppress_warnings=True,
            stepwise=True
            )
        
        # Ajuster SARIMAX
        X_train_final = train[[exog]] if exog is not None else None
        sarimax_model = SARIMAX(
            endog=y_train,
            exog=X_train_final,
            order=auto_model.order,
            trend=trend
            ).fit(disp=False)
        model = sarimax_model
    
    # Prévoir
    X_test = test[[exog]] if exog is not None else None
    pred = model.get_prediction(
        start=len(y_train),
        end=len(y_train) + n - 1,
        exog=X_test
        )
    
    # Extraire et aligner
    y_pred = pred.predicted_mean
    y_pred.index = y_test.index
    
    ci = pred.conf_int(alpha=alpha)
    lower = ci.iloc[:, 0]
    upper = ci.iloc[:, 1]
    lower.index = upper.index = y_test.index
    
    sigma = pred.se_mean
    sigma.index = y_test.index
    
    return y_test, y_pred, lower, upper, sigma

#-----------------------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------------------


# CRPS – Continuous Ranked Probability Score (pour prévisions gaussiennes)

def crps(
        df, 
        n, 
        endog, 
        exog=None, 
        model=None, 
        alpha=0.05, 
        trend='c'
        ):
    """
        CRPS pour une prédiction gaussienne N(mu, sigma²).
    
        Paramètres :
        - y_true : array-like, valeurs réelles
        - mu     : array-like, moyennes des prédictions
        - sigma  : array-like, écarts-types des prédictions
    
        Retourne :
        - float : CRPS moyen
    """
    y_test, y_pred, _, _, sigma = p_model(df, n, endog, exog, model, alpha, trend)
    from scipy.stats import norm
    y_test = np.asarray(y_test)
    mu = np.asarray(y_pred)
    sigma = np.asarray(sigma)
    sigma = np.maximum(sigma, 1e-8)
    z = (y_test - mu) / sigma
    crps = sigma * (
        z * (2 * norm.cdf(z) - 1) +
        2 * norm.pdf(z) -
        1 / np.sqrt(np.pi)
    )
    return np.mean(crps)


#-----------------------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------------------
# Interval Score (Gneiting & Raftery, 2007)
def interval_score(
        df, 
        n, 
        endog, 
        exog=None, 
        model=None, 
        alpha=0.05, 
        trend='c'
        ):
    """
    Interval Score pour un intervalle de confiance à (1 - alpha).
    
    Pénalise les intervalles trop larges ET les erreurs de couverture.
    Plus le score est bas, mieux c'est.
    
    Paramètres :
    - y_true : array-like, valeurs réelles
    - lower  : array-like, borne inférieure (quantile α/2)
    - upper  : array-like, borne supérieure (quantile 1 - α/2)
    - alpha  : float, niveau de signification (ex: 0.05 pour IC 95%)
    
    Retourne :
    - float : interval score moyen
    """
    y_test, _, lower, upper, _ = p_model(df, n, endog, exog, model, alpha, trend)
    y_test = np.asarray(y_test)
    lower = np.asarray(lower)
    upper = np.asarray(upper)
    penalty_low = (2 / alpha) * (lower - y_test) * (y_test < lower)
    penalty_high = (2 / alpha) * (y_test - upper) * (y_test > upper)
    score = (upper - lower) + penalty_low + penalty_high
    return np.mean(score)


#-----------------------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------------------

# MPIW – Mean Prediction Interval Width
def mpiw(
        df, 
        n, 
        endog, 
        exog=None, 
        model=None, 
        alpha=0.05,
        trend='c'
        ):
    """
    Mean Prediction Interval Width (MPIW).
    
    Mesure la largeur moyenne des intervalles de prédiction.
    
    Paramètres :
    - lower : array-like, bornes inférieures
    - upper : array-like, bornes supérieures
    
    Retourne :
    - float : largeur moyenne
    """
    _, _, lower, upper, _ = p_model(df, n, endog, exog, model, alpha, trend)

    return (upper - lower).mean()


#-----------------------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------------------
# PICP – Prediction Interval Coverage Probability
def picp(
        df, 
        n, 
        endog, 
        exog=None, 
        model=None, 
        alpha=0.05,
        trend='c'
        ):
    """
    Prediction Interval Coverage Probability (PICP).
    
    Mesure le % de vraies valeurs contenues dans l'intervalle de prédiction.
    
    Paramètres :
    - y_true : array-like, valeurs réelles
    - lower  : array-like, bornes inférieures de l'IC
    - upper  : array-like, bornes supérieures de l'IC
    
    Retourne :
    - float : PICP entre 0 et 1
    """
    y_test, _, lower, upper, _ = p_model(df, n, endog, exog, model, alpha, trend)

    covered = ((y_test >= lower) & (y_test <= upper)).mean()

    return  covered.mean()

#-----------------------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------------------

# Fonctions auxiliaires pour MAE/RMSE
def mae(
        df, 
        n, 
        endog, 
        exog=None, 
        model=None,
        alpha=0.05,
        trend='c'
        ):
    y_test, y_pred, _, _, _ = p_model(df, n, endog, exog, model, alpha, trend)

    return np.mean(np.abs(y_test - y_pred))

#-----------------------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------------------

def rmse(
        df, 
        n, 
        endog, 
        exog=None, 
        model=None,
        alpha=0.05,
        trend='c'
        ):
    y_test, y_pred, _, _, _ = p_model(df, n, endog, exog, model, alpha, trend)

    return np.sqrt(np.mean((y_test - y_pred) ** 2))


#-----------------------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------------------

def evaluate_sarimax(
    df,
    n,
    endog,
    exog=None,
    model=None,
    alpha=0.05,
    trend='c',
    model_name="Model",
    decimals=2
    ):
    
    # Calculer toutes les métriques
    mae_val = mae(df, n, endog, exog, model, alpha, trend)
    rmse_val = rmse(df, n, endog, exog, model, alpha, trend)
    picp_val = picp(df, n, endog, exog, model, alpha, trend)
    mpiw_val = mpiw(df, n, endog, exog, model, alpha, trend)
    is_val = interval_score(df, n, endog, exog, model, alpha, trend)
    crps_val = crps(df, n, endog, exog, model, alpha, trend)
    
    # Infos du modèle (si on l'a entraîné)
    if model is None:
        # On ne peut pas récupérer order/trend sans le modèle → laisser vide ou entraîner une fois
        order, trend = "auto", "auto"
    else:
        order = str(model.model.order)
        trend = str(model.model.trend)
    
    return pd.DataFrame({
        'Model': [model_name],
        'MAE': [mae_val],
        'RMSE': [rmse_val],
        'PICP_95': [picp_val],
        'MPIW_95': [mpiw_val],
        'Interval_Score_95': [is_val],
        'CRPS': [crps_val],
        'Order': [order],
        'Trend': [trend],
        'Train_size': [len(df) - n],
        'Test_size': [n]
        }).round(decimals)


#-----------------------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------------------

def adf_test(series, name, regression='c'):
    """
    Effectue le test ADF avec une spécification de régression choisie.
    
    Paramètres :
    - series : pd.Series, la série temporelle
    - name : str, nom de la série pour l'affichage
    - regression : str, type de régression dans le test ADF
        * 'c'  : constante seulement (série stationnaire autour d'une moyenne)
        * 'ct' : constante + tendance (série stationnaire autour d'une tendance)
        * 'nc' : pas de constante (série autour de zéro)
    
    Retourne :
    - dict avec les résultats du test
    """
    # Supprimer les NaN
    y = series.dropna()
    
    # Vérifier qu'il reste des données
    if len(y) < 10:
        print(f"⚠️  Trop peu de données pour {name} après suppression des NaN.")
        return None
    
    # Lancer le test ADF
    try:
        result = adfuller(y, regression=regression)
    except ValueError as e:
        print(f"❌ Erreur dans le test ADF pour {name} (regression='{regression}') : {e}")
        return None
    
    adf_stat = result[0]
    p_value = result[1]
    crit_vals = result[4]
    
    # Interprétation du modèle testé
    if regression == 'c':
        model_desc = "constante seulement (stationnarité autour d'une moyenne)"
    elif regression == 'ct':
        model_desc = "constante + tendance (stationnarité autour d'une tendance)"
    elif regression == 'nc':
        model_desc = "pas de constante (stationnarité autour de zéro)"
    else:
        model_desc = f"spécification personnalisée : {regression}"
    
    # Affichage
    print(f"ADF Test pour {name} (régression : '{regression}')")
    print(f"  → Modèle testé : {model_desc}")
    print(f"  Statistique ADF: {adf_stat:.4f}")
    print(f"  p-value: {p_value:.4f}")
    print(f"  Critères :")
    print(f"\t- 1% : {crit_vals['1%']:.3f}")
    print(f"\t- 5% : {crit_vals['5%']:.3f}")
    print(f"\t- 10% : {crit_vals['10%']:.3f}")
    
    # Décision
    if p_value < 0.05:
        print(f"  → ✅ Stationnaire (rejet de H0 : pas de racine unitaire)\n")
    else:
        print(f"  → ❌ Non stationnaire (H0 non rejetée : présence probable d'une racine unitaire)\n")