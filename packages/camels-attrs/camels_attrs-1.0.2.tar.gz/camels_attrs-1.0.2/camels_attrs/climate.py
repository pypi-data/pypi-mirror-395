"""
Climate indices calculation from GridMET data
"""

import numpy as np
import pandas as pd
import pygridmet as gridmet
from scipy.optimize import curve_fit


def fetch_climate_data(watershed_geom, start_date="2000-01-01", end_date="2020-12-31"):
    """
    Fetch climate data from GridMET.
    
    Parameters
    ----------
    watershed_geom : shapely.geometry
        Watershed boundary
    start_date : str
        Start date (YYYY-MM-DD)
    end_date : str
        End date (YYYY-MM-DD)
    
    Returns
    -------
    xarray.Dataset
        Climate data with variables: tmmn, tmmx, tavg, pr, pet
    """
    try:
        variables = ["tmmn", "tmmx", "pr", "pet"]
        
        ds = gridmet.get_bygeom(
            geometry=watershed_geom,
            dates=(start_date, end_date),
            variables=variables,
            crs="EPSG:4326"
        )
        
        # Unit conversions
        ds['tmmn'] = ds['tmmn'] - 273.15  # K to °C
        ds['tmmx'] = ds['tmmx'] - 273.15  # K to °C
        ds['tavg'] = (ds['tmmn'] + ds['tmmx']) / 2
        
        return ds
        
    except Exception as e:
        raise Exception(f"Failed to fetch climate data: {str(e)}")


def compute_climate_indices(climate_ds):
    """
    Compute CAMELS-style climate indices.
    
    Parameters
    ----------
    climate_ds : xarray.Dataset
        Climate data from fetch_climate_data
    
    Returns
    -------
    dict
        Climate indices including:
        - p_mean, pet_mean, temp_mean
        - aridity, p_seasonality, temp_seasonality
        - frac_snow, high_prec_freq, high_prec_dur, etc.
    """
    try:
        # Basin-averaged time series
        tavg = climate_ds['tavg'].mean(dim=['lat', 'lon'])
        prcp = climate_ds['pr'].mean(dim=['lat', 'lon'])
        pet = climate_ds['pet'].mean(dim=['lat', 'lon'])
        
        # Basic statistics
        p_mean = float(prcp.mean())
        pet_mean = float(pet.mean())
        temp_mean = float(tavg.mean())
        
        # Aridity index
        aridity = pet_mean / p_mean if p_mean > 0 else np.inf
        
        # Seasonality
        seasonality_indices = compute_seasonality(
            tavg.values, prcp.values, climate_ds.time.values
        )
        
        # Snow fraction
        frac_snow = compute_snow_fraction(tavg.values, prcp.values)
        
        # Extreme precipitation
        extreme_precip = compute_extreme_precipitation_stats(
            prcp.values, climate_ds.time.values
        )
        
        climate_indices = {
            "p_mean": p_mean,
            "pet_mean": pet_mean,
            "temp_mean": temp_mean,
            "aridity": aridity,
            "p_seasonality": seasonality_indices["p_seasonality"],
            "temp_seasonality": seasonality_indices["temp_seasonality"],
            "frac_snow": frac_snow,
            "high_prec_freq": extreme_precip["high_prec_freq"],
            "high_prec_dur": extreme_precip["high_prec_dur"],
            "high_prec_timing": extreme_precip["high_prec_timing"],
            "low_prec_freq": extreme_precip["low_prec_freq"],
            "low_prec_dur": extreme_precip["low_prec_dur"],
            "low_prec_timing": extreme_precip["low_prec_timing"],
            "prec_intensity": extreme_precip["prec_intensity"],
        }
        
        return climate_indices
        
    except Exception as e:
        raise Exception(f"Failed to compute climate indices: {str(e)}")


def compute_seasonality(temp, prcp, dates):
    """Compute temperature and precipitation seasonality using sinusoidal regression."""
    try:
        dates_dt = pd.to_datetime(dates)
        doy = dates_dt.dayofyear.values
        
        # Temperature seasonality
        def sine_temp(day_of_year, delta_t, s_t):
            return delta_t * np.sin(2 * np.pi * (day_of_year - s_t) / 365.25)
        
        temp_detrended = temp - np.mean(temp)
        temp_params, _ = curve_fit(sine_temp, doy, temp_detrended, p0=[10, -90])
        
        # Precipitation seasonality
        def sine_prec(day_of_year, delta_p, s_p):
            return 1 + delta_p * np.sin(2 * np.pi * (day_of_year - s_p) / 365.25)
        
        prcp_normalized = prcp / np.mean(prcp) - 1
        prcp_params, _ = curve_fit(sine_prec, doy, prcp_normalized, p0=[0.4, 90])
        
        return {
            "temp_seasonality": temp_params[0],  # Temperature amplitude
            "p_seasonality": abs(prcp_params[0])  # Precipitation seasonality
        }
        
    except:
        return {"temp_seasonality": 0.0, "p_seasonality": 0.0}


def compute_snow_fraction(temp, prcp):
    """Estimate fraction of precipitation falling as snow (T < 0°C)."""
    try:
        snow_days = temp < 0
        total_prcp = np.sum(prcp)
        snow_prcp = np.sum(prcp[snow_days])
        return snow_prcp / total_prcp if total_prcp > 0 else 0.0
    except:
        return 0.0


def compute_extreme_precipitation_stats(prcp, dates):
    """Compute frequency, duration, and timing of extreme precipitation events."""
    try:
        dates_dt = pd.to_datetime(dates)
        years = dates_dt.year.unique()
        n_years = len(years)
        
        # High precipitation threshold (5x mean)
        high_threshold = 5 * np.mean(prcp)
        high_events = prcp >= high_threshold
        
        # Low precipitation threshold (< 1 mm/day)
        low_threshold = 1.0
        low_events = prcp < low_threshold
        
        # Calculate frequencies
        high_prec_freq = np.sum(high_events) / n_years
        low_prec_freq = np.sum(low_events) / n_years
        
        # Calculate durations
        high_prec_dur = calculate_mean_duration(high_events)
        low_prec_dur = calculate_mean_duration(low_events)
        
        # Calculate timing (day of year)
        high_prec_timing = np.mean(dates_dt.dayofyear[high_events]) if np.any(high_events) else 0
        low_prec_timing = np.mean(dates_dt.dayofyear[low_events]) if np.any(low_events) else 0
        
        # Precipitation intensity
        prec_intensity = np.mean(prcp[prcp > 0]) if np.any(prcp > 0) else 0
        
        return {
            "high_prec_freq": high_prec_freq,
            "high_prec_dur": high_prec_dur,
            "high_prec_timing": high_prec_timing,
            "low_prec_freq": low_prec_freq,
            "low_prec_dur": low_prec_dur,
            "low_prec_timing": low_prec_timing,
            "prec_intensity": prec_intensity,
        }
        
    except:
        return {
            "high_prec_freq": 0, "high_prec_dur": 0, "high_prec_timing": 0,
            "low_prec_freq": 0, "low_prec_dur": 0, "low_prec_timing": 0,
            "prec_intensity": 0
        }


def calculate_mean_duration(mask):
    """Calculate mean duration of consecutive True values in boolean mask."""
    lengths = []
    run = 0
    for v in mask:
        if v:
            run += 1
        elif run > 0:
            lengths.append(run)
            run = 0
    if run > 0:
        lengths.append(run)
    return np.mean(lengths) if lengths else 0
