import numpy as np
import pandas as pd
import os


# ============================================================
# 1. SOLAR ACTUAL GENERATION FUNCTION
# ============================================================
def generate_solar_actual(save_path="solar_actual.csv", seed=42):
    """
    Generates 8760 hourly solar actual data using:
    - smooth diurnal sinusoidal curve
    - realistic amplitude (~10.4 kW peak)
    - Gaussian cloud noise
    - final rescaling to exactly match Table I statistics

    Saves CSV with column 'solar_actual_kw'
    """
    np.random.seed(seed)

    hours = np.arange(8760)
    hour_of_day = hours % 24

    # 1. Solar diurnal curve (sunrise ~6, sunset ~18)
    base_curve = np.sin(np.pi * (hour_of_day - 6) / 12)
    base_curve = np.clip(base_curve, 0, None)

    # 2. Seasonal modifier (mild, tropical)
    day_of_year = (hours // 24) % 365
    seasonal_factor = 1 + 0.15 * np.sin(2 * np.pi * (day_of_year - 80) / 365)

    # 3. Raw solar generation before noise
    solar_raw = base_curve * seasonal_factor * 10.4  # peak ≈ 10.4 kW

    # 4. Cloud noise
    noise = np.random.normal(0, 1.2, size=8760)
    solar_noisy = np.clip(solar_raw + noise, 0, None)

    # 5. FORCE MATCH THE EXACT STATISTICS FROM TABLE I
    target_mean = 3.472
    target_std = 3.929
    target_min = 0.0
    target_max = 10.386

    # Standardize → scale → shift
    z = (solar_noisy - solar_noisy.mean()) / (solar_noisy.std() + 1e-9)
    solar_scaled = z * target_std + target_mean

    # Clip to forced min and max
    solar_final = np.clip(solar_scaled, target_min, target_max)

    df = pd.DataFrame({"solar_actual_kw": solar_final})
    df.to_csv(save_path, index=False)
    return df



# ============================================================
# 2. SOLAR FORECAST GENERATION FUNCTION
# ============================================================
def generate_solar_forecast(solar_actual_path="solar_actual.csv",
                            save_path="solar_forecast.csv",
                            seed=43):
    """
    Generates solar forecast data using:
    - the actual solar data
    - Gaussian forecast-error noise
    - final rescaling to exactly match Table I statistics

    Saves CSV with column 'solar_forecast_kw'
    """
    np.random.seed(seed)

    # Load actual solar first
    solar_actual = pd.read_csv(solar_actual_path)["solar_actual_kw"].values

    # Gaussian forecast errors (paper says "controlled noise")
    forecast_noise = np.random.normal(0.3, 1.4, size=8760)
    forecast_raw = solar_actual + forecast_noise

    # Force Table I stats
    target_mean = 3.617
    target_std = 3.856
    target_min = 0.0
    target_max = 11.611

    z = (forecast_raw - forecast_raw.mean()) / (forecast_raw.std() + 1e-9)
    forecast_scaled = z * target_std + target_mean
    forecast_final = np.clip(forecast_scaled, target_min, target_max)

    df = pd.DataFrame({"solar_forecast_kw": forecast_final})
    df.to_csv(save_path, index=False)
    return df



# ============================================================
# 3. LOAD DEMAND GENERATION FUNCTION
# ============================================================
def generate_load_demand(save_path="load_demand.csv", seed=44):
    """
    Generates load demand using:
    - low early morning
    - two Gaussian peaks (morning + evening)
    - mild seasonal variation
    - final rescaling to match Table I exactly

    Saves CSV with column 'load_kw'
    """
    np.random.seed(seed)

    hours = np.arange(8760)
    hour_of_day = hours % 24

    # Two Gaussian peaks:
    def gaussian(h, mu, sigma, amp):
        return amp * np.exp(-0.5 * ((h - mu) / sigma)**2)

    morning = gaussian(hour_of_day, mu=8, sigma=2, amp=1)
    evening = gaussian(hour_of_day, mu=19, sigma=2.5, amp=1.2)

    base_load_shape = morning + evening + 0.4

    # Seasonal effect
    day_of_year = (hours // 24) % 365
    seasonal_factor = 1 + 0.05 * np.sin(2 * np.pi * (day_of_year - 150) / 365)

    load_raw = base_load_shape * seasonal_factor * 5.5

    # Random noise
    noise = np.random.normal(0, 0.3, size=8760)
    load_noisy = load_raw + noise

    # Force Table I statistics
    target_mean = 6.048
    target_std = 0.955
    target_min = 4.519
    target_max = 7.853

    z = (load_noisy - load_noisy.mean()) / (load_noisy.std() + 1e-9)
    load_scaled = z * target_std + target_mean
    load_final = np.clip(load_scaled, target_min, target_max)

    df = pd.DataFrame({"load_kw": load_final})
    df.to_csv(save_path, index=False)
    return df

# ============================================================
# 4. BATTERY SOC GENERATION FUNCTION (PAPER-ALIGNED)
# ============================================================
def generate_battery_soc(save_path="battery_soc.csv", seed=45):
    """
    Generates realistic battery State of Charge (SOC) data:
    - SOC bounded in [0, 100]
    - Mean ≈ 50
    - Std ≈ 20
    - Smooth variations (physical realism)
    - Matches paper constraint logic

    Saves CSV with column 'battery_soc'
    """
    np.random.seed(seed)

    hours = np.arange(8760)

    # Random walk SOC simulation
    soc = np.zeros(8760)
    soc[0] = 50  # paper initial SOC

    for t in range(1, 8760):
        step = np.random.choice([-20, -10, 0, 10, 20])
        soc[t] = soc[t-1] + step

    # Force bounds
    soc = np.clip(soc, 0, 100)

    # Force target distribution
    target_mean = 50.0
    target_std = 20.0
    target_min = 0.0
    target_max = 100.0

    z = (soc - soc.mean()) / (soc.std() + 1e-9)
    soc_scaled = z * target_std + target_mean
    soc_final = np.clip(soc_scaled, target_min, target_max)

    df = pd.DataFrame({"battery_soc": soc_final})
    df.to_csv(save_path, index=False)
    return df


# ============================================================
# 5. FINAL MICROGRID DATASET COMBINER
# ============================================================
def generate_final_microgrid_dataset(
    solar_actual_path="solar_actual.csv",
    solar_forecast_path="solar_forecast.csv",
    load_path="load_demand.csv",
    soc_path="battery_soc.csv",
    save_path="final_microgrid_dataset.csv"
):
    """
    Combines:
    - solar_actual_kw
    - solar_forecast_kw
    - load_kw
    - battery_soc
    - hour

    Into ONE CSV for direct DQN training
    """

    solar_actual = pd.read_csv(solar_actual_path)
    solar_forecast = pd.read_csv(solar_forecast_path)
    load = pd.read_csv(load_path)
    soc = pd.read_csv(soc_path)

    hours = np.arange(8760)

    final_df = pd.DataFrame({
        "hour": hours,
        "solar_actual_kw": solar_actual.iloc[:, 0],
        "solar_forecast_kw": solar_forecast.iloc[:, 0],
        "load_kw": load.iloc[:, 0],
        "battery_soc": soc.iloc[:, 0]
    })

    final_df.to_csv(save_path, index=False)
    return final_df

