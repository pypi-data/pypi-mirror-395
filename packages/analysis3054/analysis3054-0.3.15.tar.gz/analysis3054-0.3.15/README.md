# Analysis3054 – Advanced Forecasting & Analytics

Analysis3054 is a full‑featured time‑series analytics and forecasting package designed for commodity, energy, and demand‑planning practitioners. It combines plotting, statistics, machine learning, and deep learning (Chronos‑2, AutoGluon, gradient boosting, SARIMAX, and more) under a single, unified API.

## Installation
Install the latest release (Chronos‑2 and AutoGluon are installed by default):

```bash
pip install analysis3054
```

Optional extras let you control footprint per environment:

```bash
pip install "analysis3054[stats]"    # pmdarima + arch
pip install "analysis3054[ml]"       # scikit-learn + boosted trees
pip install "analysis3054[dl]"       # tensorflow
pip install "analysis3054[prophet]"  # prophet + neuralprophet
pip install "analysis3054[tbats]"    # tbats
pip install "analysis3054[all]"      # everything (same as base but explicit)
```

## High-speed API ingestion
Pull many REST endpoints into a single pandas DataFrame with HTTP/2, pooled connections, and concurrent downloads. Save the result with your own filename in any directory:

```python
from analysis3054 import fetch_apis_to_dataframe

endpoints = [
    "https://api.example.com/v1/events",
    {"url": "https://api.example.com/v1/users", "params": {"page": 1}},
]

df = fetch_apis_to_dataframe(
    endpoints,
    max_workers=16,          # tune concurrency for more throughput
    output_dir="./exports",  # optional: write CSV next to your project
    file_name="daily_snapshot",
)
print(df.head())
```

The helper grows timeouts automatically when it encounters slow endpoints,
keeping the overall ingestion resilient without sacrificing speed for the fast
paths.

### Building for PyPI
From a clean checkout:

```bash
python -m build
```

This produces wheel and sdist artifacts under `dist/` ready for upload via `twine upload dist/*`.

## Quickstart
Create a small demo DataFrame (weekly power prices with a covariate):

```python
import numpy as np
import pandas as pd
from analysis3054 import (
    five_year_plot,
    ForecastEngine,
    forecast_distillate_burn,
    ml_forecast,
    chronos2_forecast,
    bayesian_ridge_forecast,
    huber_forecast,
    pls_forecast,
    fourier_ridge_forecast,
    histgb_direct_forecast,
)

rng = pd.date_range("2020-01-05", periods=120, freq="W")
df = pd.DataFrame({
    "date": rng,
    "price": 50 + np.sin(np.arange(120) / 6) * 5 + np.random.randn(120),
    "temp": 30 + np.random.randn(120),
})
```

## Plotting
### Five‑Year Band Plot
```python
fig = five_year_plot(date="date", df=df, smooth=True)
fig.show()
```

## Forecasting APIs
### Unified engine
```python
engine = ForecastEngine.default()
forecast = engine.run(
    df=df,
    date_col="date",
    target_cols=["price"],
    horizon=8,
    covariate_cols=["temp"],
)
print(forecast.forecasts.head())
```

### High‑level helper: distillate burn
```python
res = forecast_distillate_burn(
    df=df,
    date_col="date",
    target_col="price",
    covariate_cols=["temp"],
    prediction_length=6,
    method="chronos2",
)
```

### Chronos‑2 direct use
```python
chronos_out = chronos2_forecast(
    df=df,
    date_col="date",
    target_col="price",
    covariate_cols=["temp"],
    prediction_length=12,
    model_name="amazon/chronos-2",
)
```

#### Chronos‑2 presets for every user
Each preset keeps the arguments to a minimum and mirrors everyday language so non‑Python users can follow along.

*Univariate (one series, no extra inputs)*
```python
from analysis3054 import chronos2_univariate_forecast

quick = chronos2_univariate_forecast(
    df,
    date_col="date",        # your time column
    target_col="price",      # the number you want to predict
    prediction_length=7,       # how many future steps to create
)
print(quick.forecasts.head())
```

*Multivariate (many series side‑by‑side)*
```python
from analysis3054 import chronos2_multivariate_forecast

multi = chronos2_multivariate_forecast(
    df,
    date_col="date",
    target_cols=["north", "south", "west"],   # each column becomes its own forecast
    covariate_cols=["temp"],                    # optional shared drivers
    prediction_length=10,
)
print(multi.forecasts.columns)  # (series, quantile) pairs
```

*Covariate‑informed (future drivers provided)*
```python
from analysis3054 import chronos2_covariate_forecast

# known drivers for the forecast window (e.g., weather or calendar effects)
future_cov = pd.DataFrame({
    "date": pd.date_range(df["date"].max() + pd.Timedelta(days=1), periods=14, freq="D"),
    "temp": 60,
})

guided = chronos2_covariate_forecast(
    df,
    date_col="date",
    target_col="price",
    covariate_cols=["temp"],
    future_cov_df=future_cov,
    prediction_length=14,
)
guided.forecasts.tail()
```

## ML & Robust Forecasters
All ML helpers infer frequency, propagate covariates, apply exponential error correction, and handle missing sklearn gracefully.

```python
ridge = bayesian_ridge_forecast(df, date_col="date", target_col="price", covariate_cols=["temp"], prediction_length=10)
huber = huber_forecast(df, date_col="date", target_col="price", covariate_cols=["temp"], prediction_length=10)
pls = pls_forecast(df, date_col="date", target_col="price", covariate_cols=["temp"], prediction_length=10)
fourier = fourier_ridge_forecast(df, date_col="date", target_col="price", covariate_cols=["temp"], prediction_length=10, seasonal_periods=[52])
histgb = histgb_direct_forecast(df, date_col="date", target_col="price", covariate_cols=["temp"], prediction_length=10, max_depth=4)
```

### Auto ML family (10+ helpers)
```python
from analysis3054 import (
    chronos2_auto_covariate_forecast,
    boosted_tree_forecast,
    random_forest_forecast,
    elastic_net_forecast,
    xgboost_forecast,
    catboost_forecast,
    lightgbm_forecast,
    svr_forecast,
    mlp_forecast,
    harmonic_regression_forecast,
    intraday_sarimax_forecast,
)

auto = chronos2_auto_covariate_forecast(df, "date", "price", covariate_cols=["temp"], prediction_length=6)
boosted = boosted_tree_forecast(df, "date", "price", covariate_cols=["temp"], prediction_length=6)
```

### Leaderboards & Ensembles
```python
from analysis3054 import model_leaderboard, simple_ensemble

leaderboard = model_leaderboard(df, "date", "price", covariate_cols=["temp"], prediction_length=8, models=["chronos2", "sarimax", "harmonic"])
ensemble = simple_ensemble(df, "date", "price", covariate_cols=["temp"], prediction_length=8, models=["chronos2", "harmonic"], weights=[0.7, 0.3])
```

## Additional Utilities
* `ml_forecast`: AutoGluon multiseries forecaster with optional quantiles.
* `forecast_engine`: Registry for plugging in custom model handlers.
* `forecast_distillate_burn`: Sector‑specific helper with automatic Chronos‑2 routing.
* `statistics.py` / `stats.py`: stationarity tests, autocorrelation utilities.
* `plot.py` / `visualization.py`: distribution, correlation, and seasonal plots.
* `finance.py`: Sharpe ratio, drawdown analytics, and return attribution.

Refer to `USER_GUIDE.md` for end‑to‑end walkthroughs, troubleshooting tips, and extended examples spanning every public function.
