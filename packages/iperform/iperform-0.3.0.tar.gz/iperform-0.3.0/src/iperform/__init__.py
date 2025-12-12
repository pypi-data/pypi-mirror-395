"""
iperform - Tableau de bord analytique dynamique pour telecom & banque

Conçu pour être simple, complet et communautaire.
Toutes les fonctions principales sont accessibles via `ip.fonction()`.

Pour les fonctionnalités avancées (prévision SARIMAX, narration, alertes, élaboration budget),
voir `iperform_cloud` : https://www.ipgeodata.com
"""

import os

# --- Version du package ---
__version__ = "0.2.0"

# --- Fonctions principales (exposées au niveau racine) ---
from .core import (
    get_summary_day,
    get_summary_month,
    get_summary_quarter,
    get_summary_half,
    get_summary_year,
    get_column_day,
    get_column_month,
    get_column_quarter,
    get_column_half,
    get_column_year,
    dday,
    mtd, qtd, ytd, htd, wtd,
    full_w, full_m, full_q, full_h, full_y,
    forecast_m,
    c_rate
    )

# --- Plotting KPIs ---
from .plotting import (
    graph_trend_day,
    plot_kpi,
    graph_season,
    graph_trend
    )

# --- Formatting KPIs ---
from .formatting import format_kpi

# --- Metric Models
from .metrics import(
    p_model,
    crps,
    interval_score,
    mpiw,
    picp,
    mae,
    rmse,
    evaluate_sarimax,
    adf_test
    )

# --- Utilitaires ---
from .utils import load_sample_data


# --- Contrôle de `from iperform import *` ---
__all__ = ["get_summary_day", "get_summary_month", "get_summary_quarter", "get_summary_half", "get_summary_year",
           "get_column_day", "get_column_month", "get_column_quarter", "get_column_half", "get_column_year",
           "graph_trend_day", "plot_kpi", "graph_season", "graph_trend",
           "dday",
           "wtd", "mtd", "qtd", "htd", "ytd",
           "full_w", "full_m", "full_q", "full_h", "full_y",
           "forecast_m",
           "c_rate",
           "format_kpi",
           "load_sample_data",
           "p_model", "crps", "interval_score", "mpiw", "picp", "mae", "rmse", "evaluate_sarimax", "adf_test",
           "__version__"
           ]