
"""
Created on Sun Sep 14 10:44:05 2025

@author: 'patrick ILUNGA'
"""

import os
import pandas as pd


def load_sample_data():
    """
    Charge un jeu de données exemple basé sur des données publiques (ex: ARTPC).
    
    Returns:
        pd.DataFrame
    """
    # Chemin vers le fichier CSV
    module_dir = os.path.dirname(__file__)
    data_path = os.path.join(module_dir, '..', 'data', 'data_arptc.csv')
    
    try:
        df = pd.read_csv(data_path)
        # Convertir la date
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Fichier de données exemple non trouvé : {data_path}\n"
            "Assurez-vous que 'data/artpc_data.csv' existe."
            )