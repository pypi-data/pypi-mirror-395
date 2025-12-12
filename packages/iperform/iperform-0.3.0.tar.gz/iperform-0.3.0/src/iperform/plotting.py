
"""
Created on Sun Sep 14 10:03:47 2025

@author: patrickilunga
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


def plot_kpi(df, value, factor='all_factor', zone='all_zone', freq='month'):
    """
    Trace l'évolution temporelle d'un KPI avec zone de confiance colorée.
    
    Args:
        df (pd.DataFrame): DataFrame avec colonnes temporelles (month, quarter, half, year)
        value (str): Nom de la colonne KPI à tracer (ex: 'user_actif', 'revenu', 'ARPU')
        factor (str): Opérateur spécifique ou 'all_factor' (trace la somme)
        zone (str): Filtre géographique (ex: 'all_zone', 'Kinshasa')
        freq (str): Fréquence d'agrégation ('month', 'quarter', 'half', 'year')
    
    Returns:
        matplotlib.axes.Axes: L'objet graphique
    """
    
    # Palette de couleurs par opérateur
    factor_colors = {
        'Africell': 'purple',
        'Airtel': 'red',
        'Orange': 'orange',
        'Tigo': 'blue',
        'Vodacom': 'green',
        'all_factor': 'gray'
        }
    
    # Copie pour ne pas modifier l'original
    df = df.copy()
    
    # Filtrer par zone
    df = df[df['zone'] == zone]
    
    # Si 'all_factor', agréger tous les opérateurs (sauf la ligne 'all_factor' si elle existe).
    if factor == 'all_factor':
        df = df[df['factor'] != 'all_factor']  # Exclure la ligne agrégée si elle existe
        df_grouped = df.groupby([freq, 'factor'])[value].sum().reset_index()
        df_pivot = df_grouped.pivot(index=freq, columns='factor', values=value)
        df_plot = df_pivot.sum(axis=1).reset_index(name=value)
        df_plot['factor'] = 'all_factor'
    else:
        df_plot = df[df['factor'] == factor].copy()
        if df_plot.empty:
            raise ValueError(f"Aucune donnée trouvée pour factor='{factor}' et zone='{zone}'")
    
    # Trier par date
    if freq == 'month':
        df_plot = df_plot.sort_values('month')
        x_col = 'month'
        xlabel = 'Mois'
    elif freq == 'quarter':
        df_plot = df_plot.sort_values('quarter')
        x_col = 'quarter'
        xlabel = 'Trimestre'
    elif freq == 'half':
        df_plot = df_plot.sort_values('half')
        x_col = 'half'
        xlabel = 'Semestre'
    elif freq == 'year':
        df_plot = df_plot.sort_values('year')
        x_col = 'year'
        xlabel = 'Année'
    else:
        raise ValueError("freq doit être 'month', 'quarter', 'half', ou 'year'")
    
    # Définir la couleur
    color = factor_colors.get(factor, 'gray')
    
    # Créer le graphique
    plt.figure(figsize=(14, 7))
    ax = sns.lineplot(
        data=df_plot,
        x=x_col,
        y=value,
        marker='',
        linewidth=3,
        markersize=8,
        color=color,
        label=factor
        )
    
    # Ajouter la zone colorée semi-transparente
    ax.fill_between(
        df_plot[x_col],
        df_plot[value],
        alpha=0.2,
        color=color
        )
    
    # Titre et labels
    ax.set_title(f"Évolution de {value} — {factor} ({zone}) — Fréquence: {freq}", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(value, fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(title='Opérateur', fontsize=11, title_fontsize=12)
    
    # Rotation des labels si nécessaire
    if freq in ['month', 'quarter', 'half']:
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    return ax


# -------------------------------------------------------------------------------------------------------------------------------
# GRAPH DAY
# -------------------------------------------------------------------------------------------------------------------------------


def graph_trend_day(df, var, zone='all_zone', factor='all_factor', date_first=None, date_last='last'):
    """
    Trace l'évolution quotidienne d'une variable avec une tendance polynomiale (degré 3),
    filtrée par zone, opérateur et plage de dates.

    Args :
        df (pd.DataFrame): DataFrame avec colonnes 'date' (datetime), 'zone', 'factor', et la variable.
        var (str) : Nom de la colonne à tracer (ex: 'revenu', 'user_actif').
        zone (str): Filtre par zone. 'all_zone' pour tout le pays. Par défaut 'all_zone'.
        factor (str): Filtre par opérateur. 'all_factor' pour tous (sauf les totaux si besoin). Par défaut 'all_factor'.
        date_first (str or datetime): Date de début. Si None, prend la première date du DF.
        date_last (str or datetime or 'last'): Date de fin. Si 'last', prend la dernière date du DF.

    Returns:
        None: Affiche le graphique.
    """
    # Copie pour ne pas modifier l'original
    data = df.copy()

    # 1. Convertir 'date' en datetime si nécessaire
    if not pd.api.types.is_datetime64_any_dtype(data['date']):
        data['date'] = pd.to_datetime(data['date'])

    # 2. Définir les dates de début et fin
    if date_last == 'last':
        date_end = data['date'].max()
    else:
        date_end = pd.to_datetime(date_last)

    if date_first is None:
        date_start = data['date'].min()
    else:
        date_start = pd.to_datetime(date_first)

    # 3. Filtrer par date
    data = data[(data['date'] >= date_start) & (data['date'] <= date_end)]

    # 4. Filtrer par zone
    if zone != 'all_zone':
        data = data[data['zone'] == zone]

    # 5. Filtrer par opérateur
    if factor == 'all_factor':
        # Optionnel : exclure les lignes où factor est 'all_factor' (si ce sont des totaux)
        if 'all_factor' in data['factor'].values:
            data = data[data['factor'] != 'all_factor']
    else:
        data = data[data['factor'] == factor]

    # Vérifier que des données existent après filtrage
    if data.empty:
        print("Aucune donnée disponible après filtrage.")
        return

    # 6. Préparer les données pour le graphique
    data.set_index('date', inplace=True)
    data.sort_index(inplace=True)  # S'assurer que les dates sont triées

    x = data.index
    y = data[var]

    if y.isna().all():
        print(f"Aucune valeur valide pour '{var}' dans la période sélectionnée.")
        return

    # 7. Style
    sns.set_style("whitegrid")
    plt.rcParams["figure.figsize"] = (14, 7)

    fig, ax = plt.subplots(1, 1)

    # Courbe principale
    ax.plot(x, y, color='red', linewidth=1.5, label=var)
    ax.fill_between(x, y, color='red', alpha=0.1, edgecolor='red', linewidth=0)

    # 8. Tendance polynomiale (degré 3)
    x_num = (x - x[0]).days  # jours depuis le début
    try:
        z = np.polyfit(x_num, y, 3)  # ajustement polynomial
        p = np.poly1d(z)
        trend = p(x_num)
        ax.plot(x, trend, color='blue', linewidth=1.0, linestyle='--', alpha=0.8, label='Tendance polynomiale (degré 3)')
    except np.linalg.LinAlgError:
        print("Impossible d'ajuster la tendance polynomiale (peu de données ou variance nulle).")
        pass

    # 9. Style du graphique
    title = f'Évolution de {var}'
    if zone != 'all_zone':
        title += f' - Zone: {zone}'
    if factor != 'all_factor':
        title += f' - Opérateur: {factor}'
    ax.set_title(title, fontsize=16, weight='bold', pad=20)

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel(var, fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    # 10. Ajuster et afficher
    plt.tight_layout()
    plt.show()


# -------------------------------------------------------------------------------------------------------------------------------
# GRAPH SEASON
# -------------------------------------------------------------------------------------------------------------------------------


def graph_season(df, col_value, zone=None, factor=None, date_col='date', window=7):
    """
    Trace un graphique saisonnier superposant les courbes lissées par année,
    avec une zone colorée entre le min et le max des années pour chaque jour.
    
    Arguments:
    - df: DataFrame contenant les données
    - col_value: nom de la colonne à tracer (ex: 'revenu')
    - zone: (optionnel) filtre sur la colonne 'zone'
    - factor: (optionnel) filtre sur la colonne 'factor'
    - date_col: nom de la colonne contenant les dates (par défaut 'date')
    - window: taille de la fenêtre de lissage (défaut=7)
    """
    # Filtrer le DataFrame
    df_filtered = df.copy()
    if zone is not None:
        df_filtered = df_filtered[df_filtered['zone'] == zone]
    if factor is not None:
        df_filtered = df_filtered[df_filtered['factor'] == factor]
    
    if df_filtered.empty:
        print("Aucune donnée après filtrage.")
        return

    # S'assurer que la colonne date est au format datetime
    df_filtered[date_col] = pd.to_datetime(df_filtered[date_col])
    
    # Extraire l'année et créer une colonne "day_month" (MM-DD)
    df_filtered['year'] = df_filtered[date_col].dt.year
    df_filtered['day_month'] = df_filtered[date_col].dt.strftime('%m-%d')
    # Supprimer le 29 février pour éviter les trous dans les années non bissextiles
    df_filtered = df_filtered[df_filtered['day_month'] != '02-29']
    
    # Créer une date "pivot" pour l'axe X (année 2000)
    df_filtered['plot_date'] = pd.to_datetime('2000-' + df_filtered['day_month'])
    
    # Trier par année puis par date pour le lissage
    df_filtered = df_filtered.sort_values(['year', date_col]).reset_index(drop=True)
    
    # Appliquer le lissage par moyenne mobile (cumulatif au début, puis glissant)
    smoothed_values = []
    for year in df_filtered['year'].unique():
        yearly_data = df_filtered[df_filtered['year'] == year].copy()
        values = yearly_data[col_value].values
        smoothed = []
        
        for i in range(len(values)):
            if i < window:
                # Cumulatif : moyenne des jours 0 à i
                smoothed.append(np.mean(values[:i+1]))
            else:
                # Glissant : moyenne des 7 derniers jours (i-6 à i)
                smoothed.append(np.mean(values[i-window+1:i+1]))
        
        yearly_data['smoothed'] = smoothed
        smoothed_values.append(yearly_data)
    
    # Recombiner les données lissées
    df_smoothed = pd.concat(smoothed_values, ignore_index=True)
    
    # Pivoter pour avoir une colonne par année (smoothed) indexée par day_month
    pivot_table = df_smoothed.pivot_table(
        index='day_month',
        columns='year',
        values='smoothed',
        aggfunc='mean'  # au cas où doublons (normalement pas)
        )
    
    # Créer un index de dates pivot (2000) pour l'axe X
    pivot_table['plot_date'] = pd.to_datetime('2000-' + pivot_table.index)
    pivot_table = pivot_table.sort_values('plot_date')
    
    # Calculer min et max par jour (sur les années)
    pivot_table['min'] = pivot_table.drop(columns='plot_date').min(axis=1)
    pivot_table['max'] = pivot_table.drop(columns='plot_date').max(axis=1)
    
    # --- Tracer ---
    plt.figure(figsize=(14, 8))
    
    # Colorer la zone entre min et max
    plt.fill_between(
        pivot_table['plot_date'],
        pivot_table['min'],
        pivot_table['max'],
        color='lightblue',
        alpha=0.3,
        label='Min-Max zone'
        )
    
    # Tracer chaque année
    for year in pivot_table.columns:
        if year not in ['plot_date', 'min', 'max']:
            plt.plot(
                pivot_table['plot_date'],
                pivot_table[year],
                label=f'{col_value}_{year}',
                linewidth=2
                )
    
    # Formater l'axe X
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.xticks(rotation=45, ha='right')
    
    # Style
    title = f'Évolution saisonnière lissée de "{col_value}"'
    if zone:
        title += f' (Zone: {zone})'
    if factor:
        title += f' (Opérateur: {factor})'
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Jour de l\'année', fontsize=12)
    plt.ylabel(col_value, fontsize=12)
    plt.legend(title='Année', loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()



def graph_trend(df, var):
    # Style seaborn
    sns.set_style("whitegrid")
    plt.rcParams["figure.figsize"] = (14, 7)

    # Données
    x = df.index
    y = df[var]

    # Créer le graphique
    fig, ax = plt.subplots(1, 1)
    ax.plot(x, y, color='red', linewidth=1.5, label=var)
    ax.fill_between(x, y, color='red', alpha=0.1, edgecolor='red', linewidth=0)

    # Lignes verticales pour 2018 et 2022
    # ax.axvline(pd.Timestamp('2018-01-01'), color='gray', linestyle='--', linewidth=1.5, alpha=0.8, label='2018: Tension post-électorale')
    # ax.axvline(pd.Timestamp('2022-01-01'), color='gray', linestyle='--', linewidth=1.5, alpha=0.8, label='2022: Guerre Ukraine / Dé-dollarisation')

    # 6. Style
    ax.set_title('...', fontsize=16, weight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Evolution prix ...', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    # 8. Ajuster et sauvegarder
    plt.tight_layout()
    plt.show()