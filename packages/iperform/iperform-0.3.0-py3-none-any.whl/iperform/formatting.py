import numpy as np
import pandas as pd


# ----------------------------------------------------------------------------------------------------------------------
# FONCTION FORMAT KPI
# ----------------------------------------------------------------------------------------------------------------------


def format_kpi(value, is_percentage=False):
    """Formate un nombre : 2 décimales pour %, 2 décimales sinon, avec séparateur milliers."""
    if pd.isna(value):
        return "-"
    if is_percentage:
        return f"{value:+.1%}" if not np.isnan(value) else "-"
    else:
        return f"{value:,.2f}".replace(",", " ").replace(".", ",")


# ----------------------------------------------------------------------------------------------------------------------

def format_kpi2(value, is_percentage=False):
    """
    Formate un nombre avec séparateurs de milliers, et ajoute un emoji coloré si c'est un pourcentage.
    """
    if pd.isna(value):
        return "<span style='color:orange'> </span> N/A" if is_percentage else "-"
    
    if is_percentage:
        # Choisir l'emoji et la couleur selon le signe
        if value > 0:
            emoji = ""
            color = "green"
        elif value < 0:
            emoji = ""
            color = "red"
        else:  # value == 0
            emoji = ""
            color = "yellow"
        
        # Format en pourcentage
        pct_str = f"{value:+.1%}"
        
        # Retourner le HTML pour afficher l'emoji coloré + le texte
        return f"<span style='color:{color}; font-weight:bold;'>{emoji}</span> {pct_str}"
    else:
        # Format numérique standard (avec séparateurs)
        return f"{value:,.2f}".replace(",", " ").replace(".", ",")
    
    