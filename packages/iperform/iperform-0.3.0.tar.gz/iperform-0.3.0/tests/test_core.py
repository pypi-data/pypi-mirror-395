import pytest
import pandas as pd
import numpy as np
import math
from datetime import datetime
from iperform.core import (
    dday,
    wtd, mtd, qtd, htd, ytd,
    full_w, full_m, full_q, full_h, full_y,
    forecast_m,
    c_rate,
    get_summary_day, get_summary_month, get_summary_quarter
    )

# -------------------------------------------------------------------------------
# DATASET
# -------------------------------------------------------------------------------

@pytest.fixture

def sample_df():
    """DataFrame simple avec des revenus journaliers pour un mois """
    np.random.seed(1234) 
    dates = pd.date_range('2023-01-01', periods=565, freq="D")
    revenu = np.random.uniform(30, 55, size=565)
    df = pd.DataFrame({
        "date": dates,
        "revenu": revenu,
        "user_actif": np.random.randint(950, 1050, size=565),
        "zone": "all_zone",
        "factor": "Orange" 
    })
    return df

@pytest.fixture

def sample_df_cumul():
    """DataFrame avec série cumulée (ex: base clients)."""
    dates = pd.date_range("2023-01-01", periods=565, freq="D")
    base_clients = 1000 + np.cumsum(np.random.randint(-10, 20, size=565))  # fluctue autour de 1000
    df = pd.DataFrame({
        "date": dates,
        "user_actif": base_clients,
        "zone": "all_zone",
        "factor": "Orange"
    })
    return df


# -------------------------------------------------------------------------------
# TESTS UNITAIRES
# -------------------------------------------------------------------------------

def test_dday_basic(sample_df):
    """Test basique de dday() - la valeur exacte à une date."""
    result = dday(
        df=sample_df,
        date='2023-01-15',
        value="revenu",
        d=0,
        zone="all_zone",
        factor="Orange",
        unite=1,
        decimal=2
    )
    assert isinstance(result, float)
    assert 30 <= result <= 55

def test_dday_not_found(sample_df):
    """Test quand la date n'existe pas."""
    result = dday(
        df=sample_df,
        date="2022-02-01",  # hors du DataFrame
        value="revenu",
        d=0
    )
    assert result is None

# -------------------------------------------------------------------------------

def test_wtd_flux(sample_df):
    """Test WTD pour une série de flux (somme)."""
    # 2023-01-09 est un lundi → semaine du 9 au 15 janvier
    result = wtd(
        df=sample_df,
        date="2023-01-10",  # mardi 10 janvier
        value="revenu",
        w=0,
        decimal=2,
        cumul=False
    )
    # Doit sommer du 9 au 10 janvier (2 jours)
    expected = sample_df[
        (sample_df['date'] >= "2023-01-09") &
        (sample_df['date'] <= "2023-01-10")
    ]['revenu'].sum()
    assert round(result, 2) == round(expected, 2)


def test_wtd_cumul(sample_df_cumul):
    """Test WTD pour une série cumulée (prend la valeur du jour)."""
    result = wtd(
        df=sample_df_cumul,
        date="2023-01-10",
        value="user_actif",
        w=0,
        cumul=True
    )
    expected = sample_df_cumul[sample_df_cumul['date'] == "2023-01-10"]['user_actif'].iloc[0]
    assert result == round(expected, 0)

# -------------------------------------------------------------------------------

def test_mtd_flux(sample_df):
    """Test MTD pour une série de flux (somme du 1er au jour)."""
    result = mtd(
        df=sample_df,
        date="2023-01-10",
        value="revenu",
        m=0,
        decimal=2,
        cumul=False
    )
    expected = sample_df[
        (sample_df['date'] >= "2023-01-01") &
        (sample_df['date'] <= "2023-01-10")
    ]['revenu'].sum()
    assert round(result, 2) == round(expected, 2)


# -------------------------------------------------------------------------------

def test_full_m_flux(sample_df):
    """Test full_m() - somme sur tout le mois de janvier."""
    result = full_m(
        df=sample_df,
        date="2023-01-15",
        value="revenu",
        m=0,
        decimal=0,
        cumul=False
    )
    expected = sample_df[(sample_df['date'] >= "2023-01-01") & 
                         (sample_df['date'] <= "2023-01-31")]['revenu'].sum()
    assert round(result, 0) == round(expected, 0)


# -------------------------------------------------------------------------------

def test_forecast_m_basic(sample_df):
    """Test forecast_m() - projection linéaire."""
    result = forecast_m(
        data=sample_df,
        date="2023-01-15",  # 15 jours passés → 16 restants
        value="revenu",
        decimal=0,
        cumul=False
        )
    mtd_val = sample_df[
        (sample_df['date'] >= "2023-01-01") &
        (sample_df['date'] <= "2023-01-15")
    ]['revenu'].sum()
    daily_avg = mtd_val / 15
    expected = mtd_val + (daily_avg * 16)  # 31 jours en janvier
    assert round(result, 0) == round(expected, 0)


# -------------------------------------------------------------------------------

def test_get_summary_day_basic(sample_df):
    """Test get_summary_day() - retourne une liste de 8 valeurs."""
    result = get_summary_day(
        df=sample_df,
        date="2023-02-15",
        zone="all_zone",
        factor="Orange",
        devise="USD",
        value="revenu",
        unit=1
        )
    assert len(result) == 8
    assert all(isinstance(x, (float, int, type(None))) for x in result)
    # Vérifie que la valeur courante est dans la plage
    assert 30 <= result[2] <= 55


# -------------------------------------------------------------------------------

def test_get_summary_month_basic(sample_df):
    """Test get_summary_month() - retourne une liste de 8 valeurs."""
    result = get_summary_month(
        df=sample_df,
        date="2024-04-30",
        zone="all_zone",
        factor="Orange",
        devise="USD",
        value="revenu",
        unit=1
    )
    assert len(result) == 8
    assert all(isinstance(x, (float, int, type(None))) for x in result)
    # Vérifie que le mois courant est la somme de janvier
    expected = sample_df[(sample_df['date'] >= '2024-04-01') &
                         (sample_df['date'] <= '2024-04-30')]['revenu'].sum()
    assert round(result[2], 0) == round(expected, 0)


def test_get_summary_month_cumul(sample_df_cumul):
    """Test get_summary_month() - avec argument cumul=True."""
    result = get_summary_month(
        df=sample_df_cumul,
        date="2024-04-30",
        zone="all_zone",
        factor="Orange",
        value="user_actif",
        cumul=True
    )
    expected = sample_df_cumul[sample_df_cumul["date"]=="2024-04-30"]["user_actif"].iloc[0]
    assert round(result[2], 0) == round(expected, 0)


# -------------------------------------------------------------------------------

def test_c_rate(sample_df):

    """Teste la fonction delta() avec le sample_df existant."""
    # Extraire des valeurs réelles de sample_df
    # Ex: Comparer février 2024 (29j, bissextile) vs janvier 2024 (31j)
    fev_2024 = sample_df[(sample_df['date'] >= '2024-02-01') & (sample_df['date'] <= '2024-02-29')]
    jan_2024 = sample_df[(sample_df['date'] >= '2024-01-01') & (sample_df['date'] <= '2024-01-31')]
    
    x_val = fev_2024['revenu'].sum()  # Total février
    y_val = jan_2024['revenu'].sum()  # Total janvier

    # 1. Test mode absolu avec y=0 → doit fonctionner
    result_abs_zero = c_rate(x=100, y=0, abs=True, decimal=2)
    assert result_abs_zero == 100.00

    # 2. Test mode relatif avec y=0 → doit retourner None
    result_rel_zero = c_rate(x=100, y=0, abs=False, decimal=2)
    assert result_rel_zero is None

    # 3. Test normalisation : comparer février (29j) vs janvier (31j), ramené à 30j
    #   → Si les revenus sont proportionnels aux jours, la variation devrait être ~0
    result_norm = c_rate(
        x=x_val, y=y_val,
        abs=False,
        nx=29, ny=31, nn=30,
        decimal=3
        )
    # On ne peut pas prédire la valeur exacte (données aléatoires),
    # mais on vérifie que c'est un float et pas None
    assert isinstance(result_norm, (float, int))

    # 4. Test arrondi
    result_round = c_rate(x=100, y=30, abs=False, decimal=1)
    expected = round((100 / 30) - 1, 1)  # ≈ 2.333 → 2.3
    assert result_round == expected

    # 5. Test mode absolu normalisé
    result_abs_norm = c_rate(
        x=x_val, y=y_val,
        abs=True,
        nx=29, ny=31, nn=30,
        decimal=2
        )
    assert isinstance(result_abs_norm, (float, int))



# -------------------------------------------------------------------------------
# TESTS DE VALIDATION
# -------------------------------------------------------------------------------

def test_dday_missing_column():
    """Test que dday lève une erreur si la colonne 'date' est manquante."""
    df = pd.DataFrame({"x": [1, 2, 3]})
    with pytest.raises(ValueError, match="La colonne 'date' est manquante"):
        dday(df=df, date="2023-01-01", value="x")


def test_dday_invalid_date_format():
    """Test que dday gère mal un format de date invalide."""
    df = pd.DataFrame({"date": ["not-a-date"], "x": [1]})
    with pytest.raises(ValueError):
        dday(df=df, date="invalid-date", value="x")


# -------------------------------------------------------------------------------