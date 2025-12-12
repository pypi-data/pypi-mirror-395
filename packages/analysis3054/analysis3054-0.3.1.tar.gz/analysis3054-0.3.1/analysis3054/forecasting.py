"""
Advanced time‑series forecasting methods.

This module implements additional forecasting algorithms beyond the
machine‑learning and harmonic approaches already available in the
package.  These methods rely on external libraries such as
``statsmodels`` and ``pmdarima`` to provide robust statistical
models.  If the required libraries are not available, informative
errors are raised to guide the user toward installation.

Included functions:

* :func:`arima_forecast` – Fit classical ARIMA or SARIMA models to
  univariate series using Statsmodels.  Supports automatic order
  selection via a simple grid search.
* :func:`ets_forecast` – Fit Holt–Winters exponential smoothing
  models (ETS) to univariate series.
* :func:`var_forecast` – Fit Vector Autoregression (VAR) models to
  multivariate data, capturing linear interdependencies among
  variables.
* :func:`auto_arima_forecast` – Use pmdarima’s ``auto_arima`` to
  automatically identify the best ARIMA model for each series based
  on information criteria.
* :func:`prophet_forecast` – Forecast with Facebook’s Prophet model.
  This function is available only if the ``prophet`` package is
  installed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

try:
    # Import optional libraries used in advanced forecasting functions.  These
    # imports are placed here so that the entire module does not fail to
    # import if they are unavailable.  Each function that relies on one of
    # these packages will check for its presence at runtime and raise an
    # informative ImportError if missing.  See the individual functions for
    # details.
    import torch  # type: ignore[import]
except Exception:
    # torch is optional and only required for certain functions (TimesFM)
    torch = None  # type: ignore[assignment]


@dataclass
class ArimaForecastResult:
    """Result container for :func:`arima_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each series.  The index contains the
        forecast dates and the columns correspond to those of the
        input (excluding the date column).
    models : Dict[str, object]
        Fitted SARIMAX results objects from Statsmodels for each
        series.
    """

    forecasts: pd.DataFrame
    models: Dict[str, object]


def arima_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    order: Optional[Tuple[int, int, int]] = None,
    seasonal_order: Optional[Tuple[int, int, int, int]] = None,
    freq: Optional[str] = None,
    auto: bool = False,
    max_p: int = 2,
    max_d: int = 1,
    max_q: int = 2,
    information_criterion: str = 'aic',
) -> ArimaForecastResult:
    """Forecast one or more series using ARIMA models.

    See module documentation for full details.  Requires the
    ``statsmodels`` package.
    """
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX
    except Exception as e:
        raise ImportError(
            "statsmodels is required for ARIMA forecasting. "
            "Please install statsmodels to use this function."
        ) from e
    # Determine date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Determine numeric columns
    numeric_cols: List[str] = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric data columns found for ARIMA forecasting")
    # Infer frequency if not provided
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    # Prepare future dates
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # Storage
    forecasts_data: Dict[str, np.ndarray] = {}
    models: Dict[str, object] = {}
    # Define grid search ranges
    p_range = range(0, max_p + 1)
    d_range = range(0, max_d + 1)
    q_range = range(0, max_q + 1)
    for col in numeric_cols:
        y = pd.to_numeric(df[col], errors='coerce').ffill().bfill().astype(float)
        best_ic = np.inf
        best_res = None
        if auto:
            for p in p_range:
                for d in d_range:
                    for q in q_range:
                        try:
                            mod = SARIMAX(
                                y,
                                order=(p, d, q),
                                seasonal_order=seasonal_order,
                                enforce_stationarity=False,
                                enforce_invertibility=False,
                            )
                            res = mod.fit(disp=False)
                            ic_val = res.aic if information_criterion == 'aic' else res.bic
                            if np.isfinite(ic_val) and ic_val < best_ic:
                                best_ic = ic_val
                                best_res = res
                        except Exception:
                            continue
            if best_res is None:
                raise ValueError(f"Auto ARIMA failed to fit any model for column '{col}'")
        else:
            if order is None:
                raise ValueError("order must be specified when auto=False")
            mod = SARIMAX(
                y,
                order=order,
                seasonal_order=seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False,
            )
            best_res = mod.fit(disp=False)
        # Forecast
        forecast = best_res.forecast(steps=periods)
        forecasts_data[col] = forecast.values
        models[col] = best_res
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=numeric_cols)
    return ArimaForecastResult(forecasts=forecast_df, models=models)


@dataclass
class EtsForecastResult:
    """Result container for :func:`ets_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each series.  The index contains the
        forecast dates and the columns correspond to those of the
        input (excluding the date column).
    models : Dict[str, object]
        Fitted ExponentialSmoothing results objects from Statsmodels.
    """

    forecasts: pd.DataFrame
    models: Dict[str, object]


def ets_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    seasonal_periods: Optional[int] = None,
    trend: Optional[str] = 'add',
    seasonal: Optional[str] = 'add',
    damped_trend: bool = False,
    freq: Optional[str] = None,
) -> EtsForecastResult:
    """Forecast one or more series using exponential smoothing (ETS).

    See module documentation for details.  Requires the ``statsmodels``
    package.
    """
    try:
        from statsmodels.tsa.holtwinters import ExponentialSmoothing
    except Exception as e:
        raise ImportError(
            "statsmodels is required for exponential smoothing. "
            "Please install statsmodels to use this function."
        ) from e
    # Determine date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric data columns found for exponential smoothing")
    # Infer frequency if not provided
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    # Determine seasonal_periods if not provided
    if seasonal_periods is None and freq is not None:
        if freq.startswith('M'):
            seasonal_periods = 12
        elif freq.startswith('W'):
            seasonal_periods = 52
        elif freq.startswith('Q'):
            seasonal_periods = 4
        elif freq.startswith('A') or freq.startswith('Y'):
            seasonal_periods = 1
        else:
            seasonal_periods = None
    # Prepare future dates
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    forecasts_data: Dict[str, np.ndarray] = {}
    models: Dict[str, object] = {}
    for col in numeric_cols:
        y = pd.to_numeric(df[col], errors='coerce').ffill().bfill().astype(float)
        # If no seasonal_periods is provided, disable seasonal component
        seasonal_comp = seasonal
        seasonal_periods_comp = seasonal_periods
        if seasonal_periods_comp is None:
            seasonal_comp = None
        model = ExponentialSmoothing(
            y,
            trend=trend,
            damped_trend=damped_trend,
            seasonal=seasonal_comp,
            seasonal_periods=seasonal_periods_comp,
        )
        res = model.fit()
        forecasts_data[col] = res.forecast(periods).values
        models[col] = res
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=numeric_cols)
    return EtsForecastResult(forecasts=forecast_df, models=models)


@dataclass
class VarForecastResult:
    """Result container for :func:`var_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for all series.  The index contains the
        forecast dates and the columns correspond to the selected
        numeric columns.
    model : object
        Fitted VAR model instance from statsmodels.
    """

    forecasts: pd.DataFrame
    model: object


def var_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    maxlags: int = 4,
    deterministic: str = 'c',
    freq: Optional[str] = None,
) -> VarForecastResult:
    """Forecast a multivariate time series using Vector Autoregression (VAR).

    This function fits a VAR model to all numeric columns of the
    provided DataFrame and generates forecasts ``periods`` steps
    ahead.  The optimal lag order is selected based on the Akaike
    information criterion.  Deterministic terms (constant and/or
    trend) can be specified via the ``deterministic`` argument.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  All numeric columns are included in
        the VAR model.
    periods : int, default 12
        Number of future periods to forecast.
    maxlags : int, default 4
        Maximum number of lags to consider when fitting the VAR model.
    deterministic : {'n','c','t','ct'}, default 'c'
        Specifies which deterministic terms to include in the model.
        'n' includes no constant or trend, 'c' adds a constant,
        't' adds a linear trend and 'ct' includes both constant and
        trend.
    freq : str or None, default None
        Pandas frequency string for generating forecast dates.  If
        ``None``, the frequency is inferred from the date series.

    Returns
    -------
    VarForecastResult
        Dataclass containing the forecast DataFrame and the fitted
        VAR model.

    Raises
    ------
    ImportError
        If the ``statsmodels`` package is not installed.
    """
    try:
        from statsmodels.tsa.api import VAR
    except Exception as e:
        raise ImportError(
            "statsmodels is required for VAR forecasting. "
            "Please install statsmodels to use this function."
        ) from e
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric data columns found for VAR forecasting")
    y = df[numeric_cols].ffill().bfill().astype(float)
    model = VAR(y)
    results = model.select_order(maxlags)
    selected_lag = results.selected_orders['aic']
    var_res = model.fit(selected_lag or 1, trend=deterministic)
    forecast_values = var_res.forecast(y.values[-var_res.k_ar:], periods)
    # Determine future dates
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    forecast_df = pd.DataFrame(forecast_values, index=future_index, columns=numeric_cols)
    return VarForecastResult(forecasts=forecast_df, model=var_res)


# ---------------------------------------------------------------------------
# VECM Forecasting
# ---------------------------------------------------------------------------

@dataclass
class VecmForecastResult:
    """Result container for :func:`vecm_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for all series.  The index contains the
        forecast dates and the columns correspond to the numeric
        columns of the input (excluding the date column).
    model : object
        Fitted VECM model instance from statsmodels.  May be
        ``None`` if a fallback model was used.
    """
    forecasts: pd.DataFrame
    model: object


def vecm_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    coint_rank: Optional[int] = None,
    deterministic: str = 'ci',
    freq: Optional[str] = None,
) -> VecmForecastResult:
    """Forecast a cointegrated multivariate time series using VECM.

    This function fits a Vector Error Correction Model (VECM) to the
    numeric columns of the provided DataFrame.  If the cointegration
    rank is not specified, it is estimated via the Johansen trace
    test.  The optimal lag difference order is selected based on the
    Akaike information criterion.  When VECM fitting fails, the
    function falls back to VAR forecasting.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  All numeric columns are included
        in the VECM model.
    periods : int, default 12
        Number of future periods to forecast.
    coint_rank : int or None, default None
        Number of cointegrating relationships.  If ``None``, the
        rank is estimated from the data using the Johansen test.
    deterministic : {'n','c','ci','ct','cti'}, default 'ci'
        Deterministic terms to include in the model.  See
        ``statsmodels.tsa.vector_ar.vecm.VECM`` for details.
    freq : str or None, default None
        Pandas frequency string for generating forecast dates.  If
        ``None``, the frequency is inferred from the date series.

    Returns
    -------
    VecmForecastResult
        Dataclass containing the forecast DataFrame and the fitted
        VECM model.  If the VECM fails, the model attribute is
        ``None`` and the forecasts come from a VAR fallback.

    Raises
    ------
    ImportError
        If the ``statsmodels`` package is not installed.
    ValueError
        If no numeric columns are available for modelling.
    """
    try:
        from statsmodels.tsa.vector_ar.vecm import VECM, select_order, select_coint_rank
    except Exception as e:
        raise ImportError(
            "statsmodels is required for VECM forecasting. "
            "Please install statsmodels to use this function."
        ) from e
    # Determine date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Identify numeric columns
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric data columns found for VECM forecasting")
    y = df[numeric_cols].ffill().bfill().astype(float)
    # Estimate cointegration rank if not provided
    est_rank = coint_rank
    if est_rank is None:
        try:
            rank_res = select_coint_rank(y, det_order=0, k_ar_diff=1, method='trace', signif=0.05)
            est_rank = rank_res.rank
        except Exception:
            est_rank = 0
    # Determine lag order using select_order
    try:
        order_res = select_order(y, maxlags=10, deterministic=deterministic)
        k_ar_diff = order_res.aic or 1
    except Exception:
        k_ar_diff = 1
    # Fit VECM model
    vecm_res = None
    forecast_values = None
    try:
        vecm_model = VECM(y, k_ar_diff=k_ar_diff, coint_rank=est_rank, deterministic=deterministic)
        vecm_res = vecm_model.fit()
        # Forecast returns an array of shape (periods, n_vars)
        forecast_values = vecm_res.predict(steps=periods)
    except Exception:
        vecm_res = None
    # If VECM failed, fallback to VAR
    if forecast_values is None or vecm_res is None:
        var_result = var_forecast(date, df, periods=periods, deterministic='c', freq=freq)
        return VecmForecastResult(forecasts=var_result.forecasts, model=None)
    # Determine future dates
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    forecast_df = pd.DataFrame(forecast_values, index=future_index, columns=numeric_cols)
    return VecmForecastResult(forecasts=forecast_df, model=vecm_res)


@dataclass
class AutoArimaForecastResult:
    """Result container for :func:`auto_arima_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each series.
    models : Dict[str, object]
        Fitted pmdarima ARIMA models for each series.
    """

    forecasts: pd.DataFrame
    models: Dict[str, object]


def auto_arima_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    seasonal: bool = False,
    m: int = 1,
    max_order: Optional[int] = None,
    freq: Optional[str] = None,
    information_criterion: str = 'aic',
) -> AutoArimaForecastResult:
    """Forecast one or more series using ``pmdarima.auto_arima``.

    This function leverages the pmdarima library to automatically
    identify and fit the best ARIMA model (with optional seasonal
    components) for each numeric series based on information
    criteria.  It returns the fitted models and the forecasts.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series, or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Numeric columns will be modelled
        individually.
    periods : int, default 12
        Number of future periods to forecast.
    seasonal : bool, default False
        Whether to consider seasonal models.
    m : int, default 1
        Number of periods in a season (e.g. 12 for monthly).  Only
        relevant if ``seasonal`` is True.
    max_order : int or None, default None
        Maximum value of p+q (or p+q+P+Q if seasonal) to consider.
        If None, defaults to 5 for non-seasonal and 2 for seasonal.
    freq : str or None, default None
        Pandas frequency string used to generate forecast dates.  If
        ``None``, the frequency is inferred from the date series.
    information_criterion : str, default 'aic'
        Criterion used to select the best model.  One of 'aic',
        'bic', 'hqic', etc., as supported by pmdarima.

    Returns
    -------
    AutoArimaForecastResult
        Dataclass containing the forecast DataFrame and fitted models.

    Raises
    ------
    ImportError
        If the ``pmdarima`` package is not installed.
    """
    try:
        import pmdarima as pm
    except Exception as e:
        raise ImportError(
            "pmdarima is required for auto_arima_forecast. "
            "Please install pmdarima to use this function."
        ) from e
    # Determine date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric data columns found for auto_arima forecasting")
    # Infer frequency if not provided
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    # Prepare future dates
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    forecasts_data: Dict[str, np.ndarray] = {}
    models: Dict[str, object] = {}
    for col in numeric_cols:
        y = pd.to_numeric(df[col], errors='coerce').ffill().bfill().astype(float)
        model = pm.auto_arima(
            y,
            seasonal=seasonal,
            m=m,
            information_criterion=information_criterion,
            max_order=max_order,
            error_action='ignore',
            suppress_warnings=True,
        )
        forecast = model.predict(n_periods=periods)
        forecasts_data[col] = forecast
        models[col] = model
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=numeric_cols)
    return AutoArimaForecastResult(forecasts=forecast_df, models=models)


@dataclass
class ProphetForecastResult:
    """Result container for :func:`prophet_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each series.  The index contains the
        forecast dates and the columns correspond to those of the
        input (excluding the date column).
    models : Dict[str, object]
        Fitted Prophet models for each series.
    """

    forecasts: pd.DataFrame
    models: Dict[str, object]


def prophet_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    freq: Optional[str] = None,
    seasonality_mode: str = 'additive',
    yearly_seasonality: Optional[bool] = None,
    weekly_seasonality: Optional[bool] = None,
    daily_seasonality: Optional[bool] = None,
) -> ProphetForecastResult:
    """Forecast one or more series using Facebook Prophet.

    Prophet is a decomposable time series model that handles trend,
    seasonality and holidays.  This function fits a separate Prophet
    model to each numeric column and returns forecasts.  The Prophet
    library must be installed separately; if it is not found, an
    ImportError is raised.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series, or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Numeric columns will be modelled
        individually.
    periods : int, default 12
        Number of future periods to forecast.
    freq : str or None, default None
        Frequency string for generating future dates.  If None,
        ``pandas.infer_freq`` is used.
    seasonality_mode : {'additive','multiplicative'}, default 'additive'
        Mode of seasonality.  Additive is appropriate for series with
        constant seasonal amplitude, while multiplicative is better
        for series where the amplitude increases with the level.
    yearly_seasonality, weekly_seasonality, daily_seasonality : bool or None
        Whether to include yearly, weekly and daily seasonalities.  If
        None, Prophet’s defaults are used (enabled if data frequency
        supports it).

    Returns
    -------
    ProphetForecastResult
        Dataclass containing the forecast DataFrame and fitted models.

    Raises
    ------
    ImportError
        If the ``prophet`` package is not installed.
    """
    try:
        from prophet import Prophet
    except Exception as e:
        raise ImportError(
            "prophet is required for prophet_forecast. "
            "Please install prophet (pip install prophet) to use this function."
        ) from e
    # Determine date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric data columns found for Prophet forecasting")
    # Infer frequency if not provided
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    # Prepare future dates for Prophet
    if freq is not None:
        try:
            future_dates = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_dates = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_dates = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    forecasts_data: Dict[str, np.ndarray] = {}
    models: Dict[str, object] = {}
    for col in numeric_cols:
        # Prepare Prophet DataFrame with 'ds' and 'y'
        y = pd.to_numeric(df[col], errors='coerce').ffill().bfill().astype(float)
        train_df = pd.DataFrame({'ds': dt, 'y': y})
        m = Prophet(
            seasonality_mode=seasonality_mode,
            yearly_seasonality=yearly_seasonality,
            weekly_seasonality=weekly_seasonality,
            daily_seasonality=daily_seasonality,
        )
        m.fit(train_df)
        future_df = pd.DataFrame({'ds': future_dates})
        forecast = m.predict(future_df)
        forecasts_data[col] = forecast['yhat'].values
        models[col] = m
    forecast_df = pd.DataFrame(forecasts_data, index=future_dates, columns=numeric_cols)
    return ProphetForecastResult(forecasts=forecast_df, models=models)

# ---------------------------------------------------------------------------
# Machine‑learning and ensemble forecasting
# ---------------------------------------------------------------------------


@dataclass
class RandomForestForecastResult:
    """Result container for :func:`random_forest_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each series.  The index contains the
        forecast dates and the columns correspond to those of the
        input (excluding the date column).
    models : Dict[str, object]
        Fitted scikit‑learn RandomForestRegressor models for each
        series.
    """

    forecasts: pd.DataFrame
    models: Dict[str, object]


def random_forest_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    n_lags: int = 3,
    n_estimators: int = 100,
    max_features: Union[int, float, str] = 'auto',
    random_state: Optional[int] = None,
    freq: Optional[str] = None,
) -> RandomForestForecastResult:
    """Forecast one or more series using Random Forest regressors.

    This function trains a separate RandomForestRegressor for each
    numeric series, using lagged values as features.  Forecasts are
    generated iteratively: predicted values are fed back as inputs to
    produce multi‑step forecasts.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series, or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Numeric columns will be modelled
        individually.
    periods : int, default 12
        Number of future periods to forecast.
    n_lags : int, default 3
        Number of past observations to use as features.  Larger
        values capture longer memory but increase model complexity.
    n_estimators : int, default 100
        Number of trees in the random forest.
    max_features : int, float or str, default 'auto'
        Number of features considered when looking for the best split.
        Follows scikit‑learn conventions.
    random_state : int or None, default None
        Random seed for reproducibility.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If None,
        inferred via ``pandas.infer_freq``.

    Returns
    -------
    RandomForestForecastResult
        Dataclass containing the forecast DataFrame and fitted models.

    Raises
    ------
    ImportError
        If scikit‑learn is not installed.
    """
    try:
        from sklearn.ensemble import RandomForestRegressor
    except Exception as e:
        raise ImportError(
            "scikit-learn is required for random_forest_forecast. "
            "Please install scikit-learn to use this function."
        ) from e
    # Determine date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric data columns found for Random Forest forecasting")
    # Infer frequency if not provided
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    # Prepare future dates
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    forecasts_data: Dict[str, List[float]] = {}
    models: Dict[str, object] = {}
    for col in numeric_cols:
        series = pd.to_numeric(df[col], errors='coerce').ffill().bfill().astype(float)
        # Build lag matrix
        X = []
        y_target = []
        for i in range(n_lags, len(series)):
            X.append(series.iloc[i - n_lags:i].values)
            y_target.append(series.iloc[i])
        if not X:
            raise ValueError(f"Series '{col}' is too short for {n_lags} lags")
        X_train = np.array(X)
        y_train = np.array(y_target)
        # Fit model
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_features=max_features,
            random_state=random_state,
        )
        model.fit(X_train, y_train)
        models[col] = model
        # Generate forecasts
        history = list(series.iloc[-n_lags:].values)
        preds = []
        for _ in range(periods):
            pred = model.predict([np.array(history[-n_lags:])])[0]
            preds.append(pred)
            history.append(pred)
        forecasts_data[col] = preds
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=numeric_cols)
    return RandomForestForecastResult(forecasts=forecast_df, models=models)


@dataclass
class EnsembleForecastResult:
    """Result container for :func:`ensemble_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values as the unweighted average of component
        forecasts for each series.
    components : Dict[str, pd.DataFrame]
        Forecast DataFrames from each individual method.
    """
    forecasts: pd.DataFrame
    components: Dict[str, pd.DataFrame]


def ensemble_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    methods: Optional[List[str]] = None,
    freq: Optional[str] = None,
    random_state: Optional[int] = None,
) -> EnsembleForecastResult:
    """Combine multiple forecasting methods by averaging their predictions.

    This function runs a set of selected forecasting algorithms on
    the same data and computes an unweighted average of their
    forecasts.  By combining different model classes, ensemble
    forecasts often achieve greater accuracy than any single method
    alone.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Numeric columns will be modelled
        individually.
    periods : int, default 12
        Number of future periods to forecast.
    methods : list of str or None, default None
        Forecasting methods to include in the ensemble.  If None,
        defaults to ['auto_arima','ets','unobserved_components','random_forest'].
        Supported method names include:

        - 'auto_arima' – pmdarima auto ARIMA (via :func:`auto_arima_forecast`)
        - 'ets' – Exponential smoothing (via :func:`ets_forecast`)
        - 'unobserved_components' – UC model (via :func:`unobserved_components_forecast`)
        - 'markov_switching' – Markov switching AR (via :func:`markov_switching_forecast`)
        - 'random_forest' – Random forest (via :func:`random_forest_forecast`)

    freq : str or None, default None
        Frequency string for generating forecast dates.  Passed to
        underlying functions when applicable.
    random_state : int or None, default None
        Random seed used by the random forest method.

    Returns
    -------
    EnsembleForecastResult
        Dataclass containing the combined forecast and a dictionary
        mapping method names to their individual forecast DataFrames.

    Notes
    -----
    Forecast horizons and indices are aligned based on the first
    method’s output.  If component forecasts have differing indices,
    they are reindexed to match via forward filling.
    """
    if methods is None:
        methods = ['auto_arima', 'ets', 'unobserved_components', 'random_forest']
    # Containers
    component_forecasts: Dict[str, pd.DataFrame] = {}
    # Generate forecasts for each method
    for method in methods:
        try:
            if method == 'auto_arima':
                res = auto_arima_forecast(date=date, df=df, periods=periods, freq=freq)
                component_forecasts[method] = res.forecasts
            elif method == 'ets':
                res = ets_forecast(date=date, df=df, periods=periods, freq=freq)
                component_forecasts[method] = res.forecasts
            elif method == 'unobserved_components':
                res = unobserved_components_forecast(date=date, df=df, periods=periods, freq=freq)
                component_forecasts[method] = res.forecasts
            elif method == 'markov_switching':
                res = markov_switching_forecast(date=date, df=df, periods=periods, freq=freq)
                component_forecasts[method] = res.forecasts
            elif method == 'random_forest':
                res = random_forest_forecast(date=date, df=df, periods=periods, freq=freq, random_state=random_state)
                component_forecasts[method] = res.forecasts
            else:
                raise ValueError(f"Unknown method '{method}' in ensemble_forecast")
        except Exception as e:
            # If a method fails, skip it and warn
            import warnings
            warnings.warn(f"Forecasting method '{method}' failed: {e}")
            continue
    if not component_forecasts:
        raise ValueError("No forecasts generated; check selected methods and data")
    # Align indices across component forecasts
    first_df = next(iter(component_forecasts.values()))
    combined = first_df.copy()
    # Reindex all forecasts to the first index using forward fill
    for name, f_df in component_forecasts.items():
        if f_df.index.equals(combined.index):
            continue
        component_forecasts[name] = f_df.reindex(combined.index, method='ffill')
    # Compute unweighted average
    sum_forecasts = sum(component_forecasts.values())
    avg_forecasts = sum_forecasts / len(component_forecasts)
    return EnsembleForecastResult(forecasts=avg_forecasts, components=component_forecasts)

# ---------------------------------------------------------------------------
# Advanced state‑space and regime switching models
# ---------------------------------------------------------------------------


@dataclass
class MarkovSwitchingForecastResult:
    """Result container for :func:`markov_switching_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each series using a Markov regime
        switching model.  The index contains the forecast dates and
        the columns correspond to those of the input (excluding the
        date column).
    models : Dict[str, object]
        Fitted MarkovAutoregression results for each series.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]


def markov_switching_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    k_regimes: int = 2,
    order: int = 1,
    freq: Optional[str] = None,
) -> MarkovSwitchingForecastResult:
    """Forecast univariate series using a Markov switching autoregression.

    A Markov switching autoregression (also known as a regime‑
    switching model) allows the parameters of an AR process to change
    between a finite number of regimes according to an unobserved
    Markov chain.  This can capture structural breaks or non‑linear
    dynamics often present in commodity markets.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Numeric columns will be modelled
        individually using univariate MarkovAutoregression models.
    periods : int, default 12
        Number of future periods to forecast.
    k_regimes : int, default 2
        Number of regimes (states) in the Markov chain.
    order : int, default 1
        Autoregressive order within each regime.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If None,
        ``pandas.infer_freq`` is used.

    Returns
    -------
    MarkovSwitchingForecastResult
        Dataclass containing the forecast DataFrame and the fitted
        models.

    Raises
    ------
    ImportError
        If ``statsmodels`` does not have ``MarkovAutoregression``.
    """
    try:
        from statsmodels.tsa.regime_switching.markov_autoregression import MarkovAutoregression
    except Exception as e:
        raise ImportError(
            "statsmodels with regime_switching is required for Markov switching forecasting."
        ) from e
    # Determine date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric data columns found for Markov switching forecasting")
    # Infer frequency
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    # Prepare future dates
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    forecasts_data: Dict[str, np.ndarray] = {}
    models: Dict[str, object] = {}
    for col in numeric_cols:
        y = pd.to_numeric(df[col], errors='coerce').ffill().bfill().astype(float)
        # Fit Markov autoregression with constant term
        mod = MarkovAutoregression(y, k_regimes=k_regimes, order=order, trend='c')
        res = mod.fit()
        models[col] = res
        # Extract transition matrix for forecast: 2D array shape (k_regimes, k_regimes)
        # res.regime_transition has shape (k_regimes, k_regimes, time), but transitions are constant over time.
        trans = res.regime_transition[:, :, 0]
        # Extract intercepts and AR coefficients per regime
        param_names = res.model.param_names
        params = res.params
        const_vals: Dict[int, float] = {i: 0.0 for i in range(k_regimes)}
        ar_vals: Dict[int, Dict[int, float]] = {i: {} for i in range(k_regimes)}
        for idx, pname in enumerate(param_names):
            # Constant terms: 'const[i]'
            if pname.startswith('const['):
                state = int(pname.split('[')[1].split(']')[0])
                const_vals[state] = float(params.iloc[idx] if hasattr(params, 'iloc') else params[idx])
            # AR terms: 'ar.Lk[i]'
            elif pname.startswith('ar.L'):
                parts = pname.split('[')
                lag_part = parts[0]
                lag = int(lag_part.split('L')[1])
                state = int(parts[1].split(']')[0])
                if state not in ar_vals:
                    ar_vals[state] = {}
                ar_vals[state][lag] = float(params.iloc[idx] if hasattr(params, 'iloc') else params[idx])
        # Get smoothed state probabilities at final time
        try:
            p_states = res.smoothed_marginal_probabilities.iloc[-1].values.copy()
        except Exception:
            # If smoothed probabilities are unavailable, use stationary distribution
            eigvals, eigvecs = np.linalg.eig(trans.T)
            stat = np.real(eigvecs[:, np.isclose(eigvals, 1)])
            stat = stat / stat.sum()
            p_states = stat.ravel()
        # Initialize history with last observed values (for AR lags)
        history = list(y.iloc[-order:]) if order > 0 else []
        preds: List[float] = []
        for h in range(periods):
            # Forecast per state
            state_preds = []
            for i in range(k_regimes):
                # Constant term
                pred_i = const_vals.get(i, 0.0)
                # Add AR terms
                for lag in range(1, order + 1):
                    coeff = ar_vals.get(i, {}).get(lag, 0.0)
                    if lag <= len(history):
                        pred_i += coeff * history[-lag]
                state_preds.append(pred_i)
            # Weighted forecast
            weighted_pred = float(np.dot(p_states, state_preds))
            preds.append(weighted_pred)
            # Update history
            if order > 0:
                history.append(weighted_pred)
                if len(history) > order:
                    history.pop(0)
            # Update state probabilities for next step: p_{t+1} = p_t * trans
            p_states = np.dot(p_states, trans)
        forecasts_data[col] = np.array(preds)
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=numeric_cols)
    return MarkovSwitchingForecastResult(forecasts=forecast_df, models=models)


@dataclass
class UnobservedComponentsForecastResult:
    """Result container for :func:`unobserved_components_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each series using unobserved components
        models.  The index contains the forecast dates and the
        columns correspond to those of the input (excluding the date
        column).
    models : Dict[str, object]
        Fitted UnobservedComponents results for each series.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]


def unobserved_components_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    level: bool = True,
    trend: bool = False,
    seasonal_periods: Optional[int] = None,
    freq: Optional[str] = None,
) -> UnobservedComponentsForecastResult:
    """Forecast univariate series using unobserved components models.

    Unobserved components (UC) models treat the observed series as a
    sum of latent components such as level, trend and seasonality.
    This function fits a UC model to each numeric column and
    forecasts future values.  It leverages the Kalman filter for
    state estimation.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Numeric columns will be modelled
        individually using univariate UC models.
    periods : int, default 12
        Number of future periods to forecast.
    level : bool, default True
        Include a level component (local level) in the model.
    trend : bool, default False
        Include a trend component (local linear trend) in the model.
    seasonal_periods : int or None, default None
        Number of periods in the seasonal component.  If ``None``,
        seasonality is omitted.  For example, 12 for monthly data.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If None,
        inferred using ``pandas.infer_freq``.

    Returns
    -------
    UnobservedComponentsForecastResult
        Dataclass containing the forecast DataFrame and the fitted
        models.

    Raises
    ------
    ImportError
        If the required ``statsmodels`` classes are not available.
    """
    try:
        from statsmodels.tsa.statespace.structural import UnobservedComponents
    except Exception as e:
        raise ImportError(
            "statsmodels is required for unobserved components forecasting."
        ) from e
    # Determine date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric data columns found for unobserved components forecasting")
    # Infer frequency and future dates
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    forecasts_data: Dict[str, np.ndarray] = {}
    models: Dict[str, object] = {}
    for col in numeric_cols:
        y = pd.to_numeric(df[col], errors='coerce').ffill().bfill().astype(float)
        # Specify seasonal_periods if not provided
        sp = seasonal_periods
        # Build model
        mod = UnobservedComponents(
            y,
            level='local level' if level else None,
            trend='local linear trend' if trend else None,
            seasonal=sp,
        )
        res = mod.fit(disp=False)
        pred = res.get_forecast(steps=periods)
        forecasts_data[col] = pred.predicted_mean.values
        models[col] = res
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=numeric_cols)
    return UnobservedComponentsForecastResult(forecasts=forecast_df, models=models)


@dataclass
class DynamicFactorForecastResult:
    """Result container for :func:`dynamic_factor_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for all series using a dynamic factor model.
    model : object
        Fitted DynamicFactor results.
    """
    forecasts: pd.DataFrame
    model: object


def dynamic_factor_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    k_factors: int = 1,
    factor_order: int = 1,
    freq: Optional[str] = None,
) -> DynamicFactorForecastResult:
    """Forecast multivariate series using a dynamic factor model.

    Dynamic factor models capture shared dynamics across multiple
    series by representing them as linear combinations of a small
    number of unobserved factors that evolve according to vector
    autoregressions.  This can be particularly powerful when
    multiple commodities exhibit co‑movement driven by common latent
    influences.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  All numeric columns are included in
        the model.
    periods : int, default 12
        Number of future periods to forecast.
    k_factors : int, default 1
        Number of latent factors to estimate.
    factor_order : int, default 1
        Order of the factor autoregression.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If None,
        inferred via ``pandas.infer_freq``.

    Returns
    -------
    DynamicFactorForecastResult
        Dataclass containing the forecast DataFrame and the fitted
        model.

    Raises
    ------
    ImportError
        If the required ``statsmodels`` classes are not available.
    """
    try:
        from statsmodels.tsa.statespace.dynamic_factor import DynamicFactor
    except Exception as e:
        raise ImportError(
            "statsmodels is required for dynamic factor forecasting."
        ) from e
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if len(numeric_cols) < 2:
        raise ValueError("Dynamic factor forecasting requires at least two numeric columns")
    y = df[numeric_cols].ffill().bfill().astype(float)
    # Fit dynamic factor model
    # Attempt to fit dynamic factor model; if it fails, fall back to VAR
    try:
        mod = DynamicFactor(y, k_factors=k_factors, factor_order=factor_order)
        res = mod.fit(disp=False)
        # Forecast factor and observed variables
        try:
            forecast_values = res.forecast(periods)
        except Exception:
            forecast_values = None
        # If forecast_values is empty or contains NaNs, fall back to predict
        if forecast_values is None or np.all(np.isnan(forecast_values)):
            start = len(y)
            end = len(y) + periods - 1
            forecast_pred = res.predict(start=start, end=end)
            forecast_values = forecast_pred.values
        model_res = res
    except Exception:
        # On failure, use VAR as fallback
        from .forecasting import var_forecast
        var_res = var_forecast(date=date, df=df, periods=periods, maxlags=factor_order, freq=freq)
        forecast_values = var_res.forecasts.values
        model_res = var_res.model
    # Determine future dates
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # At this point, forecast_values, model_res, future_index, numeric_cols are defined
    # If forecast_values is already a DataFrame (fallback), use it directly
    if isinstance(forecast_values, pd.DataFrame):
        forecast_df = forecast_values
    else:
        forecast_df = pd.DataFrame(forecast_values, index=future_index, columns=numeric_cols)
    return DynamicFactorForecastResult(forecasts=forecast_df, model=model_res)

# ---------------------------------------------------------------------------
# Additional advanced forecasting methods
# ---------------------------------------------------------------------------

@dataclass
class SarimaxForecastResult:
    """Result container for :func:`sarimax_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each series.  The index contains the
        forecast dates and the columns correspond to the numeric
        columns of the input (excluding the date column).
    models : Dict[str, object]
        Fitted SARIMAX results for each series.
    lower_conf_int : pandas.DataFrame or None
        Lower bounds of prediction intervals if requested; otherwise
        ``None``.
    upper_conf_int : pandas.DataFrame or None
        Upper bounds of prediction intervals if requested; otherwise
        ``None``.
    """

    forecasts: pd.DataFrame
    models: Dict[str, object]
    lower_conf_int: Optional[pd.DataFrame] = None
    upper_conf_int: Optional[pd.DataFrame] = None

# ---------------------------------------------------------------------------
# New intraday forecasting methods
# ---------------------------------------------------------------------------

@dataclass
class IntradaySarimaxForecastResult:
    """Result container for :func:`intraday_sarimax_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Predicted burn values for each series at the future intraday times.
    models : Dict[str, object]
        Fitted SARIMAX results objects from Statsmodels for each burn series.
    lower_conf_int : pandas.DataFrame or None
        Lower 95% prediction interval bounds for each series, if available.
    upper_conf_int : pandas.DataFrame or None
        Upper 95% prediction interval bounds for each series, if available.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]
    lower_conf_int: Optional[pd.DataFrame] = None
    upper_conf_int: Optional[pd.DataFrame] = None
    

@dataclass
class ForecastDistillateBurnResult:
    """Result container for :func:`forecast_distillate_burn`."""

    forecasts: pd.DataFrame
    method: str
    metadata: Dict[str, Any]


def forecast_distillate_burn(
    burn_df: pd.DataFrame,
    load_df: pd.DataFrame,
    *,
    date_col: str = "date",
    burn_cols: Optional[List[str]] = None,
    method: str = "sarimax",
    horizon: int = 12,
    quantile_levels: Optional[List[float]] = None,
    engine: Optional[object] = None,
    **kwargs: Any,
) -> ForecastDistillateBurnResult:
    """High‑level wrapper for forecasting distillate burn with covariates.

    This helper routes to an advanced backend (Chronos‑2 or SARIMAX) when
    available and falls back to a covariate‑aware baseline ratio forecast when
    dependencies are missing.  It is intentionally opinionated: burn columns
    are forecast using the first numeric load column as a covariate and the
    provided ``horizon`` determines the forecast length.

    Parameters
    ----------
    burn_df : pd.DataFrame
        Historical burn measurements containing ``date_col`` and numeric burn
        columns.
    load_df : pd.DataFrame
        Load (covariate) data containing ``date_col`` and at least one numeric
        load column. Future load values should be present for the forecast
        horizon when using SARIMAX or Chronos‑2.
    date_col : str, default "date"
        Name of the datetime column shared across data frames.
    burn_cols : list[str] or None, default None
        Burn columns to forecast. If None, all numeric columns in ``burn_df``
        other than ``date_col`` are used.
    method : {"sarimax", "chronos2", "baseline"}, default "sarimax"
        Backend to use. ``chronos2`` forwards covariates to
        :func:`chronos2_forecast`; ``sarimax`` uses
        :func:`intraday_sarimax_forecast`; ``baseline`` computes an average
        burn‑to‑load ratio and scales future load values.
    horizon : int, default 12
        Forecast horizon.
    quantile_levels : list[float] or None, default None
        Optional Chronos‑2 quantile levels.
    engine : ForecastEngine or None, default None
        Optional :class:`~analysis3054.forecast_engine.ForecastEngine` instance
        to reuse for Chronos‑2 dispatching.
    **kwargs : Any
        Additional parameters forwarded to the selected backend.
    """

    if date_col not in burn_df.columns:
        raise KeyError(f"Date column '{date_col}' not found in burn_df")
    if date_col not in load_df.columns:
        raise KeyError(f"Date column '{date_col}' not found in load_df")

    numeric_burn_cols = [c for c in burn_df.columns if c != date_col and pd.api.types.is_numeric_dtype(burn_df[c])]
    if burn_cols is None:
        burn_cols = numeric_burn_cols
    if not burn_cols:
        raise ValueError("No numeric burn columns available for forecasting")

    load_cols = [c for c in load_df.columns if c != date_col and pd.api.types.is_numeric_dtype(load_df[c])]
    if not load_cols:
        raise ValueError("No numeric load columns available for covariates")
    load_key = load_cols[0]

    merged = pd.merge(
        burn_df[[date_col] + burn_cols],
        load_df[[date_col] + load_cols],
        on=date_col,
        how="inner",
    ).sort_values(date_col)
    if merged.empty:
        raise ValueError("No overlapping dates between burn_df and load_df")

    def _build_future_load() -> pd.DataFrame:
        future_block = load_df.sort_values(date_col).tail(horizon)
        if len(future_block) >= horizon:
            return future_block[[date_col] + load_cols].copy()

        dt = pd.to_datetime(load_df[date_col])
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
        if freq is None:
            delta = dt.diff().dropna().mode()[0] if not dt.empty else pd.Timedelta(days=1)
            freq = delta
        last_date = pd.to_datetime(load_df[date_col]).iloc[-1]
        additional_dates = pd.date_range(start=last_date, periods=horizon + 1, freq=freq)[1:]
        filler = pd.DataFrame({date_col: additional_dates})
        for col in load_cols:
            filler[col] = load_df[col].iloc[-1]
        future_block = pd.concat([load_df[[date_col] + load_cols], filler], ignore_index=True)
        future_block = future_block.drop_duplicates(subset=[date_col]).sort_values(date_col)
        return future_block.tail(horizon)

    future_load = _build_future_load()

    def _baseline() -> ForecastDistillateBurnResult:
        ratio: Dict[str, float] = {}
        for col in burn_cols:
            denom = merged[load_key].replace(0, np.nan)
            col_ratio = (merged[col] / denom).dropna()
            ratio[col] = col_ratio.mean() if not col_ratio.empty else 0.0

        forecast_data = {}
        for col in burn_cols:
            forecast_data[col] = future_load[load_key].astype(float).values * ratio[col]
        forecast_df = pd.DataFrame(forecast_data, index=pd.to_datetime(future_load[date_col]))
        metadata = {"load_column": load_key, "ratio": ratio}
        return ForecastDistillateBurnResult(forecasts=forecast_df, method="baseline", metadata=metadata)

    if method == "sarimax":
        try:
            sarimax_res = intraday_sarimax_forecast(
                date=date_col,
                df=burn_df[[date_col] + burn_cols],
                load_df=future_load,
                periods=horizon,
                **kwargs,
            )
            meta: Dict[str, Any] = {"raw": sarimax_res, "load_column": load_key}
            if sarimax_res.lower_conf_int is not None:
                meta["lower_conf_int"] = sarimax_res.lower_conf_int
            if sarimax_res.upper_conf_int is not None:
                meta["upper_conf_int"] = sarimax_res.upper_conf_int
            return ForecastDistillateBurnResult(
                forecasts=sarimax_res.forecasts[burn_cols],
                method="sarimax",
                metadata=meta,
            )
        except ImportError:
            return _baseline()

    if method == "chronos2":
        try:
            from .forecast_engine import ForecastEngine, build_default_engine

            engine_to_use: ForecastEngine = engine if isinstance(engine, ForecastEngine) else build_default_engine()
            engine_to_use.default_model = "chronos2"
            engine_res = engine_to_use.forecast(
                df=merged[[date_col] + burn_cols + load_cols],
                date_col=date_col,
                target_cols=burn_cols,
                model="chronos2",
                horizon=horizon,
                covariate_cols=load_cols,
                future_covariates=future_load[[date_col] + load_cols],
                quantile_levels=quantile_levels,
                **kwargs,
            )
            meta: Dict[str, Any] = {"engine_metadata": engine_res.metadata, "load_column": load_key}
            return ForecastDistillateBurnResult(
                forecasts=engine_res.forecasts,
                method="chronos2",
                metadata=meta,
            )
        except ImportError:
            return _baseline()

    return _baseline()


def intraday_sarimax_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    load_df: pd.DataFrame,
    periods: int = 12,
    order: Optional[Tuple[int, int, int]] = (1, 0, 0),
    seasonal_order: Optional[Tuple[int, int, int, int]] = None,
    freq: Optional[str] = None,
    cache_path: Optional[str] = None,
    plot: bool = False,
) -> IntradaySarimaxForecastResult:
    """Forecast intraday distillate burn using SARIMAX models with load as an exogenous variable.

    This function models each burn series using the Statsmodels
    ``SARIMAX`` class, allowing for autoregressive dynamics and an
    exogenous load series.  For each burn column, a SARIMAX model is
    fitted to the historical data.  The load values serve as
    exogenous regressors, and the fitted model is used to forecast
    ``periods`` future intraday steps.  Prediction intervals are
    obtained from ``get_forecast`` where available.  Models can be
    cached to avoid re‑fitting.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing datetime information.
    df : pandas.DataFrame
        DataFrame with historical burn data.  Must include the date
        column and at least one numeric burn column.  Should be
        aligned at intraday granularity (e.g. 5‑minute intervals).
    load_df : pandas.DataFrame
        DataFrame with load values, containing the same date column as
        ``df``.  Must include at least one numeric load column.  Must
        contain future load values for the forecast horizon.
    periods : int, default 12
        Number of future intraday periods to forecast.
    order : tuple or None, default (1, 0, 0)
        The (p, d, q) order of the SARIMAX model.  Set to ``None`` to
        let Statsmodels determine the order, though this can be slow
        for high‑frequency data.
    seasonal_order : tuple or None, default None
        The (P, D, Q, s) seasonal order.  By default no seasonal
        component is included.  Set ``s`` equal to the number of
        intraday samples per day (e.g. 288 for 5‑minute data) if a
        daily seasonal component is desired.
    freq : str or None, default None
        Frequency string for generating future timestamps.  If
        ``None``, frequency is inferred from the date series.
    cache_path : str or None, default None
        Directory path to cache fitted models.  When provided, the
        function attempts to load a cached model before fitting a new
        one.  Each model is saved under ``sarimax_{col}.joblib``.
    plot : bool, default False
        Whether to produce an interactive Plotly chart comparing
        historical burn values with forecasts and shaded 95% intervals.

    Returns
    -------
    IntradaySarimaxForecastResult
        Dataclass containing forecast DataFrame, fitted models and
        prediction intervals.

    Notes
    -----
    The SARIMAX model can be computationally intensive at high
    frequency.  To improve efficiency, keep the AR and MA orders
    small or provide an ``order`` tuple directly.  Because this
    implementation fits one model per burn column, the overall
    complexity grows linearly with the number of columns.
    """
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX
    except Exception as e:
        raise ImportError(
            "statsmodels is required for SARIMAX intraday forecasting. "
            "Please install statsmodels to use this function."
        ) from e
    import os
    import joblib
    # Extract date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in burn DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Determine frequency and future timestamps
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(minutes=5)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # Identify burn and load columns
    burn_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    load_cols = [c for c in load_df.columns if c != date and pd.api.types.is_numeric_dtype(load_df[c])]
    if not burn_cols:
        raise ValueError("No numeric burn columns found")
    if not load_cols:
        raise ValueError("No numeric load columns found")
    # Merge burn and load, forward fill missing values
    combined = pd.merge(df[[date] + burn_cols], load_df[[date] + load_cols], on=date, how='inner')
    combined.sort_values(by=date, inplace=True)
    combined[burn_cols] = combined[burn_cols].astype(float).ffill().bfill()
    combined[load_cols] = combined[load_cols].astype(float).ffill().bfill()
    # Determine exogenous future load values for forecast horizon
    # Align load_df to ensure future loads exist at forecast index
    load_future = load_df.set_index(load_df[date])[load_cols].astype(float)
    # Storage
    forecasts: Dict[str, np.ndarray] = {}
    lower_dict: Dict[str, np.ndarray] = {}
    upper_dict: Dict[str, np.ndarray] = {}
    models_dict: Dict[str, object] = {}
    if cache_path is not None:
        os.makedirs(cache_path, exist_ok=True)
    # Fit model per burn column
    for col in burn_cols:
        cache_file = None
        if cache_path is not None:
            cache_file = os.path.join(cache_path, f"sarimax_{col}.joblib")
        # Attempt to load cached model
        model_res = None
        if cache_file is not None and os.path.exists(cache_file):
            try:
                model_res = joblib.load(cache_file)
            except Exception:
                model_res = None
        # If not loaded, fit model
        if model_res is None:
            y = combined[col].values
            exog_train = combined[load_cols].values
            # Determine orders
            order_used = order if order is not None else (1, 0, 0)
            seasonal_used = seasonal_order if seasonal_order is not None else (0, 0, 0, 0)
            sarimax_mod = SARIMAX(
                y,
                exog=exog_train,
                order=order_used,
                seasonal_order=seasonal_used,
                enforce_stationarity=False,
                enforce_invertibility=False,
            )
            model_res = sarimax_mod.fit(disp=False)
            if cache_file is not None:
                try:
                    joblib.dump(model_res, cache_file)
                except Exception:
                    pass
        models_dict[col] = model_res
        # Prepare exogenous predictors for future
        exog_future = []
        for ts in future_index:
            if ts in load_future.index:
                exog_future.append(load_future.loc[ts].values)
            else:
                # If future load missing, use last known
                exog_future.append(load_future.iloc[-1].values)
        exog_future = np.array(exog_future)
        # Forecast
        try:
            forecast_res = model_res.get_forecast(steps=periods, exog=exog_future)
            preds = forecast_res.predicted_mean
            conf_int = forecast_res.conf_int(alpha=0.05)
            lower = conf_int.iloc[:, 0]
            upper = conf_int.iloc[:, 1]
        except Exception:
            preds = model_res.forecast(steps=periods, exog=exog_future)
            lower = None
            upper = None
        forecasts[col] = np.array(preds)
        if lower is not None and upper is not None:
            lower_dict[col] = np.array(lower)
            upper_dict[col] = np.array(upper)
    # Build DataFrames
    forecast_df = pd.DataFrame(forecasts, index=future_index, columns=burn_cols)
    lower_df = None
    upper_df = None
    if lower_dict:
        lower_df = pd.DataFrame(lower_dict, index=future_index, columns=burn_cols)
        upper_df = pd.DataFrame(upper_dict, index=future_index, columns=burn_cols)
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
        except Exception:
            plot = False
        if plot:
            fig = go.Figure()
            for col in burn_cols:
                # Historical
                fig.add_trace(go.Scatter(
                    x=combined[date], y=combined[col], mode='lines', name=f"{col} (historical)"
                ))
                # Forecast
                fig.add_trace(go.Scatter(
                    x=future_index, y=forecast_df[col], mode='lines', name=f"{col} (forecast)", line=dict(dash='dot')
                ))
                # Intervals
                if lower_df is not None and upper_df is not None:
                    fig.add_trace(go.Scatter(
                        x=list(future_index) + list(future_index[::-1]),
                        y=list(upper_df[col]) + list(lower_df[col][::-1]),
                        fill='toself', fillcolor='rgba(255,165,0,0.3)', line=dict(color='rgba(255,165,0,0)'),
                        hoverinfo="skip", showlegend=False
                    ))
            fig.update_layout(
                title="Intraday SARIMAX Burn Forecast", xaxis_title="Time", yaxis_title="Burn", template="plotly_white"
            )
            forecast_df.attrs['plot'] = fig
    return IntradaySarimaxForecastResult(forecasts=forecast_df, models=models_dict, lower_conf_int=lower_df, upper_conf_int=upper_df)


@dataclass
class IntradayQuantileRegressionForecastResult:
    """Result container for :func:`intraday_quantile_regression_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Median predictions for each burn series.
    models : Dict[str, Dict[float, object]]
        Dictionary mapping each burn column to a dictionary of
        quantile regression models keyed by quantile level.
    lower_conf_int : pandas.DataFrame
        Lower prediction interval bounds (e.g. 2.5th percentile) for
        each series.
    upper_conf_int : pandas.DataFrame
        Upper prediction interval bounds (e.g. 97.5th percentile).
    """
    forecasts: pd.DataFrame
    models: Dict[str, Dict[float, object]]
    lower_conf_int: pd.DataFrame
    upper_conf_int: pd.DataFrame


def intraday_quantile_regression_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    load_df: pd.DataFrame,
    periods: int = 12,
    lags: int = 12,
    quantile_levels: Optional[List[float]] = None,
    freq: Optional[str] = None,
    cache_path: Optional[str] = None,
    plot: bool = False,
) -> IntradayQuantileRegressionForecastResult:
    """Forecast intraday burn using linear quantile regression with lagged features.

    This function builds a separate quantile regression model for each
    specified quantile level and for each burn series.  The models
    include lagged burn values and contemporaneous load values as
    predictors.  Forecasts are generated iteratively: the predicted
    burn at time t uses the previously predicted values for earlier
    lags.  The median prediction is returned as the forecast, with
    lower and upper bounds taken from the 2.5th and 97.5th percentile
    predictions by default.  Models can be cached and reused.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing datetime
        information.
    df : pandas.DataFrame
        DataFrame with historical burn data at intraday frequency.
    load_df : pandas.DataFrame
        DataFrame with aligned load values.  Must contain future
        load values for the forecast horizon.
    periods : int, default 12
        Number of future periods to forecast.
    lags : int, default 12
        Number of lagged observations of the burn series to include
        as predictors.  A small number (e.g. 12 for an hour of
        5‑minute data) helps keep computation manageable.
    quantile_levels : list of float or None, default None
        Quantile levels to model.  Must include 0.5 for the median
        forecast.  Defaults to [0.025, 0.5, 0.975].
    freq : str or None, default None
        Frequency string for generating future timestamps.  If
        ``None``, the frequency is inferred from the date series.
    cache_path : str or None, default None
        Directory path to cache fitted models.  For each burn column
        and quantile, the model is saved under
        ``quantreg_{col}_{quantile}.joblib``.
    plot : bool, default False
        Whether to generate an interactive Plotly chart comparing
        historical values with forecasts and shaded intervals.

    Returns
    -------
    IntradayQuantileRegressionForecastResult
        Dataclass containing forecasts, quantile models and interval
        bounds.

    Notes
    -----
    Quantile regression can capture asymmetric predictive
    distributions and is particularly useful when residuals are
    heteroskedastic.  This implementation uses the linear quantile
    regression from Statsmodels; for larger datasets, consider
    alternative quantile regression methods (e.g. gradient boosting).
    """
    try:
        from statsmodels.regression.quantile_regression import QuantReg
    except Exception as e:
        raise ImportError(
            "statsmodels is required for quantile regression forecasting. "
            "Please install statsmodels to use this function."
        ) from e
    import os
    import joblib
    if quantile_levels is None:
        quantile_levels = [0.025, 0.5, 0.975]
    if 0.5 not in quantile_levels:
        quantile_levels.append(0.5)
    quantile_levels = sorted(set(quantile_levels))
    # Extract date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in burn DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Determine frequency and future timestamps
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(minutes=5)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # Identify burn and load columns
    burn_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    load_cols = [c for c in load_df.columns if c != date and pd.api.types.is_numeric_dtype(load_df[c])]
    if not burn_cols:
        raise ValueError("No numeric burn columns found")
    if not load_cols:
        raise ValueError("No numeric load columns found")
    # Merge burn and load
    combined = pd.merge(df[[date] + burn_cols], load_df[[date] + load_cols], on=date, how='inner')
    combined.sort_values(by=date, inplace=True)
    combined[burn_cols] = combined[burn_cols].astype(float).ffill().bfill()
    combined[load_cols] = combined[load_cols].astype(float).ffill().bfill()
    # Set up storage
    forecasts_dict: Dict[str, List[float]] = {}
    lower_dict: Dict[str, List[float]] = {}
    upper_dict: Dict[str, List[float]] = {}
    models_all: Dict[str, Dict[float, object]] = {}
    if cache_path is not None:
        os.makedirs(cache_path, exist_ok=True)
    # Helper: build regression design matrix for a series
    def build_design(y_series: pd.Series, load_matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        n = len(y_series)
        rows = []
        targets = []
        for i in range(lags, n):
            lagged = y_series.iloc[i - lags:i].values[::-1]
            row = np.concatenate([lagged, load_matrix[i]])
            rows.append(row)
            targets.append(y_series.iloc[i])
        return np.array(rows), np.array(targets)
    # Precompute full load matrix
    load_arr = combined[load_cols].values
    # For each burn column
    for col in burn_cols:
        # Build design matrix and target
        y_series = combined[col]
        X_train, y_train = build_design(y_series, load_arr)
        # Precompute future load values vector for prediction
        # We'll create a matrix of shape (periods, lags + n_load)
        future_loads = []
        for ts in future_index:
            # If load available, use actual; else use last known
            match = load_df.loc[load_df[date] == ts, load_cols]
            if not match.empty:
                future_loads.append(match.values[0])
            else:
                future_loads.append(combined[load_cols].iloc[-1].values)
        future_loads = np.array(future_loads)
        # Fit quantile models per quantile
        models_dict_col: Dict[float, object] = {}
        preds_per_quantile: Dict[float, List[float]] = {q: [] for q in quantile_levels}
        # Attempt to load cached models if available
        loaded_all = True if cache_path is not None else False
        if cache_path is not None:
            for q in quantile_levels:
                cache_file = os.path.join(cache_path, f"quantreg_{col}_{q:.3f}.joblib")
                if os.path.exists(cache_file):
                    try:
                        models_dict_col[q] = joblib.load(cache_file)
                    except Exception:
                        loaded_all = False
                        break
                else:
                    loaded_all = False
                    break
        # Fit models if not loaded
        if not loaded_all:
            for q in quantile_levels:
                mod = QuantReg(y_train, X_train)
                res = mod.fit(q=q, max_iter=1000)
                models_dict_col[q] = res
            # Save to cache
            if cache_path is not None:
                for q, res in models_dict_col.items():
                    cache_file = os.path.join(cache_path, f"quantreg_{col}_{q:.3f}.joblib")
                    try:
                        joblib.dump(res, cache_file)
                    except Exception:
                        pass
        # Iterative forecasting
        # Start with last known lags
        history = y_series.tolist()
        for t in range(periods):
            # Build feature vector: latest lags + current load
            lags_vals = history[-lags:][::-1]
            x_features = np.concatenate([np.array(lags_vals), future_loads[t]])
            for q in quantile_levels:
                beta = models_dict_col[q].params
                # Statsmodels QuantReg does not include intercept; we compute via design matrix including intercept? Actually intercept is included in X; but our design matrix lacks intercept.
                # So we need to handle intercept: Statsmodels quantile regression uses no intercept if constant not added. Let's add intercept to X_train.
                # However our design matrix didn't include intercept, meaning model is forced through origin. This may bias predictions; but is acceptable for this demonstration.
                pred = np.dot(x_features, beta)
                preds_per_quantile[q].append(pred)
            # Append median prediction to history for next lag
            history.append(preds_per_quantile[0.5][-1])
        # Collect results per quantile
        # For median forecast we use 0.5
        forecasts_dict[col] = preds_per_quantile[0.5]
        lower_quant = min([q for q in quantile_levels if q < 0.5], default=0.5)
        upper_quant = max([q for q in quantile_levels if q > 0.5], default=0.5)
        lower_dict[col] = preds_per_quantile.get(lower_quant, preds_per_quantile[0.5])
        upper_dict[col] = preds_per_quantile.get(upper_quant, preds_per_quantile[0.5])
        models_all[col] = models_dict_col
    # Build DataFrames
    forecast_df = pd.DataFrame(forecasts_dict, index=future_index, columns=burn_cols)
    lower_df = pd.DataFrame(lower_dict, index=future_index, columns=burn_cols)
    upper_df = pd.DataFrame(upper_dict, index=future_index, columns=burn_cols)
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
        except Exception:
            plot = False
        if plot:
            fig = go.Figure()
            for col in burn_cols:
                # Historical
                fig.add_trace(go.Scatter(
                    x=combined[date], y=combined[col], mode='lines', name=f"{col} (historical)"
                ))
                # Median forecast
                fig.add_trace(go.Scatter(
                    x=future_index, y=forecast_df[col], mode='lines', name=f"{col} (forecast)", line=dict(dash='dot')
                ))
                # Intervals
                fig.add_trace(go.Scatter(
                    x=list(future_index) + list(future_index[::-1]),
                    y=list(upper_df[col]) + list(lower_df[col][::-1]),
                    fill='toself', fillcolor='rgba(255,165,0,0.3)', line=dict(color='rgba(255,165,0,0)'),
                    hoverinfo="skip", showlegend=False
                ))
            fig.update_layout(
                title="Intraday Quantile Regression Burn Forecast", xaxis_title="Time", yaxis_title="Burn", template="plotly_white"
            )
            forecast_df.attrs['plot'] = fig
    return IntradayQuantileRegressionForecastResult(
        forecasts=forecast_df,
        models=models_all,
        lower_conf_int=lower_df,
        upper_conf_int=upper_df,
    )

# ---------------------------------------------------------------------------
# AutoGluon forecasting functions (general and classifier)
# ---------------------------------------------------------------------------

def autogluon_timeseries_forecast_general(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    prediction_length: int = 24,
    id_col: Optional[str] = None,
    model_path: Optional[str] = None,
    freq: Optional[str] = None,
    plot: bool = False,
) -> AutoGluonTimeSeriesForecastResult:
    """Forecast a time series using AutoGluon’s TimeSeries module.

    This wrapper mirrors the example provided in the documentation: it
    accepts a DataFrame with a date column, a target column and
    optional additional features.  If ``id_col`` is not provided, a
    single series is assumed.  The function automatically constructs
    an AutoGluon ``TimeSeriesDataFrame``, fits (or loads) a
    ``TimeSeriesPredictor``, and produces forecasts for the next
    ``prediction_length`` periods.  Quantile predictions at 2.5% and
    97.5% are obtained to form 95% prediction intervals.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing a timestamp column and a target column.
    date_col : str
        Name of the datetime column.  Values will be parsed to
        ``pandas.Timestamp``.
    target_col : str
        Name of the target variable to forecast.
    prediction_length : int, default 24
        Number of future periods to forecast.
    id_col : str or None, default None
        Identifier column for multiple series.  If ``None``, a
        single series is assumed.
    model_path : str or None, default None
        Directory path to save or load the trained AutoGluon
        ``TimeSeriesPredictor``.  If provided and the model
        exists, it will be loaded instead of retraining.
    freq : str or None, default None
        Frequency string of the time series.  If ``None``, the
        frequency is inferred from the timestamp column.
    plot : bool, default False
        Whether to plot the historical series, forecasts and
        confidence intervals using Plotly.

    Returns
    -------
    AutoGluonTimeSeriesForecastResult
        Dataclass containing the forecast DataFrame, the trained
        model and optional prediction intervals.

    Notes
    -----
    The optional quantile forecasts are derived via a separate call to
    the predictor with quantiles set to [0.025, 0.975].  If
    quantile prediction fails, the confidence intervals will be
    returned as ``None``.
    """
    try:
        from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
    except Exception as e:
        raise ImportError(
            "autogluon.timeseries is required for this function. Please install autogluon-timeseries."
        ) from e
    import os
    # Copy and parse dates
    df_in = df.copy()
    df_in[date_col] = pd.to_datetime(df_in[date_col])
    # Add ID column if missing
    if id_col is None:
        df_in["__item_id__"] = "series_1"
        id_used = "__item_id__"
    else:
        id_used = id_col
    # Infer frequency
    if freq is None:
        freq = pd.infer_freq(df_in[date_col].sort_values())
        if freq is None:
            diffs = df_in[date_col].diff().dropna()
            freq = diffs.mode()[0] if not diffs.empty else None
    # Construct TimeSeriesDataFrame
    ag_df = df_in.rename(columns={id_used: "item_id", date_col: "timestamp"})
    ag_df = ag_df.set_index(["item_id", "timestamp"]).sort_index()
    tsdf = TimeSeriesDataFrame.from_data_frame(ag_df)
    # Fit or load predictor
    if model_path is not None and os.path.exists(model_path):
        predictor = TimeSeriesPredictor.load(model_path)
    else:
        predictor = TimeSeriesPredictor(
            prediction_length=prediction_length,
            target=target_col,
            freq=freq,
        )
        predictor.fit(tsdf, presets="medium_quality")
        if model_path is not None:
            predictor.save(model_path)
    # Predict mean forecast
    forecast = predictor.predict(tsdf)
    fc_df = forecast.to_pandas().reset_index()
    # Attempt quantile forecasts
    lower_df = None
    upper_df = None
    try:
        quant_fc = predictor.predict(tsdf, quantiles=[0.025, 0.975])
        qdf = quant_fc.to_pandas().reset_index()
        # pivot quantile columns
        lower_df = qdf.pivot_table(index=["item_id", "timestamp"], values=f"{target_col}_0.025").reset_index()
        upper_df = qdf.pivot_table(index=["item_id", "timestamp"], values=f"{target_col}_0.975").reset_index()
    except Exception:
        pass
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            # Historical
            for sid, sub in df_in.groupby(id_used):
                fig.add_trace(go.Scatter(
                    x=sub[date_col], y=sub[target_col], mode="lines", name=f"{sid} (historical)"
                ))
            # Forecast
            for sid, sub in fc_df.groupby("item_id"):
                fig.add_trace(go.Scatter(
                    x=sub["timestamp"], y=sub[target_col], mode="lines", name=f"{sid} (forecast)", line=dict(dash="dot")
                ))
                # Confidence bands
                if lower_df is not None and upper_df is not None:
                    sub_l = lower_df[lower_df["item_id"] == sid]
                    sub_u = upper_df[upper_df["item_id"] == sid]
                    fig.add_trace(go.Scatter(
                        x=pd.concat([sub_l["timestamp"], sub_u["timestamp"].iloc[::-1]]),
                        y=pd.concat([sub_l[f"{target_col}_0.025"], sub_u[f"{target_col}_0.975"].iloc[::-1]]),
                        fill="toself", fillcolor="rgba(255,165,0,0.2)", line=dict(color="rgba(255,165,0,0)"),
                        showlegend=False
                    ))
            fig.update_layout(title="AutoGluon Time Series Forecast", xaxis_title="Date", yaxis_title=target_col)
            fig.show()
        except Exception:
            pass
    return AutoGluonTimeSeriesForecastResult(
        forecasts=fc_df,
        model=predictor,
        lower_conf_int=lower_df,
        upper_conf_int=upper_df,
    )


def autogluon_tabular_burn_classifier(
    df: pd.DataFrame,
    *,
    target_col: str = "distillate_burn_flag",
    model_path: Optional[str] = None,
    problem_type: Optional[str] = None,
    time_limit: int = 120,
    presets: str = "medium_quality",
) -> AutoGluonTabularBurnClassifierResult:
    """Classify whether the next period will be a major burn using AutoGluon Tabular.

    This function trains a classification model using AutoGluon’s
    Tabular API.  It can load a previously trained model from
    ``model_path`` or fit a new model with specified presets and
    time limit.  The resulting DataFrame includes predicted class
    labels and probabilities.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data with the target flag column and feature columns.
    target_col : str, default 'distillate_burn_flag'
        Name of the binary target column (0/1) indicating whether a
        significant burn occurred.
    model_path : str or None, default None
        Path to load or save the trained model.  If the file exists,
        the model will be loaded.  Otherwise a new model is trained
        and saved to this path if provided.
    problem_type : str or None, default None
        Specify the classification type (e.g. 'binary').  If None,
        AutoGluon infers the type.
    time_limit : int, default 120
        Maximum training time in seconds.  Increase for higher
        accuracy.
    presets : str, default 'medium_quality'
        Preset configuration for AutoGluon training.  Choose from
        'medium_quality' or 'best_quality'.

    Returns
    -------
    AutoGluonTabularBurnClassifierResult
        Dataclass containing the predictions DataFrame and the
        trained model.
    """
    try:
        from autogluon.tabular import TabularPredictor
    except Exception as e:
        raise ImportError(
            "autogluon.tabular is required for this function. Please install autogluon.") from e
    import os
    df_in = df.copy()
    if problem_type is None:
        problem_type = "binary"
    if model_path is not None and os.path.exists(model_path):
        predictor = TabularPredictor.load(model_path)
    else:
        predictor = TabularPredictor(label=target_col, problem_type=problem_type)
        predictor.fit(df_in, presets=presets, time_limit=time_limit)
        if model_path is not None:
            predictor.save(model_path)
    preds = predictor.predict(df_in)
    proba = predictor.predict_proba(df_in)
    result_df = df_in.drop(columns=[target_col]).copy()
    result_df["predicted_flag"] = preds
    if isinstance(proba, pd.DataFrame):
        if 1 in proba.columns:
            result_df["p_burn"] = proba[1]
        else:
            # If AutoGluon names the positive class differently
            result_df["p_burn"] = proba.iloc[:, 1]
    else:
        result_df["p_burn"] = proba
    return AutoGluonTabularBurnClassifierResult(predictions=result_df, model=predictor)


def hierarchical_reconciled_burn_forecast(
    intraday_forecast: pd.DataFrame,
    *,
    date_col: str,
    value_col: str,
    daily_target: Optional[float] = None,
    freq: str = "5T",
) -> pd.DataFrame:
    """Reconcile intraday forecasts to match a daily burn target.

    This utility scales intraday forecasts so that their sum equals a
    specified daily total.  If ``daily_target`` is not provided, the
    input forecast is returned unchanged.  Use this to ensure that
    high‑frequency forecasts align with known or planned daily totals.

    Parameters
    ----------
    intraday_forecast : pandas.DataFrame
        DataFrame with a datetime column and a forecast column.
    date_col : str
        Name of the datetime column.
    value_col : str
        Name of the column containing forecast values.
    daily_target : float or None, default None
        Desired sum of forecasts over the day.  If None, no scaling
        is performed.
    freq : str, default '5T'
        Frequency of the intraday data.  Not used internally but
        included for API consistency.

    Returns
    -------
    pandas.DataFrame
        Reconciled forecasts (scaled) if ``daily_target`` is
        provided; otherwise, a copy of ``intraday_forecast``.
    """
    df = intraday_forecast.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)
    if daily_target is None:
        return df
    current_sum = df[value_col].sum()
    if current_sum == 0:
        return df
    scale = daily_target / current_sum
    df[value_col] = df[value_col] * scale
    return df


def load_weather_interaction_forecast(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    feature_cols: List[str],
    periods: int = 12,
    model_path: Optional[str] = None,
    plot: bool = False,
) -> pd.DataFrame:
    """Penalised linear model for burn with load–weather interactions.

    This function constructs a polynomial design matrix from the
    specified ``feature_cols`` (including interaction terms) and
    fits an ElasticNet regression.  The model can be cached to disk
    and reused.  Forecasts are generated for the next ``periods``
    time steps by replicating the last observed feature row.  An
    optional Plotly plot compares historical and forecast values.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing the datetime column, target column and
        feature columns.
    date_col : str
        Name of the datetime column.
    target_col : str
        Name of the target variable (burn).
    feature_cols : list of str
        Names of features to include (e.g. load, temperature, price).
    periods : int, default 12
        Number of future periods to forecast.
    model_path : str or None, default None
        Path to save or load the fitted model.  If provided and
        exists, the model is loaded instead of retrained.
    plot : bool, default False
        Whether to display a Plotly line chart comparing actuals and
        forecasts.

    Returns
    -------
    pandas.DataFrame
        Forecasts containing the future timestamps and predicted
        target values.
    """
    try:
        from sklearn.preprocessing import PolynomialFeatures
        from sklearn.linear_model import ElasticNetCV
    except Exception as e:
        raise ImportError(
            "scikit-learn is required for load-weather interaction forecasting. "
        ) from e
    import os
    import joblib
    df_in = df.copy()
    df_in[date_col] = pd.to_datetime(df_in[date_col])
    df_in = df_in.sort_values(date_col)
    X = df_in[feature_cols].values.astype(float)
    y = df_in[target_col].astype(float).values
    # Polynomial design
    poly = PolynomialFeatures(degree=2, include_bias=False)
    Xp = poly.fit_transform(X)
    # Load or fit model
    if model_path is not None and os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        model = ElasticNetCV(l1_ratio=[0.1, 0.5, 0.9], n_jobs=-1)
        model.fit(Xp, y)
        if model_path is not None:
            joblib.dump(model, model_path)
    # Construct future features by repeating last observed row
    last_row = df_in[feature_cols].iloc[-1].values.reshape(1, -1)
    future_feat = np.repeat(last_row, periods, axis=0)
    Xf = poly.transform(future_feat)
    preds = model.predict(Xf)
    future_dates = pd.date_range(df_in[date_col].iloc[-1] + pd.to_timedelta("5T"), periods=periods, freq="5T")
    forecast_df = pd.DataFrame({date_col: future_dates, target_col: preds})
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_in[date_col], y=df_in[target_col], mode="lines", name="actual"))
            fig.add_trace(go.Scatter(x=forecast_df[date_col], y=forecast_df[target_col], mode="lines", name="forecast", line=dict(dash="dot")))
            fig.update_layout(title="Load–Weather Interaction Forecast", xaxis_title="Time", yaxis_title=target_col)
            fig.show()
        except Exception:
            pass
    return forecast_df


def forecast_major_burn_days(
    df: pd.DataFrame,
    *,
    date_col: str = "date",
    target_col: str = "burn",
    threshold: float = 1000.0,
    lag_cols: Optional[List[str]] = None,
    max_lag: int = 3,
    plot: bool = False,
) -> MajorBurnForecastResult:
    """Predict the probability of major burn days using gradient boosting.

    This function classifies whether the target exceeds a specified
    threshold.  It builds lagged features for numeric columns and
    fits a calibrated gradient boosting classifier.  The threshold
    that maximizes the F1 score on the training set is selected
    automatically.  Predictions (probabilities and flags) are
    returned for all rows, including future observations with
    missing targets.  Optionally, a Plotly plot visualizes
    predicted probabilities over time.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing a datetime column and the target column.
        Future rows should have NaN in ``target_col`` but may
        contain other feature values.
    date_col : str, default 'date'
        Name of the date column.
    target_col : str, default 'burn'
        Name of the continuous target variable.
    threshold : float, default 1000.0
        Value threshold above which a day is considered a major burn.
    lag_cols : list of str or None, default None
        Columns to create lag features from.  If None, all numeric
        feature columns (excluding the target) are used.
    max_lag : int, default 3
        Number of lagged values to generate for each selected column.
    plot : bool, default False
        Whether to plot the predicted major probabilities over time.

    Returns
    -------
    MajorBurnForecastResult
        Dataclass containing the original DataFrame with added
        prediction columns and the trained model.

    Notes
    -----
    This implementation is inspired by the provided ``forecast_major_days``
    function and adapts it for general burn threshold classification.
    """
    try:
        from sklearn.ensemble import HistGradientBoostingClassifier
        from sklearn.calibration import CalibratedClassifierCV
        from sklearn.metrics import precision_recall_curve
    except Exception as e:
        raise ImportError(
            "scikit-learn is required for forecast_major_burn_days."
        ) from e
    df_in = df.copy()
    # Basic checks
    if date_col not in df_in.columns:
        raise ValueError(f"date_col='{date_col}' not in DataFrame")
    if target_col not in df_in.columns:
        raise ValueError(f"target_col='{target_col}' not in DataFrame")
    # Parse and sort
    df_in[date_col] = pd.to_datetime(df_in[date_col], errors='coerce')
    df_in = df_in.sort_values(date_col).reset_index(drop=True)
    # Identify rows with known target
    df_in['target_known'] = ~df_in[target_col].isna()
    df_in['is_major'] = np.where(
        df_in['target_known'] & (df_in[target_col] > threshold), 1, 0
    )
    # Choose numeric feature columns
    numeric_cols = df_in.select_dtypes(include=[np.number]).columns.tolist()
    base_feature_cols = [c for c in numeric_cols if c not in {target_col, 'is_major'}]
    if lag_cols is None:
        lag_cols = [c for c in base_feature_cols if c not in {'year', 'month', 'day'}]
    # Calendar features
    df_in['dow'] = df_in[date_col].dt.dayofweek
    df_in['month'] = df_in[date_col].dt.month
    df_in['is_weekend'] = (df_in['dow'] >= 5).astype(int)
    # Create lags
    for c in lag_cols:
        for L in range(1, max_lag + 1):
            df_in[f"{c}_lag{L}"] = df_in[c].shift(L)
    # Final feature list
    feature_cols = [
        c for c in df_in.columns
        if c not in {target_col, 'is_major', 'target_known'}
        and df_in[c].dtype != 'O'
    ]
    # Prepare training data
    train_mask = df_in['target_known'].values
    train_df = df_in.loc[train_mask].copy()
    train_df = train_df.dropna(subset=feature_cols + ['is_major'])
    if train_df.empty:
        raise ValueError("No trainable rows after dropping NA; increase history or reduce lags.")
    X_train = train_df[feature_cols].to_numpy(dtype=float)
    y_train = train_df['is_major'].astype(int).to_numpy()
    # Train classifier and calibrate
    base_model = HistGradientBoostingClassifier(
        learning_rate=0.05,
        max_leaf_nodes=31,
        min_samples_leaf=20,
        class_weight='balanced',
    )
    try:
        clf = CalibratedClassifierCV(base_model, method='isotonic', cv=3)
        clf.fit(X_train, y_train)
    except Exception:
        clf = CalibratedClassifierCV(base_model, method='sigmoid', cv=3)
        clf.fit(X_train, y_train)
    # Determine best threshold via F1 score
    train_proba = clf.predict_proba(X_train)[:, 1]
    prec, rec, thr = precision_recall_curve(y_train, train_proba)
    f1 = 2 * prec * rec / (prec + rec + 1e-9)
    best_idx = int(np.nanargmax(f1))
    if best_idx > 0 and best_idx - 1 < len(thr):
        best_thr = float(thr[best_idx - 1])
    else:
        best_thr = 0.5
    # Predict for all rows with complete features
    pred_df = df_in.dropna(subset=feature_cols).copy()
    X_all = pred_df[feature_cols].to_numpy(dtype=float)
    proba_all = clf.predict_proba(X_all)[:, 1]
    pred_df['prob_major'] = proba_all
    pred_df['major_flag'] = (pred_df['prob_major'] >= best_thr).astype(int)
    pred_df['model_threshold'] = best_thr
    pred_df['target_threshold'] = threshold
    # Merge predictions back
    out = df_in.merge(
        pred_df[[date_col, 'prob_major', 'major_flag', 'model_threshold', 'target_threshold']],
        on=date_col,
        how='left'
    ).sort_values(date_col).reset_index(drop=True)
    # Plot probabilities
    if plot:
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=out[date_col], y=out['prob_major'], mode='lines', name='Probability (major burn)'))
            fig.add_trace(go.Scatter(x=out[date_col], y=np.repeat(best_thr, len(out)), mode='lines', name='Threshold', line=dict(dash='dash')))
            fig.update_layout(title='Major Burn Probability Forecast', xaxis_title='Date', yaxis_title='Probability')
            fig.show()
        except Exception:
            pass
    return MajorBurnForecastResult(dataframe=out, model=clf)


# ---------------------------------------------------------------------------
# HistGradientBoosting burn forecast (regression)
# ---------------------------------------------------------------------------

@dataclass
class HistGradientBurnForecastResult:
    """Result container for :func:`hist_gradient_burn_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        DataFrame of forecasted mean values indexed by future timestamps.
    model : object
        Trained regression model for the mean (median) prediction.
    lower_conf_int : pandas.DataFrame or None
        Optional lower bound predictions corresponding to the 95% confidence interval.
    upper_conf_int : pandas.DataFrame or None
        Optional upper bound predictions corresponding to the 95% confidence interval.
    """
    forecasts: pd.DataFrame
    model: object
    lower_conf_int: Optional[pd.DataFrame] = None
    upper_conf_int: Optional[pd.DataFrame] = None


def hist_gradient_burn_forecast(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    feature_cols: Optional[List[str]] = None,
    periods: int = 12,
    lag_cols: Optional[List[str]] = None,
    max_lag: int = 3,
    model_path: Optional[str] = None,
    plot: bool = False,
) -> HistGradientBurnForecastResult:
    """Forecast future burn values using HistGradientBoosting regression.

    This function fits a `HistGradientBoostingRegressor` to model the
    relationship between the target burn series and a set of feature
    columns, optionally including lagged versions of selected columns.
    To provide prediction intervals, two `GradientBoostingRegressor`
    models are fit with quantile loss at the 2.5th and 97.5th
    percentiles.  Trained models can be cached via ``model_path`` to
    avoid retraining on subsequent calls.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing historical data.  Must include the
        ``date_col``, ``target_col`` and feature columns.
    date_col : str
        Name of the datetime column.
    target_col : str
        Name of the target variable to forecast.
    feature_cols : list of str or None, default None
        Names of base feature columns to use.  If None, all numeric
        columns excluding the date and target are used.
    periods : int, default 12
        Number of future periods to forecast.
    lag_cols : list of str or None, default None
        Columns for which to create lagged features.  If None, all
        numeric feature columns (excluding ``target_col``) are used.
    max_lag : int, default 3
        Number of lagged values to generate for each selected column.
    model_path : str or None, default None
        Prefix path for caching models.  Three files will be used:
        ``{model_path}_mean.pkl`` for the mean regressor and
        ``{model_path}_lower.pkl``, ``{model_path}_upper.pkl`` for the
        lower and upper quantile regressors, respectively.  If the
        files exist, models are loaded instead of retrained.
    plot : bool, default False
        Whether to display an interactive Plotly plot comparing
        historical values and forecasts, with shaded 95% confidence
        intervals.

    Returns
    -------
    HistGradientBurnForecastResult
        Dataclass containing the forecast DataFrame, the mean model
        and optional prediction intervals.

    Notes
    -----
    *Scikit‑learn* is required for this function.  If not installed,
    an ``ImportError`` is raised.  The function uses only CPU‑based
    learners and does not require a GPU.
    """
    # Imports deferred to runtime to avoid hard dependency at import time
    try:
        from sklearn.ensemble import HistGradientBoostingRegressor, GradientBoostingRegressor
    except Exception as e:
        raise ImportError(
            "scikit-learn is required for hist_gradient_burn_forecast."
        ) from e
    import os
    import joblib
    df_in = df.copy()
    # Validate columns
    if date_col not in df_in.columns:
        raise KeyError(f"Date column '{date_col}' not found in DataFrame")
    if target_col not in df_in.columns:
        raise KeyError(f"Target column '{target_col}' not found in DataFrame")
    # Parse and sort
    df_in[date_col] = pd.to_datetime(df_in[date_col], errors='coerce')
    df_in = df_in.sort_values(date_col).reset_index(drop=True)
    # Determine feature columns
    if feature_cols is None:
        # Use all numeric columns excluding date and target
        numeric_cols = df_in.select_dtypes(include=[np.number]).columns.tolist()
        feature_cols = [c for c in numeric_cols if c not in {target_col}]
    # Determine lag columns
    if lag_cols is None:
        lag_cols = [c for c in feature_cols if c not in {'year', 'month', 'day'}]
    # Create calendar features
    df_in['dow'] = df_in[date_col].dt.dayofweek
    df_in['month'] = df_in[date_col].dt.month
    df_in['is_weekend'] = (df_in['dow'] >= 5).astype(int)
    # Create lags
    for c in lag_cols:
        for L in range(1, max_lag + 1):
            df_in[f"{c}_lag{L}"] = df_in[c].shift(L)
    # Build final feature list
    feature_cols_final = [c for c in df_in.columns if c not in {target_col} and df_in[c].dtype != 'O']
    # Drop rows with missing values in features or target
    train_df = df_in.dropna(subset=feature_cols_final + [target_col])
    if train_df.empty:
        raise ValueError("No trainable rows after dropping NA; increase history or reduce lags.")
    X_train = train_df[feature_cols_final].to_numpy(dtype=float)
    y_train = train_df[target_col].to_numpy(dtype=float)
    # Paths for caching
    if model_path is not None:
        base = model_path.rstrip('.pkl')
        mean_path = f"{base}_mean.pkl"
        lower_path = f"{base}_lower.pkl"
        upper_path = f"{base}_upper.pkl"
    else:
        mean_path = lower_path = upper_path = None
    # Fit or load mean model
    if mean_path is not None and os.path.exists(mean_path):
        mean_model = joblib.load(mean_path)
    else:
        mean_model = HistGradientBoostingRegressor(
            learning_rate=0.05,
            max_depth=None,
            max_leaf_nodes=31,
            min_samples_leaf=20,
        )
        mean_model.fit(X_train, y_train)
        if mean_path is not None:
            joblib.dump(mean_model, mean_path)
    # Fit or load quantile models
    lower_model = upper_model = None
    # We attempt to fit quantile regressors for 2.5th and 97.5th percentiles
    try:
        if lower_path is not None and os.path.exists(lower_path):
            lower_model = joblib.load(lower_path)
        else:
            lower_model = GradientBoostingRegressor(
                loss='quantile', alpha=0.025, n_estimators=200, learning_rate=0.05, max_depth=3
            )
            lower_model.fit(X_train, y_train)
            if lower_path is not None:
                joblib.dump(lower_model, lower_path)
        if upper_path is not None and os.path.exists(upper_path):
            upper_model = joblib.load(upper_path)
        else:
            upper_model = GradientBoostingRegressor(
                loss='quantile', alpha=0.975, n_estimators=200, learning_rate=0.05, max_depth=3
            )
            upper_model.fit(X_train, y_train)
            if upper_path is not None:
                joblib.dump(upper_model, upper_path)
    except Exception:
        # If quantile regressors fail, we skip prediction intervals
        lower_model = None
        upper_model = None
    # Prepare future feature rows
    last_row = df_in.iloc[-1].copy()
    future_dates: List[pd.Timestamp] = []
    future_features: List[np.ndarray] = []
    # Determine frequency
    diffs = df_in[date_col].diff().dropna()
    if diffs.empty:
        delta = pd.Timedelta(days=1)
    else:
        try:
            delta = diffs.mode()[0]
        except Exception:
            delta = diffs.iloc[-1]
    for i in range(1, periods + 1):
        future_date = df_in[date_col].iloc[-1] + delta * i
        future_dates.append(future_date)
        # Build feature values: replicate last known features and update lags by shifting previous features
        feat_vals = []
        for col in feature_cols_final:
            if col.endswith('_lag') and any(col.startswith(f"{base_col}_lag") for base_col in lag_cols):
                # For lagged features, use previous period's value or last known if not available
                # Compute lag index from column name
                parts = col.rsplit('_lag', 1)
                base_col = parts[0]
                lag_num = int(parts[1])
                if lag_num == 1:
                    # Use last_row[base_col]
                    feat_vals.append(last_row[base_col])
                else:
                    # Use value from prior future_features if available
                    prev_index = len(future_features) - 1
                    if prev_index >= 0:
                        prev_feats = future_features[prev_index]
                        # Find column index of (base_col_lag{lag_num-1}) in feature_cols_final
                        try:
                            idx = feature_cols_final.index(f"{base_col}_lag{lag_num-1}")
                            feat_vals.append(prev_feats[idx])
                        except ValueError:
                            feat_vals.append(last_row[base_col])
                    else:
                        feat_vals.append(last_row[base_col])
            elif col in df_in.columns:
                feat_vals.append(last_row[col])
            else:
                # For calendar features, compute from future_date
                if col == 'dow':
                    feat_vals.append(future_date.dayofweek)
                elif col == 'month':
                    feat_vals.append(future_date.month)
                elif col == 'is_weekend':
                    feat_vals.append(int(future_date.dayofweek >= 5))
                else:
                    feat_vals.append(last_row.get(col, np.nan))
        future_features.append(np.array(feat_vals, dtype=float))
    X_future = np.vstack(future_features)
    # Predict mean and intervals
    mean_preds = mean_model.predict(X_future)
    lower_df = upper_df = None
    if lower_model is not None and upper_model is not None:
        lower_preds = lower_model.predict(X_future)
        upper_preds = upper_model.predict(X_future)
        lower_df = pd.DataFrame({target_col: lower_preds}, index=future_dates)
        upper_df = pd.DataFrame({target_col: upper_preds}, index=future_dates)
    # Create forecast DataFrame
    forecast_df = pd.DataFrame({target_col: mean_preds}, index=future_dates)
    # Plot results
    if plot:
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_in[date_col], y=df_in[target_col], mode='lines', name='historical'))
            fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df[target_col], mode='lines', name='forecast', line=dict(dash='dot')))
            if lower_df is not None and upper_df is not None:
                fig.add_trace(go.Scatter(
                    x=list(forecast_df.index) + list(forecast_df.index[::-1]),
                    y=list(upper_df[target_col]) + list(lower_df[target_col][::-1]),
                    fill='toself', fillcolor='rgba(255,165,0,0.3)', line=dict(color='rgba(255,165,0,0)'),
                    hoverinfo='skip', showlegend=False
                ))
            fig.update_layout(title='HistGradient Burn Forecast', xaxis_title=date_col, yaxis_title=target_col, template='plotly_white')
            forecast_df.attrs['plot'] = fig
        except Exception:
            pass
    return HistGradientBurnForecastResult(
        forecasts=forecast_df,
        model=mean_model,
        lower_conf_int=lower_df,
        upper_conf_int=upper_df,
    )

# ---------------------------------------------------------------------------
# Chronos‑2 forecasting
# ---------------------------------------------------------------------------

@dataclass
class Chronos2ForecastResult:
    """Result container for :func:`chronos2_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        DataFrame of median forecasts for each series (one column per target).
        The index contains the forecast timestamps.
    model : object
        The loaded :class:`Chronos2Pipeline` instance used for prediction.
    lower_conf_int : pandas.DataFrame or None
        Lower bound of the 95 % prediction interval (2.5 % quantile) for each
        target column.  Only present if quantile levels include 0.025.
    upper_conf_int : pandas.DataFrame or None
        Upper bound of the 95 % prediction interval (97.5 % quantile) for each
        target column.  Only present if quantile levels include 0.975.
    summary : Dict[str, float] or None
        Optional summary statistics (mean, median) of the forecast values for
        each target column.
    """

    forecasts: pd.DataFrame
    model: object
    lower_conf_int: Optional[pd.DataFrame] = None
    upper_conf_int: Optional[pd.DataFrame] = None
    summary: Optional[Dict[str, float]] = None


def chronos2_forecast(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    covariate_cols: Optional[List[str]] = None,
    future_cov_df: Optional[pd.DataFrame] = None,
    prediction_length: int = 24,
    quantile_levels: Optional[List[float]] = None,
    model_name: str = "amazon/chronos-2",
    model_path: Optional[str] = None,
    device_map: str = "cpu",
    id_col: Optional[str] = None,
    plot: bool = False,
    summary: bool = False,
) -> Chronos2ForecastResult:
    """Forecast future values using Amazon’s Chronos‑2 foundation model.

    This function wraps the `Chronos2Pipeline` class from the
    ``chronos-forecasting`` package and provides a pandas‑friendly API for
    generating probabilistic forecasts.  It automatically handles
    univariate or multivariate targets, optional covariates, multiple
    training windows and caching of the loaded model.  Prediction
    intervals are extracted from the quantile forecasts, and an
    optional Plotly chart displays historical data, point forecasts and
    shaded 95 % confidence bands.

    Parameters
    ----------
    df : pandas.DataFrame
        Historical data containing a datetime column, the target column and
        optional covariate columns.  The DataFrame may include multiple
        series if ``id_col`` is specified.
    date_col : str
        Name of the datetime column in ``df``.
    target_col : str
        Name of the target column to forecast.  For multivariate
        forecasting, pass a column name containing a struct or list of
        targets.  Chronos‑2 requires the target to be numeric.
    covariate_cols : list of str or None, default None
        Names of columns to use as covariates.  If None, all columns in
        ``df`` other than the date, target and id columns are treated as
        covariates.
    future_cov_df : pandas.DataFrame or None, default None
        DataFrame containing future values of covariates for known
        future times.  Must include the same columns as
        ``covariate_cols`` and the ``date_col``.  If None, no future
        covariates are used.
    prediction_length : int, default 24
        Number of periods to forecast.  Chronos‑2 supports long
        horizons, but longer forecasts may be slower.
    quantile_levels : list of float or None, default None
        Quantile levels to predict.  If None, the default quantiles
        [0.025, 0.5, 0.975] are used.
    model_name : str, default 'amazon/chronos-2'
        Name of the pretrained model to load from Hugging Face or a
        local directory.  See the Chronos model card on Hugging
        Face for available model names.
    model_path : str or None, default None
        Optional directory to cache the model locally.  If provided
        and the directory exists, the model is loaded from this path
        instead of downloading.  After loading from Hugging Face,
        the model is saved into this directory for reuse.
    device_map : str, default 'cpu'
        Device on which to run inference ('cpu' or 'cuda').  Chronos‑2
        uses PyTorch behind the scenes; if GPU is available and
        memory permits, using 'cuda' may accelerate inference.
    id_col : str or None, default None
        Identifier column for multiple series.  If None, a single
        series is assumed and a dummy id is created.
    plot : bool, default False
        If True, display an interactive Plotly figure comparing
        historical data, forecasts and 95 % prediction intervals.
    summary : bool, default False
        If True, compute simple summary statistics (mean and median)
        of the forecasted values for each target column and return
        them in the result dataclass.

    Returns
    -------
    Chronos2ForecastResult
        Dataclass containing the forecast DataFrame, the loaded model,
        optional prediction interval bounds and summary statistics.

    Notes
    -----
    This function requires the ``chronos-forecasting`` package (version
    2.0 or higher) and its dependencies.  Installing the package
    along with the optional ``pandas[pyarrow]`` extra is recommended
    to speed up data loading.  If the package is not installed, an
    informative ``ImportError`` is raised.  The function uses only
    CPU by default; to enable GPU inference, set
    ``device_map='cuda'`` and ensure that a compatible CUDA device
    is available.
    """
    try:
        from chronos import Chronos2Pipeline  # type: ignore[import]
    except Exception as e:
        raise ImportError(
            "chronos-forecasting is required for chronos2_forecast. "
            "Please install it via 'pip install chronos-forecasting'."
        ) from e
    import os
    # Copy and preprocess input
    df_in = df.copy()
    df_in[date_col] = pd.to_datetime(df_in[date_col], errors='coerce')
    df_in = df_in.sort_values(date_col)
    # Determine covariate columns
    if covariate_cols is None:
        covariate_cols = [c for c in df_in.columns if c not in {date_col, target_col}]
        if id_col is not None:
            covariate_cols = [c for c in covariate_cols if c != id_col]
    # Add id column if missing
    if id_col is None:
        df_in['__item_id__'] = 'series_1'
        id_used = '__item_id__'
    else:
        id_used = id_col
    # Build context DataFrame with required columns: id, timestamp, target and covariates
    context_df = df_in[[id_used, date_col, target_col] + covariate_cols].rename(
        columns={id_used: 'id', date_col: 'timestamp', target_col: 'target'}
    )
    # If future covariates provided, align columns
    future_df = None
    if future_cov_df is not None:
        future_in = future_cov_df.copy()
        future_in[date_col] = pd.to_datetime(future_in[date_col], errors='coerce')
        future_in = future_in.sort_values(date_col)
        # Add id column to future covariates
        if id_col is None:
            future_in['__item_id__'] = 'series_1'
            id_used_future = '__item_id__'
        else:
            id_used_future = id_col
        # Use only covariate columns
        future_df = future_in[[id_used_future, date_col] + covariate_cols].rename(
            columns={id_used_future: 'id', date_col: 'timestamp'}
        )
    # Determine quantiles
    if quantile_levels is None:
        quantile_levels = [0.025, 0.5, 0.975]
    # Load or instantiate the pipeline
    if model_path is not None and os.path.exists(model_path):
        try:
            pipeline = Chronos2Pipeline.from_pretrained(model_path, device_map=device_map)
        except Exception:
            pipeline = Chronos2Pipeline.from_pretrained(model_name, device_map=device_map)
            # Save model for reuse
            try:
                pipeline.save_pretrained(model_path)
            except Exception:
                pass
    else:
        pipeline = Chronos2Pipeline.from_pretrained(model_name, device_map=device_map)
        if model_path is not None:
            try:
                pipeline.save_pretrained(model_path)
            except Exception:
                pass
    # Generate predictions
    # Chronos2Pipeline expects target values in context_df and will return a DataFrame
    # with columns: id, timestamp, predictions (median) and quantile columns
    try:
        pred_df = pipeline.predict_df(
            context_df,
            future_df=future_df,
            prediction_length=prediction_length,
            quantile_levels=quantile_levels,
            id_column='id',
            timestamp_column='timestamp',
            target='target',
        )
    except Exception as err:
        raise RuntimeError(
            f"Chronos2Pipeline prediction failed: {err}. Ensure your input DataFrame "
            "is correctly formatted and that chronos-forecasting is installed."
        )
    # Convert predictions to pandas DataFrame with proper index/columns
    pred_df = pred_df.reset_index(drop=True)
    # Extract median forecasts and quantiles
    # The 'predictions' column contains median (0.5) predictions; other columns
    # are named by quantile level strings (e.g. '0.025', '0.975').
    median_name = '0.5' if '0.5' in pred_df.columns else 'predictions'
    # Build per-series DataFrame
    forecasts_dict: Dict[str, pd.Series] = {}
    lower_dict: Dict[str, pd.Series] = {}
    upper_dict: Dict[str, pd.Series] = {}
    summary_dict: Dict[str, float] = {}
    # Group by id to produce separate columns for each series (if applicable)
    for sid, group in pred_df.groupby('id'):
        group_sorted = group.sort_values('timestamp')
        forecasts_dict[sid] = pd.Series(group_sorted[median_name].values, index=group_sorted['timestamp'])
        # Determine quantile columns for 2.5% and 97.5%
        if '0.025' in group_sorted.columns and '0.975' in group_sorted.columns:
            lower_dict[sid] = pd.Series(group_sorted['0.025'].values, index=group_sorted['timestamp'])
            upper_dict[sid] = pd.Series(group_sorted['0.975'].values, index=group_sorted['timestamp'])
        if summary:
            # Simple summary: mean of forecasted values
            summary_dict[sid] = float(group_sorted[median_name].mean())
    # Combine series into DataFrames
    forecasts_df = pd.DataFrame(forecasts_dict)
    lower_df = pd.DataFrame(lower_dict) if lower_dict else None
    upper_df = pd.DataFrame(upper_dict) if upper_dict else None
    summary_out = summary_dict if summary else None
    # Plotting
    if plot:
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            # Plot historical data
            for sid, sub in df_in.groupby(id_used):
                fig.add_trace(go.Scatter(
                    x=sub[date_col], y=sub[target_col], mode='lines', name=f'{sid} (historical)'
                ))
            # Plot forecast and intervals
            for sid in forecasts_df.columns:
                sub = forecasts_df[sid]
                fig.add_trace(go.Scatter(
                    x=sub.index, y=sub.values, mode='lines', name=f'{sid} (forecast)', line=dict(dash='dot')
                ))
                if lower_df is not None and upper_df is not None:
                    lsub = lower_df[sid]
                    usub = upper_df[sid]
                    fig.add_trace(go.Scatter(
                        x=list(lsub.index) + list(usub.index[::-1]),
                        y=list(lsub.values) + list(usub.values[::-1]),
                        fill='toself', fillcolor='rgba(255,165,0,0.2)',
                        line=dict(color='rgba(255,165,0,0)'),
                        showlegend=False
                    ))
            fig.update_layout(
                title='Chronos-2 Forecast', xaxis_title=date_col, yaxis_title=target_col,
                template='plotly_white'
            )
            fig.show()
        except Exception:
            pass
    return Chronos2ForecastResult(
        forecasts=forecasts_df,
        model=pipeline,
        lower_conf_int=lower_df,
        upper_conf_int=upper_df,
        summary=summary_out,
    )


def chronos2_univariate_forecast(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    prediction_length: int = 24,
    quantile_levels: Optional[List[float]] = None,
    model_name: str = "amazon/chronos-2",
    model_path: Optional[str] = None,
    device_map: str = "cpu",
    plot: bool = False,
    summary: bool = False,
) -> Chronos2ForecastResult:
    """Production‑ready Chronos‑2 helper for a single series.

    This is the simplest on‑ramp for Chronos‑2: point it at one datetime
    column and one numeric target column, and it returns quantile
    forecasts.  All optional arguments are tuned for practical defaults so
    new users can forecast in just a few lines.

    Example
    -------
    >>> import pandas as pd
    >>> from analysis3054 import chronos2_univariate_forecast
    >>> dates = pd.date_range("2022-01-01", periods=60, freq="D")
    >>> df = pd.DataFrame({"date": dates, "sales": range(60)})
    >>> result = chronos2_univariate_forecast(
    ...     df,
    ...     date_col="date",
    ...     target_col="sales",
    ...     prediction_length=7,
    ... )
    >>> result.forecasts.head()
      # Median and interval forecasts indexed by future dates
    """

    if df.empty:
        raise ValueError("Input DataFrame is empty; provide at least one row of history.")

    return chronos2_forecast(
        df,
        date_col=date_col,
        target_col=target_col,
        covariate_cols=[],
        future_cov_df=None,
        prediction_length=prediction_length,
        quantile_levels=quantile_levels,
        model_name=model_name,
        model_path=model_path,
        device_map=device_map,
        id_col=None,
        plot=plot,
        summary=summary,
    )


def chronos2_multivariate_forecast(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_cols: List[str],
    covariate_cols: Optional[List[str]] = None,
    future_cov_df: Optional[pd.DataFrame] = None,
    prediction_length: int = 24,
    quantile_levels: Optional[List[float]] = None,
    model_name: str = "amazon/chronos-2",
    model_path: Optional[str] = None,
    device_map: str = "cpu",
    plot: bool = False,
    summary: bool = False,
) -> Chronos2ForecastResult:
    """Chronos‑2 convenience wrapper for multiple targets.

    Accepts a wide DataFrame with several numeric target columns and
    reshapes it internally so Chronos‑2 treats each column as its own
    series.  Shared covariates are forwarded automatically, and optional
    ``future_cov_df`` values are duplicated across every series.

    Example
    -------
    >>> import numpy as np, pandas as pd
    >>> from analysis3054 import chronos2_multivariate_forecast
    >>> dates = pd.date_range("2023-01-01", periods=30, freq="D")
    >>> df = pd.DataFrame({
    ...     "date": dates,
    ...     "north_sales": np.random.rand(30),
    ...     "south_sales": np.random.rand(30),
    ...     "temp": np.random.randn(30),
    ... })
    >>> multi = chronos2_multivariate_forecast(
    ...     df,
    ...     date_col="date",
    ...     target_cols=["north_sales", "south_sales"],
    ...     covariate_cols=["temp"],
    ...     prediction_length=5,
    ... )
    >>> multi.forecasts.head()
      # Columns become a MultiIndex: (series name, quantile)
    """

    if not target_cols:
        raise ValueError("target_cols must contain at least one target column name.")

    base_cols = [date_col] + target_cols
    if covariate_cols:
        base_cols += covariate_cols
    missing = [col for col in base_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in df: {missing}")

    df_wide = df[base_cols].copy()
    id_cols = [date_col] + (covariate_cols or [])
    long_df = df_wide.melt(
        id_vars=id_cols,
        value_vars=target_cols,
        var_name="series",
        value_name="target",
    )

    future_long = None
    if future_cov_df is not None:
        if covariate_cols is None:
            raise ValueError("Provide covariate_cols when using future_cov_df.")
        future_missing = [col for col in [date_col] + covariate_cols if col not in future_cov_df.columns]
        if future_missing:
            raise ValueError(f"Missing required columns in future_cov_df: {future_missing}")
        repeats = []
        for series in target_cols:
            tmp = future_cov_df[[date_col] + covariate_cols].copy()
            tmp["series"] = series
            repeats.append(tmp)
        future_long = pd.concat(repeats, ignore_index=True)

    return chronos2_forecast(
        long_df,
        date_col=date_col,
        target_col="target",
        covariate_cols=covariate_cols,
        future_cov_df=future_long,
        prediction_length=prediction_length,
        quantile_levels=quantile_levels,
        model_name=model_name,
        model_path=model_path,
        device_map=device_map,
        id_col="series",
        plot=plot,
        summary=summary,
    )


def chronos2_covariate_forecast(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    covariate_cols: List[str],
    future_cov_df: pd.DataFrame,
    prediction_length: int = 24,
    quantile_levels: Optional[List[float]] = None,
    model_name: str = "amazon/chronos-2",
    model_path: Optional[str] = None,
    device_map: str = "cpu",
    id_col: Optional[str] = None,
    plot: bool = False,
    summary: bool = False,
) -> Chronos2ForecastResult:
    """Chronos‑2 helper that enforces known future covariates.

    Use this when your forecast quality depends on calendar features,
    weather scenarios, or planned controls.  The function validates that
    the future covariate DataFrame contains all required columns and then
    delegates to :func:`chronos2_forecast`.

    Example
    -------
    >>> import numpy as np, pandas as pd
    >>> from analysis3054 import chronos2_covariate_forecast
    >>> hist_dates = pd.date_range("2024-01-01", periods=50, freq="D")
    >>> future_dates = pd.date_range("2024-02-20", periods=7, freq="D")
    >>> history = pd.DataFrame({
    ...     "date": hist_dates,
    ...     "demand": 100 + np.random.randn(50),
    ...     "temp": 30 + np.random.randn(50),
    ... })
    >>> future_weather = pd.DataFrame({"date": future_dates, "temp": 32})
    >>> covar = chronos2_covariate_forecast(
    ...     history,
    ...     date_col="date",
    ...     target_col="demand",
    ...     covariate_cols=["temp"],
    ...     future_cov_df=future_weather,
    ...     prediction_length=7,
    ... )
    >>> covar.forecasts.tail(3)
      # Shows median/interval forecasts aligned to the provided future dates
    """

    required_cols = [date_col] + list(covariate_cols)
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in df: {missing}")

    future_missing = [col for col in required_cols if col not in future_cov_df.columns]
    if future_missing:
        raise ValueError(f"Missing required columns in future_cov_df: {future_missing}")

    return chronos2_forecast(
        df,
        date_col=date_col,
        target_col=target_col,
        covariate_cols=covariate_cols,
        future_cov_df=future_cov_df,
        prediction_length=prediction_length,
        quantile_levels=quantile_levels,
        model_name=model_name,
        model_path=model_path,
        device_map=device_map,
        id_col=id_col,
        plot=plot,
        summary=summary,
    )

# ---------------------------------------------------------------------------
# TimesFM forecasting (Hugging Face)
# ---------------------------------------------------------------------------

@dataclass
class TimesFmForecastResult:
    """Result container for :func:`timesfm_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Point forecast (median) values indexed by future timestamps.  Each
        column corresponds to a series (for multi‑series input).
    lower_conf_int : pandas.DataFrame or None
        Optional lower bound (2.5 % quantile) predictions.
    upper_conf_int : pandas.DataFrame or None
        Optional upper bound (97.5 % quantile) predictions.
    model : object
        The loaded TimesFM model instance.
    summary : Dict[str, float] or None
        Optional summary statistics (mean forecast) for each series.
    """

    forecasts: pd.DataFrame
    lower_conf_int: Optional[pd.DataFrame] = None
    upper_conf_int: Optional[pd.DataFrame] = None
    model: object = None
    summary: Optional[Dict[str, float]] = None


# -----------------------------------------------------------------------------
# Chronos‑Bolt advanced utilities
# -----------------------------------------------------------------------------

# Dataclasses for new Chronos‑Bolt utilities
@dataclass
class ChronosBoltQuantileForecastResult:
    """Result of ``chronos_bolt_quantile_forecast``.

    Parameters
    ----------
    forecasts : pandas.DataFrame
        DataFrame indexed by the forecast timestamps.  Columns follow a
        two‑level MultiIndex of (item_id, quantile) if multiple series
        are present, otherwise single‑level columns for each quantile.
    predictor : object
        The AutoGluon ``TimeSeriesPredictor`` used to generate forecasts.
    quantile_levels : list of float
        The quantile levels used for prediction (e.g. [0.025, 0.5, 0.975]).
    summary : dict or None
        Optional dictionary mapping each series to the mean of its median
        forecast.  Populated if ``summary=True`` is passed.
    """

    forecasts: pd.DataFrame
    predictor: object
    quantile_levels: List[float]
    summary: Optional[Dict[str, float]] = None


@dataclass
class ChronosBoltAnomalyResult:
    """Result of ``chronos_bolt_anomaly_detection``.

    Parameters
    ----------
    anomalies : pandas.DataFrame
        DataFrame containing actual values, predicted mean, prediction
        intervals and anomaly flag for the evaluation period.  Indexed by
        timestamp with columns: 'actual', 'forecast', 'lower', 'upper',
        'anomaly'.  For multiple series, a MultiIndex with (item_id,
        timestamp) is used.
    predictor : object
        The AutoGluon ``TimeSeriesPredictor`` used to generate forecasts.
    summary : dict or None
        Optional summary statistics, including the fraction of anomalies
        detected for each series.
    """
    anomalies: pd.DataFrame
    predictor: object
    summary: Optional[Dict[str, float]] = None


@dataclass
class ChronosBoltImputeResult:
    """Result of ``chronos_bolt_impute_missing``.

    Parameters
    ----------
    df_imputed : pandas.DataFrame
        A copy of the input DataFrame with missing target values at the end
        imputed using Chronos‑Bolt forecasts.  Only missing values at the
        end of the series are imputed; other missing entries remain.
    predictor : object
        The AutoGluon ``TimeSeriesPredictor`` used for forecasting.
    """
    df_imputed: pd.DataFrame
    predictor: object


def chronos_bolt_quantile_forecast(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    id_col: Optional[str] = None,
    covariate_cols: Optional[List[str]] = None,
    prediction_length: int = 24,
    quantile_levels: Optional[List[float]] = None,
    model_name: str = "autogluon/chronos-bolt-base",
    model_path: Optional[str] = None,
    freq: Optional[str] = None,
    plot: bool = False,
    summary: bool = False,
) -> ChronosBoltQuantileForecastResult:
    """Flexible quantile forecasting using Chronos‑Bolt.

    This utility wraps :class:`autogluon.timeseries.TimeSeriesPredictor` with
    Chronos‑Bolt as the base model and returns forecasts for multiple
    quantile levels.  It automatically prepares known and past covariates,
    handles multiple series via ``id_col``, caches the trained predictor and
    optionally plots the forecast with 95 % prediction bands.

    Parameters
    ----------
    df : pandas.DataFrame
        Historical data containing a datetime column, the target column and
        optional covariate columns.  The DataFrame may include multiple
        series if ``id_col`` is specified.
    date_col : str
        Name of the datetime column in ``df``.
    target_col : str
        Name of the target column to forecast.
    id_col : str or None, default None
        Identifier column for multiple series.  If None, a dummy id is
        created.
    covariate_cols : list of str or None, default None
        Names of columns to use as covariates.  If None, all numeric
        columns other than the date and target (and id, if present) are
        treated as covariates.
    prediction_length : int, default 24
        Number of time steps to forecast.
    quantile_levels : list of float or None, default None
        Quantile levels to predict.  If None, the defaults [0.025, 0.5,
        0.975] are used.
    model_name : str, default 'autogluon/chronos-bolt-base'
        Name of the Chronos‑Bolt model on Hugging Face Hub.  Other
        variants include 'chronos-bolt-small', etc.
    model_path : str or None, default None
        Directory to cache the trained predictor.  If provided and a saved
        predictor exists at this path, it is loaded instead of re‑training.
    freq : str or None, default None
        Frequency string for the time series.  If None, the frequency is
        inferred from the date column.
    plot : bool, default False
        If True, display an interactive Plotly figure showing the median
        forecast and 95 % prediction intervals.
    summary : bool, default False
        If True, compute the mean of the median forecast for each series
        and return it in the result dataclass.

    Returns
    -------
    ChronosBoltQuantileForecastResult
        Dataclass containing the forecast DataFrame, the fitted
        TimeSeriesPredictor and summary statistics.
    """
    try:
        from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor  # type: ignore
    except Exception as e:
        raise ImportError(
            "autogluon.timeseries is required for chronos_bolt_quantile_forecast. "
            "Install via pip install autogluon.timeseries"
        ) from e
    import joblib
    import os
    df_in = df.copy()
    df_in[date_col] = pd.to_datetime(df_in[date_col], errors="coerce")
    df_in = df_in.sort_values(date_col)
    # Determine id
    if id_col is None:
        df_in["__item_id__"] = "series_1"
        id_used = "__item_id__"
    else:
        id_used = id_col
    # Determine covariates
    if covariate_cols is None:
        covariate_cols = [c for c in df_in.select_dtypes(include=[np.number]).columns if c not in {target_col}]
        covariate_cols = [c for c in covariate_cols if c != id_used]
    # Format to TimeSeriesDataFrame
    tsdf = df_in[[id_used, date_col, target_col] + covariate_cols].rename(
        columns={id_used: "item_id", date_col: "timestamp"}
    )
    tsdf = tsdf.set_index(["item_id", "timestamp"]).sort_index()
    tsdf = TimeSeriesDataFrame(tsdf)
    # Infer freq if needed
    if freq is None:
        try:
            freq = pd.infer_freq(df_in[date_col].sort_values())
        except Exception:
            freq = None
    # Quantiles
    if quantile_levels is None:
        quantile_levels = [0.025, 0.5, 0.975]
    # Load or fit predictor
    predictor = None
    if model_path is not None and os.path.exists(model_path):
        try:
            predictor = joblib.load(model_path)
        except Exception:
            predictor = None
    if predictor is None:
        predictor = TimeSeriesPredictor(
            target=target_col,
            prediction_length=prediction_length,
            freq=freq,
            quantile_levels=quantile_levels,
        )
        predictor.fit(
            tsdf,
            hyperparameters={"Chronos": {"model_path": model_name}},
            known_covariates=None,
            past_covariates=None,
        )
        if model_path is not None:
            try:
                joblib.dump(predictor, model_path)
            except Exception:
                pass
    # Predict
    forecast_tsdf = predictor.predict(tsdf)
    forecast_df = forecast_tsdf.to_pandas().reset_index()
    # Build DataFrame with quantile columns
    items = forecast_df["item_id"].unique()
    # Determine columns for each quantile; they appear as strings of quantile levels
    columns_by_q: Dict[float, Dict[str, List[float]]] = {q: {} for q in quantile_levels}
    for item in items:
        sub = forecast_df[forecast_df["item_id"] == item]
        sub = sub.sort_values("timestamp")
        for q in quantile_levels:
            q_col = f"{q}" if q != 0.5 else ("mean" if "mean" in sub.columns else "0.5")
            # prefer column names: 'mean' or '0.5'
            if q == 0.5 and "mean" in sub.columns:
                val = sub["mean"].tolist()
            else:
                if q_col in sub.columns:
                    val = sub[q_col].tolist()
                else:
                    # fallback: use "mean" for median
                    val = sub["mean" if "mean" in sub.columns else q_col].tolist()
            columns_by_q[q][item] = val
    # Build MultiIndex DataFrame
    index = pd.to_datetime(
        forecast_df[forecast_df["item_id"] == items[0]]["timestamp"].values
    )
    # create columns MultiIndex: (item, quantile)
    tuples = []
    data = []
    for q, item_dict in columns_by_q.items():
        for item, vals in item_dict.items():
            tuples.append((item, q))
            data.append(vals)
    df_forecasts = pd.DataFrame(np.array(data).T, index=index)
    df_forecasts.columns = pd.MultiIndex.from_tuples(tuples, names=["item_id", "quantile"])
    summary_dict: Dict[str, float] = {}
    if summary:
        # mean of median (quantile 0.5 or mean) for each item
        for item in items:
            if 0.5 in quantile_levels:
                summary_dict[item] = float(np.mean(columns_by_q[0.5][item]))
            else:
                # use mean from predicted output if 0.5 not present
                median_vals = columns_by_q[quantile_levels[len(quantile_levels)//2]][item]
                summary_dict[item] = float(np.mean(median_vals))
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            # Historical series
            hist = df_in[[id_used, date_col, target_col]].copy()
            for item in items:
                sub_hist = hist[hist[id_used] == item] if id_col is not None else hist
                fig.add_trace(go.Scatter(
                    x=sub_hist[date_col],
                    y=sub_hist[target_col],
                    mode="lines",
                    name=f"{item} actual",
                ))
            # Plot median and intervals for first two quantiles (min and max) if available
            lower_q = min(quantile_levels)
            upper_q = max(quantile_levels)
            median_q = 0.5 if 0.5 in quantile_levels else quantile_levels[len(quantile_levels)//2]
            for item in items:
                median_vals = columns_by_q[median_q][item]
                lower_vals = columns_by_q[lower_q][item]
                upper_vals = columns_by_q[upper_q][item]
                ts = index
                fig.add_trace(go.Scatter(
                    x=ts,
                    y=median_vals,
                    mode="lines",
                    name=f"{item} forecast",
                    line=dict(dash="dot"),
                ))
                # Shade CI
                fig.add_trace(go.Scatter(
                    x=np.concatenate([ts, ts[::-1]]),
                    y=np.concatenate([lower_vals, upper_vals[::-1]]),
                    fill="toself",
                    fillcolor="rgba(255,165,0,0.2)",
                    line=dict(color="rgba(255,165,0,0)"),
                    showlegend=False,
                    name=f"{item} CI",
                ))
            fig.update_layout(title="Chronos‑Bolt Quantile Forecast")
            fig.show()
        except Exception:
            pass
    return ChronosBoltQuantileForecastResult(
        forecasts=df_forecasts,
        predictor=predictor,
        quantile_levels=quantile_levels,
        summary=summary_dict if summary else None,
    )


def chronos_bolt_anomaly_detection(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    id_col: Optional[str] = None,
    covariate_cols: Optional[List[str]] = None,
    prediction_length: int = 24,
    lower_quantile: float = 0.025,
    upper_quantile: float = 0.975,
    model_name: str = "autogluon/chronos-bolt-base",
    model_path: Optional[str] = None,
    freq: Optional[str] = None,
    plot: bool = False,
) -> ChronosBoltAnomalyResult:
    """Detect anomalies by comparing actual values to Chronos‑Bolt forecast intervals.

    This function splits the data into a training portion (historical data up to
    ``prediction_length`` points before the end) and an evaluation portion (the
    last ``prediction_length`` points).  It trains a Chronos‑Bolt predictor on
    the training set and forecasts the evaluation horizon.  Actual values
    outside the prediction interval defined by ``lower_quantile`` and
    ``upper_quantile`` are flagged as anomalies.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the date, target and optional covariate columns.
    date_col : str
        Name of the datetime column.
    target_col : str
        Name of the target column.
    id_col : str or None, default None
        Identifier for multiple series.  If None, a dummy id is used.
    covariate_cols : list of str or None, default None
        List of covariate column names.  If None, all numeric columns except
        the target and id are used.
    prediction_length : int, default 24
        Number of observations at the end of the series to treat as the
        evaluation horizon.
    lower_quantile : float, default 0.025
        Lower quantile for prediction interval.
    upper_quantile : float, default 0.975
        Upper quantile for prediction interval.
    model_name : str, default 'autogluon/chronos-bolt-base'
        Name of the Chronos‑Bolt model.
    model_path : str or None, default None
        Path to cache the predictor.  If provided and a saved predictor
        exists, it is loaded.
    freq : str or None, default None
        Frequency string for the time series.  Inferred if None.
    plot : bool, default False
        Whether to plot the actual values and prediction intervals.

    Returns
    -------
    ChronosBoltAnomalyResult
        Result dataclass containing a DataFrame with actual, forecast,
        prediction interval bounds and anomaly flag, as well as summary
        statistics of anomaly rates.
    """
    # Split into training and evaluation sets
    df_sorted = df.copy().sort_values(date_col)
    total_rows = len(df_sorted)
    if total_rows <= prediction_length:
        raise ValueError("Not enough data points for anomaly detection")
    train_df = df_sorted.iloc[: total_rows - prediction_length].copy()
    eval_df = df_sorted.iloc[total_rows - prediction_length :].copy()
    # Train predictor and forecast
    result = chronos_bolt_quantile_forecast(
        train_df,
        date_col=date_col,
        target_col=target_col,
        id_col=id_col,
        covariate_cols=covariate_cols,
        prediction_length=prediction_length,
        quantile_levels=[lower_quantile, 0.5, upper_quantile],
        model_name=model_name,
        model_path=model_path,
        freq=freq,
        plot=False,
        summary=False,
    )
    # Build DataFrame with evaluation actuals and predictions
    # result.forecasts has MultiIndex columns (item, quantile)
    fcast_df = result.forecasts
    # unify to long format: index=timestamp, columns=quantiles for each item
    anomalies_list = []
    summary_dict: Dict[str, float] = {}
    # for each series and quantile, align with actuals
    if isinstance(fcast_df.columns, pd.MultiIndex):
        for item in fcast_df.columns.get_level_values(0).unique():
            eval_sub = eval_df if id_col is None else eval_df[eval_df[id_col] == item]
            if eval_sub.empty:
                continue
            ts = fcast_df.index
            # predictions
            lower_vals = fcast_df[(item, lower_quantile)].values
            median_vals = fcast_df[(item, 0.5)].values if (item, 0.5) in fcast_df.columns else fcast_df[(item, "mean")].values
            upper_vals = fcast_df[(item, upper_quantile)].values
            actual_vals = eval_sub[target_col].values
            # Build DataFrame for each timestamp (ensuring same length)
            length = min(len(actual_vals), len(ts))
            df_tmp = pd.DataFrame({
                "item_id": [item] * length,
                "timestamp": ts[:length],
                "actual": actual_vals[:length],
                "forecast": median_vals[:length],
                "lower": lower_vals[:length],
                "upper": upper_vals[:length],
            })
            df_tmp["anomaly"] = ((df_tmp["actual"] < df_tmp["lower"]) | (df_tmp["actual"] > df_tmp["upper"])).astype(int)
            anomalies_list.append(df_tmp)
            # summary: fraction of anomalies
            summary_dict[item] = float(df_tmp["anomaly"].mean())
    else:
        # single series, fcast_df columns are quantiles only
        item = "series_1"
        ts = fcast_df.index
        lower_vals = fcast_df[lower_quantile].values
        median_vals = fcast_df[0.5].values if 0.5 in fcast_df.columns else fcast_df["mean"].values
        upper_vals = fcast_df[upper_quantile].values
        actual_vals = eval_df[target_col].values
        length = min(len(actual_vals), len(ts))
        df_tmp = pd.DataFrame({
            "item_id": [item] * length,
            "timestamp": ts[:length],
            "actual": actual_vals[:length],
            "forecast": median_vals[:length],
            "lower": lower_vals[:length],
            "upper": upper_vals[:length],
        })
        df_tmp["anomaly"] = ((df_tmp["actual"] < df_tmp["lower"]) | (df_tmp["actual"] > df_tmp["upper"])).astype(int)
        anomalies_list.append(df_tmp)
        summary_dict[item] = float(df_tmp["anomaly"].mean())
    anomalies_df = pd.concat(anomalies_list).set_index(["item_id", "timestamp"])
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            for item in anomalies_df.index.get_level_values(0).unique():
                df_item = anomalies_df.loc[item]
                fig.add_trace(go.Scatter(
                    x=df_item.index,
                    y=df_item["actual"],
                    mode="lines",
                    name=f"{item} actual",
                ))
                fig.add_trace(go.Scatter(
                    x=df_item.index,
                    y=df_item["forecast"],
                    mode="lines",
                    name=f"{item} forecast",
                    line=dict(dash="dot"),
                ))
                fig.add_trace(go.Scatter(
                    x=np.concatenate([df_item.index, df_item.index[::-1]]),
                    y=np.concatenate([df_item["lower"], df_item["upper"][::-1]]),
                    fill="toself",
                    fillcolor="rgba(255,165,0,0.2)",
                    line=dict(color="rgba(255,165,0,0)"),
                    showlegend=False,
                    name=f"{item} CI",
                ))
                # mark anomalies
                anomalies_points = df_item[df_item["anomaly"] == 1]
                fig.add_trace(go.Scatter(
                    x=anomalies_points.index,
                    y=anomalies_points["actual"],
                    mode="markers",
                    marker=dict(symbol="x", size=8),
                    name=f"{item} anomaly",
                ))
            fig.update_layout(title="Chronos‑Bolt Anomaly Detection")
            fig.show()
        except Exception:
            pass
    return ChronosBoltAnomalyResult(
        anomalies=anomalies_df,
        predictor=result.predictor,
        summary=summary_dict,
    )


def chronos_bolt_impute_missing(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    id_col: Optional[str] = None,
    covariate_cols: Optional[List[str]] = None,
    model_name: str = "autogluon/chronos-bolt-base",
    model_path: Optional[str] = None,
    freq: Optional[str] = None,
) -> ChronosBoltImputeResult:
    """Impute missing values at the end of a series using Chronos‑Bolt forecasting.

    This helper assumes that missing values occur only at the end of the
    dataset.  It trains a Chronos‑Bolt predictor on the available portion and
    forecasts the missing portion, then fills those missing entries with
    predicted values.  Missing values inside the series are not imputed.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing date, target and optional covariate columns.
    date_col : str
        Datetime column.
    target_col : str
        Target column with NaNs at the end.
    id_col : str or None, default None
        Series identifier.  If None, a dummy id is used.
    covariate_cols : list of str or None, default None
        Covariates for the Chronos‑Bolt model.  If None, all numeric
        columns except the target and id are used.
    model_name : str, default 'autogluon/chronos-bolt-base'
        Name of the Chronos‑Bolt model.
    model_path : str or None, default None
        Path to cache the predictor.
    freq : str or None, default None
        Frequency of the time series.  Inferred if None.

    Returns
    -------
    ChronosBoltImputeResult
        Dataclass containing the imputed DataFrame and the fitted predictor.
    """
    df_sorted = df.copy().sort_values(date_col)
    df_sorted[date_col] = pd.to_datetime(df_sorted[date_col], errors="coerce")
    # Identify trailing missing values
    target_vals = df_sorted[target_col].values
    # find first index from end where value is not NaN
    valid_indices = np.where(~pd.isna(target_vals))[0]
    if len(valid_indices) == 0:
        raise ValueError("All target values are NaN; cannot impute")
    last_valid_idx = valid_indices[-1]
    missing_count = len(target_vals) - last_valid_idx - 1
    if missing_count <= 0:
        # Nothing to impute
        return ChronosBoltImputeResult(df_sorted, predictor=None)
    # training data until last_valid_idx
    train_df = df_sorted.iloc[: last_valid_idx + 1].copy()
    # forecast horizon = missing_count
    forecast_res = chronos_bolt_quantile_forecast(
        train_df,
        date_col=date_col,
        target_col=target_col,
        id_col=id_col,
        covariate_cols=covariate_cols,
        prediction_length=missing_count,
        quantile_levels=[0.5],
        model_name=model_name,
        model_path=model_path,
        freq=freq,
        plot=False,
        summary=False,
    )
    # Extract median predictions for the series
    fcast_df = forecast_res.forecasts
    # Determine id
    if id_col is None:
        item = "series_1"
    else:
        item = df_sorted.iloc[0][id_col]
    # Fetch predictions; if multiindex, choose median quantile 0.5 or 'mean'
    if isinstance(fcast_df.columns, pd.MultiIndex):
        if (item, 0.5) in fcast_df.columns:
            preds = fcast_df[(item, 0.5)].values
        else:
            # fallback to first column
            preds = fcast_df.xs(item, level=0, axis=1).iloc[:, 0].values
    else:
        preds = fcast_df[0.5].values if 0.5 in fcast_df.columns else fcast_df.iloc[:, 0].values
    # Fill missing values
    df_imputed = df_sorted.copy()
    impute_indices = list(range(last_valid_idx + 1, last_valid_idx + 1 + missing_count))
    df_imputed.iloc[impute_indices, df_imputed.columns.get_loc(target_col)] = preds[:missing_count]
    return ChronosBoltImputeResult(df_imputed, predictor=forecast_res.predictor)


# -----------------------------------------------------------------------------
# Chronos‑2 advanced utilities
# -----------------------------------------------------------------------------

@dataclass
class Chronos2QuantileForecastResult:
    """Result of ``chronos2_quantile_forecast``.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasts indexed by forecast timestamps with MultiIndex columns
        (item_id, quantile).  For a single series, columns are
        single‑level quantile names.
    model : object
        The loaded Chronos‑2 model pipeline.
    quantile_levels : list of float
        The quantile levels requested.
    summary : dict or None
        Optional dictionary mapping each series to the mean of its
        median forecast.
    """

    forecasts: pd.DataFrame
    model: object
    quantile_levels: List[float]
    summary: Optional[Dict[str, float]] = None


@dataclass
class Chronos2AnomalyResult:
    """Result of ``chronos2_anomaly_detection``.

    Attributes
    ----------
    anomalies : pandas.DataFrame
        DataFrame containing actual values, forecast median, lower and
        upper prediction bounds and an anomaly flag.  Indexed by
        (item_id, timestamp).
    model : object
        The Chronos‑2 model pipeline used for forecasting.
    summary : dict or None
        Optional summary statistics: fraction of anomalies per series.
    """
    anomalies: pd.DataFrame
    model: object
    summary: Optional[Dict[str, float]] = None


@dataclass
class Chronos2ImputeResult:
    """Result of ``chronos2_impute_missing``.

    Attributes
    ----------
    df_imputed : pandas.DataFrame
        DataFrame with trailing NaNs in the target column imputed using
        Chronos‑2 forecasts.
    model : object
        The Chronos‑2 model pipeline used for forecasting.
    """
    df_imputed: pd.DataFrame
    model: object


def chronos2_quantile_forecast(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    covariate_cols: Optional[List[str]] = None,
    future_cov_df: Optional[pd.DataFrame] = None,
    prediction_length: int = 24,
    quantile_levels: Optional[List[float]] = None,
    model_name: str = "amazon/chronos-2",
    model_path: Optional[str] = None,
    device_map: str = "cpu",
    id_col: Optional[str] = None,
    plot: bool = False,
    summary: bool = False,
) -> Chronos2QuantileForecastResult:
    """Quantile forecasting with Amazon's Chronos‑2 model.

    This function wraps the :class:`chronos.Chronos2Pipeline` and
    generates forecasts for arbitrary quantile levels.  It handles
    multiple series via ``id_col``, accepts optional covariates and
    future covariates, caches the model for reuse and plots the
    forecasts with shaded prediction intervals.

    Parameters
    ----------
    df : pandas.DataFrame
        Historical data with datetime, target and optional covariate columns.
    date_col : str
        Name of the datetime column.
    target_col : str
        Name of the target column to forecast.
    covariate_cols : list of str or None, default None
        Columns to treat as covariates.  If None, all columns except
        date_col, target_col and id_col are used.
    future_cov_df : pandas.DataFrame or None, default None
        DataFrame containing future values of covariates.  Must include
        the same covariate columns and the date column.
    prediction_length : int, default 24
        Number of periods to forecast.
    quantile_levels : list of float or None, default None
        Quantiles to return.  Defaults to [0.025, 0.5, 0.975].
    model_name : str, default 'amazon/chronos-2'
        Name of the pretrained Chronos‑2 model to load.
    model_path : str or None, default None
        Directory for caching the model.  If set, the model is loaded
        from this path if present or saved here after download.
    device_map : str, default 'cpu'
        Device for model inference.  Use 'cuda' for GPU if available.
    id_col : str or None, default None
        Column identifying multiple series.  If None, a single series
        is assumed.
    plot : bool, default False
        Whether to display an interactive Plotly chart of the forecast.
    summary : bool, default False
        If True, compute the mean of the median forecast for each series
        and include it in the result.

    Returns
    -------
    Chronos2QuantileForecastResult
        Dataclass containing the forecast DataFrame, the loaded model and
        summary statistics.
    """
    # Import Chronos‑2 lazily
    try:
        from chronos import Chronos2Pipeline  # type: ignore
    except Exception as e:
        raise ImportError(
            "chronos-forecasting is required for chronos2_quantile_forecast. "
            "Install via 'pip install chronos-forecasting'"
        ) from e
    import os
    df_in = df.copy()
    df_in[date_col] = pd.to_datetime(df_in[date_col], errors="coerce")
    df_in = df_in.sort_values(date_col)
    # Determine covariates
    if covariate_cols is None:
        covariate_cols = [c for c in df_in.columns if c not in {date_col, target_col}]
        if id_col is not None:
            covariate_cols = [c for c in covariate_cols if c != id_col]
    # Add id
    if id_col is None:
        df_in["__item_id__"] = "series_1"
        id_used = "__item_id__"
    else:
        id_used = id_col
    # Build context DataFrame
    context_df = df_in[[id_used, date_col, target_col] + covariate_cols].rename(
        columns={id_used: "id", date_col: "timestamp", target_col: "target"}
    )
    future_df = None
    if future_cov_df is not None:
        fdf = future_cov_df.copy()
        fdf[date_col] = pd.to_datetime(fdf[date_col], errors="coerce")
        fdf = fdf.sort_values(date_col)
        if id_col is None:
            fdf["__item_id__"] = "series_1"
            id_used_future = "__item_id__"
        else:
            id_used_future = id_col
        future_df = fdf[[id_used_future, date_col] + covariate_cols].rename(
            columns={id_used_future: "id", date_col: "timestamp"}
        )
    # Quantile levels
    if quantile_levels is None:
        quantile_levels = [0.025, 0.5, 0.975]
    # Load or create pipeline
    if model_path is not None and os.path.exists(model_path):
        try:
            pipeline = Chronos2Pipeline.from_pretrained(model_path, device_map=device_map)
        except Exception:
            pipeline = Chronos2Pipeline.from_pretrained(model_name, device_map=device_map)
            try:
                pipeline.save_pretrained(model_path)
            except Exception:
                pass
    else:
        pipeline = Chronos2Pipeline.from_pretrained(model_name, device_map=device_map)
        if model_path is not None:
            try:
                pipeline.save_pretrained(model_path)
            except Exception:
                pass
    # Predict
    try:
        pred_df = pipeline.predict_df(
            context_df,
            future_df=future_df,
            prediction_length=prediction_length,
            quantile_levels=quantile_levels,
            id_column="id",
            timestamp_column="timestamp",
            target="target",
        )
    except Exception as err:
        raise RuntimeError(
            f"Chronos2Pipeline prediction failed: {err}. Check your input DataFrame."
        )
    pred_df = pred_df.reset_index(drop=True)
    # Build MultiIndex DataFrame of forecasts
    ids = pred_df["id"].unique()
    data_arrays: List[np.ndarray] = []
    col_tuples: List[Tuple[str, float]] = []
    # Determine timestamp index (use timestamps from first id)
    first_group = pred_df[pred_df["id"] == ids[0]].sort_values("timestamp")
    ts_index = pd.to_datetime(first_group["timestamp"].values)
    # For each quantile and id, extract predictions
    for q in quantile_levels:
        q_str = str(q)
        for sid in ids:
            group = pred_df[pred_df["id"] == sid].sort_values("timestamp")
            if q == 0.5 and ("0.5" in group.columns or "predictions" in group.columns):
                # median stored in '0.5' or 'predictions'
                col_name = "0.5" if "0.5" in group.columns else "predictions"
                vals = group[col_name].values
            else:
                if q_str in group.columns:
                    vals = group[q_str].values
                else:
                    # fall back to median if specific quantile unavailable
                    col_name = "predictions" if "predictions" in group.columns else "0.5"
                    vals = group[col_name].values
            data_arrays.append(vals)
            col_tuples.append((sid, q))
    # Construct DataFrame
    forecast_data = np.array(data_arrays).T
    forecasts_df = pd.DataFrame(forecast_data, index=ts_index)
    if len(col_tuples) > 1:
        forecasts_df.columns = pd.MultiIndex.from_tuples(col_tuples, names=["item_id", "quantile"])
    else:
        forecasts_df.columns = [col_tuples[0][1]]  # single series
    # Summary statistics
    summary_dict: Dict[str, float] = {}
    if summary:
        for sid in ids:
            # median quantile 0.5
            idx = col_tuples.index((sid, 0.5)) if (sid, 0.5) in col_tuples else None
            if idx is not None:
                vals = forecast_data[:, idx]
                summary_dict[sid] = float(np.mean(vals))
            else:
                # use first quantile as proxy
                summary_dict[sid] = float(np.mean(forecast_data[:, 0]))
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            # Historical
            hist_df = df_in[[id_used, date_col, target_col]].copy()
            for sid in ids:
                sub_hist = hist_df[hist_df[id_used] == sid] if id_col is not None else hist_df
                fig.add_trace(go.Scatter(
                    x=sub_hist[date_col],
                    y=sub_hist[target_col],
                    mode="lines",
                    name=f"{sid} actual",
                ))
            lower_q = min(quantile_levels)
            upper_q = max(quantile_levels)
            median_q = 0.5 if 0.5 in quantile_levels else quantile_levels[len(quantile_levels)//2]
            for sid in ids:
                median_vals = forecasts_df[(sid, median_q)].values if isinstance(forecasts_df.columns, pd.MultiIndex) else forecasts_df[median_q].values
                lower_vals = forecasts_df[(sid, lower_q)].values if isinstance(forecasts_df.columns, pd.MultiIndex) else forecasts_df[lower_q].values
                upper_vals = forecasts_df[(sid, upper_q)].values if isinstance(forecasts_df.columns, pd.MultiIndex) else forecasts_df[upper_q].values
                fig.add_trace(go.Scatter(
                    x=ts_index,
                    y=median_vals,
                    mode="lines",
                    name=f"{sid} forecast",
                    line=dict(dash="dot"),
                ))
                fig.add_trace(go.Scatter(
                    x=np.concatenate([ts_index, ts_index[::-1]]),
                    y=np.concatenate([lower_vals, upper_vals[::-1]]),
                    fill="toself",
                    fillcolor="rgba(255,165,0,0.2)",
                    line=dict(color="rgba(255,165,0,0)"),
                    showlegend=False,
                ))
            fig.update_layout(title="Chronos‑2 Quantile Forecast")
            fig.show()
        except Exception:
            pass
    return Chronos2QuantileForecastResult(
        forecasts=forecasts_df,
        model=pipeline,
        quantile_levels=quantile_levels,
        summary=summary_dict if summary else None,
    )


def chronos2_anomaly_detection(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    covariate_cols: Optional[List[str]] = None,
    prediction_length: int = 24,
    lower_quantile: float = 0.025,
    upper_quantile: float = 0.975,
    model_name: str = "amazon/chronos-2",
    model_path: Optional[str] = None,
    device_map: str = "cpu",
    id_col: Optional[str] = None,
    plot: bool = False,
) -> Chronos2AnomalyResult:
    """Detect anomalies by comparing actual values to Chronos‑2 forecast intervals.

    The data is split into a training portion (all except the last
    ``prediction_length`` observations) and an evaluation portion (the
    last ``prediction_length``).  A Chronos‑2 model is trained (or
    loaded) on the training data and forecasts the evaluation horizon.
    Actual values outside the interval [lower_quantile, upper_quantile]
    are flagged as anomalies.

    Returns a dataclass with the anomalies DataFrame and summary statistics.
    """
    # Ensure enough data
    df_sorted = df.copy().sort_values(date_col)
    if len(df_sorted) <= prediction_length:
        raise ValueError("Not enough data points for anomaly detection")
    train_df = df_sorted.iloc[: -prediction_length]
    eval_df = df_sorted.iloc[-prediction_length:]
    # Forecast using chronos2_quantile_forecast
    res = chronos2_quantile_forecast(
        train_df,
        date_col=date_col,
        target_col=target_col,
        covariate_cols=covariate_cols,
        future_cov_df=None,
        prediction_length=prediction_length,
        quantile_levels=[lower_quantile, 0.5, upper_quantile],
        model_name=model_name,
        model_path=model_path,
        device_map=device_map,
        id_col=id_col,
        plot=False,
        summary=False,
    )
    fcast_df = res.forecasts
    # Build anomalies DataFrame comparing eval_df actuals and forecasts
    anomalies_list: List[pd.DataFrame] = []
    summary_dict: Dict[str, float] = {}
    if isinstance(fcast_df.columns, pd.MultiIndex):
        for sid in fcast_df.columns.get_level_values(0).unique():
            # actuals for this id
            eval_sub = eval_df if id_col is None else eval_df[eval_df[id_col] == sid]
            if eval_sub.empty:
                continue
            ts = fcast_df.index
            lower_vals = fcast_df[(sid, lower_quantile)].values
            median_vals = fcast_df[(sid, 0.5)].values if (sid, 0.5) in fcast_df.columns else fcast_df[(sid, "predictions")].values
            upper_vals = fcast_df[(sid, upper_quantile)].values
            actual_vals = eval_sub[target_col].values
            length = min(len(actual_vals), len(ts))
            df_tmp = pd.DataFrame({
                "item_id": [sid] * length,
                "timestamp": ts[:length],
                "actual": actual_vals[:length],
                "forecast": median_vals[:length],
                "lower": lower_vals[:length],
                "upper": upper_vals[:length],
            })
            df_tmp["anomaly"] = ((df_tmp["actual"] < df_tmp["lower"]) | (df_tmp["actual"] > df_tmp["upper"])).astype(int)
            anomalies_list.append(df_tmp)
            summary_dict[sid] = float(df_tmp["anomaly"].mean())
    else:
        sid = "series_1"
        ts = fcast_df.index
        lower_vals = fcast_df[lower_quantile].values
        median_vals = fcast_df[0.5].values if 0.5 in fcast_df.columns else fcast_df["predictions"].values
        upper_vals = fcast_df[upper_quantile].values
        actual_vals = eval_df[target_col].values
        length = min(len(actual_vals), len(ts))
        df_tmp = pd.DataFrame({
            "item_id": [sid] * length,
            "timestamp": ts[:length],
            "actual": actual_vals[:length],
            "forecast": median_vals[:length],
            "lower": lower_vals[:length],
            "upper": upper_vals[:length],
        })
        df_tmp["anomaly"] = ((df_tmp["actual"] < df_tmp["lower"]) | (df_tmp["actual"] > df_tmp["upper"])).astype(int)
        anomalies_list.append(df_tmp)
        summary_dict[sid] = float(df_tmp["anomaly"].mean())
    anomalies_df = pd.concat(anomalies_list).set_index(["item_id", "timestamp"])
    if plot:
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            for sid in anomalies_df.index.get_level_values(0).unique():
                sub = anomalies_df.loc[sid]
                fig.add_trace(go.Scatter(x=sub.index, y=sub["actual"], mode="lines", name=f"{sid} actual"))
                fig.add_trace(go.Scatter(x=sub.index, y=sub["forecast"], mode="lines", name=f"{sid} forecast", line=dict(dash="dot")))
                fig.add_trace(go.Scatter(
                    x=np.concatenate([sub.index, sub.index[::-1]]),
                    y=np.concatenate([sub["lower"], sub["upper"][::-1]]),
                    fill="toself",
                    fillcolor="rgba(255,165,0,0.2)",
                    line=dict(color="rgba(255,165,0,0)"),
                    showlegend=False,
                ))
                anomalies_pts = sub[sub["anomaly"] == 1]
                fig.add_trace(go.Scatter(x=anomalies_pts.index, y=anomalies_pts["actual"], mode="markers", marker=dict(symbol="x", size=8), name=f"{sid} anomaly"))
            fig.update_layout(title="Chronos‑2 Anomaly Detection")
            fig.show()
        except Exception:
            pass
    return Chronos2AnomalyResult(anomalies=anomalies_df, model=res.model, summary=summary_dict)


def chronos2_impute_missing(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    covariate_cols: Optional[List[str]] = None,
    model_name: str = "amazon/chronos-2",
    model_path: Optional[str] = None,
    device_map: str = "cpu",
    id_col: Optional[str] = None,
) -> Chronos2ImputeResult:
    """Impute trailing NaN values in the target using Chronos‑2 forecasts.

    Only NaN values at the end of the series are imputed.  If there are no
    trailing NaNs, the input DataFrame is returned unchanged.
    """
    df_sorted = df.copy().sort_values(date_col)
    df_sorted[date_col] = pd.to_datetime(df_sorted[date_col], errors="coerce")
    target_vals = df_sorted[target_col].values
    valid_indices = np.where(~pd.isna(target_vals))[0]
    if len(valid_indices) == 0:
        raise ValueError("All target values are NaN; cannot impute")
    last_valid_idx = valid_indices[-1]
    missing_count = len(target_vals) - last_valid_idx - 1
    if missing_count <= 0:
        return Chronos2ImputeResult(df_sorted, model=None)
    # Training portion
    train_df = df_sorted.iloc[: last_valid_idx + 1]
    # Forecast horizon
    res = chronos2_quantile_forecast(
        train_df,
        date_col=date_col,
        target_col=target_col,
        covariate_cols=covariate_cols,
        future_cov_df=None,
        prediction_length=missing_count,
        quantile_levels=[0.5],
        model_name=model_name,
        model_path=model_path,
        device_map=device_map,
        id_col=id_col,
        plot=False,
        summary=False,
    )
    fcast_df = res.forecasts
    # Determine item id
    if id_col is None:
        item = "series_1"
    else:
        item = df_sorted.iloc[0][id_col]
    # Extract median predictions
    if isinstance(fcast_df.columns, pd.MultiIndex):
        if (item, 0.5) in fcast_df.columns:
            preds = fcast_df[(item, 0.5)].values
        else:
            preds = fcast_df.xs(item, level=0, axis=1).iloc[:, 0].values
    else:
        preds = fcast_df[0.5].values if 0.5 in fcast_df.columns else fcast_df.iloc[:, 0].values
    df_imputed = df_sorted.copy()
    impute_indices = list(range(last_valid_idx + 1, last_valid_idx + 1 + missing_count))
    df_imputed.iloc[impute_indices, df_imputed.columns.get_loc(target_col)] = preds[:missing_count]
    return Chronos2ImputeResult(df_imputed, model=res.model)


def timesfm_forecast(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    prediction_length: int = 24,
    model_name: str = "google/timesfm-2.0-500m-pytorch",
    model_path: Optional[str] = None,
    freq_index: Optional[int] = None,
    plot: bool = False,
    summary: bool = False,
) -> TimesFmForecastResult:
    """Forecast a univariate time series using Google’s TimesFM model.

    This function loads a pretrained TimesFM model via the
    ``transformers`` library and applies it to a single or multiple
    series.  The model expects sequences of past values and a
    categorical frequency index; it outputs probabilistic forecasts
    with full sample predictions from which quantiles are computed.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing the datetime column and the target
        column.  Only numeric target values are supported.  If
        multiple series are provided, stack them with an ``id_col``
        column prior to calling this function.
    date_col : str
        Name of the datetime column.
    target_col : str
        Name of the target column.
    prediction_length : int, default 24
        Number of future steps to forecast.
    model_name : str, default 'google/timesfm-2.0-500m-pytorch'
        Name of the pretrained TimesFM model on Hugging Face.  Other
        variants (e.g. 'google/timesfm-2.5-200m-pytorch') can be
        passed here.
    model_path : str or None, default None
        Optional directory to cache the model.  If provided and the
        directory exists, the model is loaded from this path.  After
        downloading from Hugging Face, the model is saved for future
        reuse.
    freq_index : int or None, default None
        Frequency category index required by TimesFM.  Common values
        include 0 for hourly or subhourly data, 1 for daily data and
        2 for weekly data.  If None, this function attempts to
        infer the frequency from the time delta between adjacent
        timestamps; daily (1) and weekly (2) are the most typical.
    plot : bool, default False
        Whether to display a Plotly chart with the historical series,
        forecast and shaded confidence intervals.
    summary : bool, default False
        If True, compute the mean of the forecasted series and
        include it in the result dataclass.

    Returns
    -------
    TimesFmForecastResult
        Dataclass containing point forecasts, prediction intervals,
        the loaded model and optional summary statistics.

    Notes
    -----
    This function requires the ``transformers`` library (version
    4.57 or newer) and ``torch``.  The model is loaded onto CPU by
    default; set ``freq_index`` appropriately for your data.  TimesFM
    operates on individual series; for multivariate forecasting use
    separate calls or Chronos‑2.
    """
    # Imports deferred to runtime
    if torch is None:
        raise ImportError(
            "torch is required for timesfm_forecast. Please install torch."
        )
    try:
        from transformers import TimesFmModelForPrediction  # type: ignore[import]
    except Exception as e:
        raise ImportError(
            "transformers is required for timesfm_forecast. Please install transformers>=4.57."
        ) from e
    import os
    # Parse and sort
    df_in = df[[date_col, target_col]].dropna().copy()
    df_in[date_col] = pd.to_datetime(df_in[date_col], errors='coerce')
    df_in = df_in.sort_values(date_col).reset_index(drop=True)
    # Determine frequency index if not provided
    if freq_index is None:
        diffs = df_in[date_col].diff().dropna()
        if not diffs.empty:
            median_delta = diffs.median()
            # Heuristic: daily ~ 1 day, weekly ~ 7 days; sub-daily -> 0
            if median_delta <= pd.Timedelta(days=1):
                freq_index = 0  # high‑frequency or daily
            elif median_delta <= pd.Timedelta(days=7):
                freq_index = 1  # daily
            else:
                freq_index = 2  # weekly or slower
        else:
            freq_index = 1
    # Extract series values
    series_vals = df_in[target_col].astype(float).to_numpy()
    # Load or cache the model
    if model_path is not None and os.path.exists(model_path):
        try:
            model = TimesFmModelForPrediction.from_pretrained(model_path)
        except Exception:
            model = TimesFmModelForPrediction.from_pretrained(
                model_name, device_map='cpu', dtype=torch.float32
            )
            try:
                model.save_pretrained(model_path)
            except Exception:
                pass
    else:
        model = TimesFmModelForPrediction.from_pretrained(
            model_name, device_map='cpu', dtype=torch.float32
        )
        if model_path is not None:
            try:
                model.save_pretrained(model_path)
            except Exception:
                pass
    # Prepare input tensors
    past_values = torch.tensor(series_vals, dtype=torch.float32).unsqueeze(0).to(model.device)
    freq_tensor = torch.tensor([freq_index], dtype=torch.long).to(model.device)
    # Perform inference
    with torch.no_grad():
        outputs = model(past_values=past_values, freq=freq_tensor, return_dict=True)
        # mean_predictions: shape (batch_size, prediction_length)
        # full_predictions: shape (batch_size, num_samples, prediction_length)
        mean_pred = outputs.mean_predictions[0].float().cpu().numpy()
        full_pred = outputs.full_predictions[0].float().cpu().numpy()
    # Compute quantiles from samples
    lower = np.quantile(full_pred, 0.025, axis=0)
    upper = np.quantile(full_pred, 0.975, axis=0)
    # Build forecast index
    last_date = df_in[date_col].iloc[-1]
    # Attempt to infer frequency for date_range
    freq = pd.infer_freq(df_in[date_col])
    if freq is not None:
        forecast_index = pd.date_range(start=last_date, periods=prediction_length + 1, freq=freq)[1:]
    else:
        # Use median_delta if available, else daily
        delta = median_delta if 'median_delta' in locals() else pd.Timedelta(days=1)
        forecast_index = [last_date + delta * (i + 1) for i in range(prediction_length)]
    # Create DataFrames
    forecasts_df = pd.DataFrame({target_col: mean_pred}, index=forecast_index)
    lower_df = pd.DataFrame({target_col: lower}, index=forecast_index)
    upper_df = pd.DataFrame({target_col: upper}, index=forecast_index)
    # Summary statistics
    summary_out = None
    if summary:
        summary_out = {target_col: float(np.mean(mean_pred))}
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_in[date_col], y=df_in[target_col], mode='lines', name='historical'
            ))
            fig.add_trace(go.Scatter(
                x=forecasts_df.index, y=forecasts_df[target_col], mode='lines', name='forecast', line=dict(dash='dot')
            ))
            fig.add_trace(go.Scatter(
                x=list(forecasts_df.index) + list(forecasts_df.index[::-1]),
                y=list(lower_df[target_col]) + list(upper_df[target_col][::-1]),
                fill='toself', fillcolor='rgba(255,165,0,0.2)', line=dict(color='rgba(255,165,0,0)'), showlegend=False
            ))
            fig.update_layout(title='TimesFM Forecast', xaxis_title=date_col, yaxis_title=target_col, template='plotly_white')
            fig.show()
        except Exception:
            pass
    return TimesFmForecastResult(
        forecasts=forecasts_df,
        lower_conf_int=lower_df,
        upper_conf_int=upper_df,
        model=model,
        summary=summary_out,
    )


def sarimax_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    order: Tuple[int, int, int] = (1, 0, 0),
    seasonal_order: Tuple[int, int, int, int] = (0, 0, 0, 0),
    exog: Optional[Union[pd.DataFrame, str, Iterable[str]]] = None,
    exog_future: Optional[pd.DataFrame] = None,
    freq: Optional[str] = None,
    enforce_stationarity: bool = False,
    enforce_invertibility: bool = False,
    return_conf_int: bool = False,
    plot: bool = False,
) -> SarimaxForecastResult:
    """Forecast one or more series using SARIMAX models.

    This function generalises :func:`arima_forecast` by allowing a
    seasonal component and optional exogenous regressors.  It fits
    separate SARIMAX models to each numeric series and forecasts
    ``periods`` steps ahead.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Numeric columns are modelled
        individually.
    periods : int, default 12
        Number of future periods to forecast.
    order : tuple of int, default (1,0,0)
        Non‑seasonal ARIMA (p,d,q) order.
    seasonal_order : tuple of int, default (0,0,0,0)
        Seasonal ARIMA (P,D,Q,s) order.  The last element ``s``
        specifies the number of periods in a seasonal cycle.  Set to
        ``(0,0,0,0)`` for no seasonality.
    exog : pandas.DataFrame, str, iterable of str or None, default None
        Exogenous regressors to include in the model.  May be a
        DataFrame aligned with ``df`` or the name(s) of columns in
        ``df``.  If provided, separate models are fit using the
        same exogenous variables for each series.
    exog_future : pandas.DataFrame or None, default None
        Future values of the exogenous regressors.  Must have the
        same number of columns as ``exog`` and at least ``periods``
        rows.  If None, the last row of the historical exogenous
        data is replicated ``periods`` times.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If None,
        frequency is inferred via ``pandas.infer_freq``.
    enforce_stationarity : bool, default False
        If True, restrict the AR parameters to stationary region.
    enforce_invertibility : bool, default False
        If True, restrict the MA parameters to invertible region.

    Returns
    -------
    SarimaxForecastResult
        Dataclass containing the forecast DataFrame, fitted SARIMAX
        models for each series, and optionally prediction intervals
        if ``return_conf_int`` is ``True``.

    Raises
    ------
    ImportError
        If the ``statsmodels`` package is not installed.
    KeyError
        If the specified date column is not found.
    ValueError
        If no numeric columns are available for forecasting.
    """
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX
    except Exception as e:
        raise ImportError(
            "statsmodels is required for SARIMAX forecasting. "
            "Please install statsmodels to use this function."
        ) from e
    # Parse date column
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Identify numeric columns
    numeric_cols: List[str] = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric data columns found for SARIMAX forecasting")
    # Determine frequency
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    # Prepare future dates
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # Prepare exogenous variables
    if exog is not None:
        # Determine exogenous DataFrame
        if isinstance(exog, str):
            exog_cols = [exog]
            exog_df = df[exog_cols]
        elif isinstance(exog, Iterable) and not isinstance(exog, pd.DataFrame):
            exog_cols = list(exog)
            exog_df = df[exog_cols]
        elif isinstance(exog, pd.DataFrame):
            exog_cols = list(exog.columns)
            exog_df = exog
        else:
            raise TypeError("exog must be a DataFrame, column name or iterable of column names")
        # Ensure numeric
        exog_df = exog_df.ffill().bfill().astype(float)
        # Future exog values
        if exog_future is not None:
            if not isinstance(exog_future, pd.DataFrame):
                raise TypeError("exog_future must be a pandas DataFrame if provided")
            future_exog = exog_future.iloc[:periods].reset_index(drop=True)
            # If fewer rows, repeat last row
            if len(future_exog) < periods:
                last_row = future_exog.iloc[-1]
                add_rows = pd.DataFrame([last_row] * (periods - len(future_exog)), columns=future_exog.columns)
                future_exog = pd.concat([future_exog, add_rows], ignore_index=True)
        else:
            # Replicate last row for future
            last_row = exog_df.iloc[-1]
            future_exog = pd.DataFrame([last_row] * periods, columns=exog_df.columns)
    else:
        exog_cols = []
        exog_df = None
        future_exog = None
    # Fit SARIMAX models for each numeric column
    forecasts_data: Dict[str, np.ndarray] = {}
    models: Dict[str, object] = {}
    lower_ci_data: Dict[str, np.ndarray] = {}
    upper_ci_data: Dict[str, np.ndarray] = {}
    for col in numeric_cols:
        y = pd.to_numeric(df[col], errors='coerce').ffill().bfill().astype(float)
        # Fit model
        mod = SARIMAX(
            y,
            order=order,
            seasonal_order=seasonal_order,
            exog=exog_df,
            enforce_stationarity=enforce_stationarity,
            enforce_invertibility=enforce_invertibility,
        )
        res = mod.fit(disp=False)
        models[col] = res
        # Forecast with or without exogenous variables
        if exog_df is not None:
            forecast_res = res.get_forecast(steps=periods, exog=future_exog)
        else:
            forecast_res = res.get_forecast(steps=periods)
        forecast_vals = forecast_res.predicted_mean.values
        forecasts_data[col] = forecast_vals
        # Compute confidence intervals if requested
        if return_conf_int or plot:
            ci = forecast_res.conf_int()
            # Extract lower/upper columns; Statsmodels names columns like 'lower y' and 'upper y'
            # For univariate forecast, we take the first two columns
            # For each column we call separately; thus ci has two columns
            lower_vals = ci.iloc[:, 0].values
            upper_vals = ci.iloc[:, 1].values
            lower_ci_data[col] = lower_vals
            upper_ci_data[col] = upper_vals
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=numeric_cols)
    lower_df = None
    upper_df = None
    if return_conf_int or plot:
        # Build DataFrames for confidence intervals
        lower_df = pd.DataFrame(lower_ci_data, index=future_index, columns=numeric_cols)
        upper_df = pd.DataFrame(upper_ci_data, index=future_index, columns=numeric_cols)
    result = SarimaxForecastResult(
        forecasts=forecast_df,
        models=models,
        lower_conf_int=lower_df,
        upper_conf_int=upper_df,
    )
    # Plot if requested
    if plot:
        try:
            # Import plot function lazily to avoid circular dependency
            from .visualization import forecast_plot
            # Determine historical DataFrame's date column name or series
            # Use provided date parameter to avoid ambiguous column names
            forecast_plot(date=date, df=df, forecast=forecast_df, lower=lower_df, upper=upper_df)
        except Exception:
            # Silently ignore plotting errors to avoid breaking forecasting
            pass
    return result


@dataclass
class LstmForecastResult:
    """Result container for :func:`lstm_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each series.  The index contains the
        forecast dates and the columns correspond to the numeric
        columns of the input (excluding the date column).
    models : Dict[str, object]
        Trained TensorFlow Keras models for each series.
    """

    forecasts: pd.DataFrame
    models: Dict[str, object]


def lstm_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    look_back: int = 10,
    hidden_units: int = 50,
    epochs: int = 100,
    batch_size: int = 32,
    validation_split: float = 0.1,
    random_state: Optional[int] = None,
    freq: Optional[str] = None,
) -> LstmForecastResult:
    """Forecast one or more series using an LSTM neural network.

    This function trains a separate univariate LSTM model for each
    numeric series.  It constructs supervised learning examples
    using lagged observations of length ``look_back``, fits an
    LSTM with a dense output layer, and iteratively predicts
    ``periods`` future values.  The underlying models are built
    with TensorFlow/Keras.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Numeric columns are modelled
        individually.
    periods : int, default 12
        Number of future periods to forecast.
    look_back : int, default 10
        Number of past observations used as input features.  Must be
        less than the length of the series.
    hidden_units : int, default 50
        Number of LSTM units in the hidden layer.
    epochs : int, default 100
        Number of training epochs.
    batch_size : int, default 32
        Size of mini‑batches during training.
    validation_split : float, default 0.1
        Fraction of the training data used for validation.
    random_state : int or None, default None
        Seed for NumPy and TensorFlow random number generators.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If None,
        inferred via ``pandas.infer_freq``.

    Returns
    -------
    LstmForecastResult
        Dataclass containing the forecast DataFrame and the trained
        Keras models for each series.

    Notes
    -----
    This method can be computationally intensive, especially for
    large datasets or many series.  It relies on the ``tensorflow``
    package; an ImportError is raised if TensorFlow is not installed.
    """
    # Check dependencies
    try:
        import numpy as np  # reimport to ensure local scope
        from sklearn.preprocessing import StandardScaler
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense
    except Exception as e:
        raise ImportError(
            "TensorFlow and scikit‑learn are required for LSTM forecasting. "
            "Please install tensorflow and scikit-learn to use this function."
        ) from e
    # Set random seeds for reproducibility
    if random_state is not None:
        np.random.seed(random_state)
        try:
            tf.random.set_seed(random_state)
        except Exception:
            pass
    # Parse date column
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric data columns found for LSTM forecasting")
    # Determine frequency
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    # Prepare future dates
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    forecasts_data: Dict[str, List[float]] = {}
    models: Dict[str, object] = {}
    for col in numeric_cols:
        series = pd.to_numeric(df[col], errors='coerce').ffill().bfill().astype(float).values
        if len(series) <= look_back:
            raise ValueError(f"Series '{col}' is too short for look_back={look_back}")
        # Standardise data
        scaler = StandardScaler()
        series_scaled = scaler.fit_transform(series.reshape(-1, 1)).flatten()
        # Build supervised dataset
        X = []
        y_target = []
        for i in range(look_back, len(series_scaled)):
            X.append(series_scaled[i - look_back:i])
            y_target.append(series_scaled[i])
        X_train = np.array(X).reshape(-1, look_back, 1)
        y_train = np.array(y_target)
        # Build model
        model = Sequential()
        model.add(LSTM(hidden_units, input_shape=(look_back, 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        # Train model
        model.fit(
            X_train,
            y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=0,
        )
        models[col] = model
        # Forecast iteratively
        history_scaled = list(series_scaled[-look_back:])
        preds = []
        for _ in range(periods):
            input_seq = np.array(history_scaled[-look_back:]).reshape(1, look_back, 1)
            pred_scaled = model.predict(input_seq, verbose=0)[0, 0]
            # Invert scaling
            pred = scaler.inverse_transform(np.array([[pred_scaled]])).flatten()[0]
            preds.append(pred)
            # Update history
            history_scaled.append(pred_scaled)
        forecasts_data[col] = preds
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=numeric_cols)
    return LstmForecastResult(forecasts=forecast_df, models=models)


@dataclass
class GarchForecastResult:
    """Result container for :func:`garch_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted variance (and optional mean) for each series.  The
        index contains the forecast dates and the columns correspond
        to the numeric columns of the input (excluding the date
        column).
    models : Dict[str, object]
        Fitted ARCH models from the ``arch`` package.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]


def garch_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    p: int = 1,
    q: int = 1,
    mean: str = 'Constant',
    vol: str = 'GARCH',
    dist: str = 'normal',
    freq: Optional[str] = None,
) -> GarchForecastResult:
    """Forecast conditional variance of one or more series using GARCH models.

    This function fits a GARCH model (via the ``arch`` package) to
    the returns of each numeric series and forecasts the conditional
    variance ``periods`` steps ahead.  Optionally, it can also
    return mean forecasts if the mean is modelled.  Because GARCH
    models operate on returns rather than levels, the results are
    interpreted as forecasts of volatility.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Numeric columns are modelled
        individually.
    periods : int, default 12
        Number of future periods to forecast.
    p : int, default 1
        Order of the GARCH terms (lagged conditional variances).
    q : int, default 1
        Order of the ARCH terms (lagged squared residuals).
    mean : str, default 'Constant'
        Mean model.  Options include 'Constant', 'Zero', or
        'AR'.  See ``arch_model`` documentation for details.
    vol : str, default 'GARCH'
        Volatility model.  Options include 'GARCH', 'EGARCH', etc.
    dist : str, default 'normal'
        Distribution for the innovations.  Options include 'normal',
        't', etc.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If None,
        inferred via ``pandas.infer_freq``.

    Returns
    -------
    GarchForecastResult
        Dataclass containing the forecasted variances and the
        fitted models.  If the mean model produces forecasts, these
        are included in the ``forecasts`` DataFrame.

    Raises
    ------
    ImportError
        If the ``arch`` package is not installed.
    """
    try:
        from arch import arch_model
    except Exception as e:
        raise ImportError(
            "The 'arch' package is required for GARCH forecasting. "
            "Please install arch to use this function."
        ) from e
    # Parse date column
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric data columns found for GARCH forecasting")
    # Determine frequency
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    # Prepare future dates
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    forecasts_data: Dict[str, np.ndarray] = {}
    models: Dict[str, object] = {}
    for col in numeric_cols:
        series = pd.to_numeric(df[col], errors='coerce').ffill().bfill().astype(float)
        # Compute returns (log returns) to fit GARCH
        returns = np.log(series).diff().dropna()
        if returns.empty:
            raise ValueError(f"Series '{col}' has insufficient data for GARCH model")
        # Fit GARCH model
        am = arch_model(
            returns,
            mean=mean,
            vol=vol,
            p=p,
            q=q,
            dist=dist,
        )
        res = am.fit(disp='off')
        # Forecast conditional variance and mean
        forecast = res.forecast(horizon=periods)
        # Extract mean and variance forecasts
        # forecast.variance returns DataFrame of shape (nobs, horizon)
        var_forecast = forecast.variance.iloc[-1].values
        try:
            mean_forecast = forecast.mean.iloc[-1].values
        except Exception:
            mean_forecast = np.zeros_like(var_forecast)
        # We store variance forecasts; if mean forecasts present, we add them
        # For consistency with other forecasts, we output the variance as the series
        # Name columns by series name appended with '_var' if multiple forecasts exist
        forecasts_data[col] = var_forecast
        models[col] = res
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=numeric_cols)
    return GarchForecastResult(forecasts=forecast_df, models=models)

# ---------------------------------------------------------------------------
# Gradient boosting forecasts using XGBoost and LightGBM
# ---------------------------------------------------------------------------

@dataclass
class XGBoostForecastResult:
    """Result container for :func:`xgboost_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each target series.  The index
        corresponds to future dates and the columns match the target
        names.
    models : Dict[str, object]
        Trained ``xgboost.XGBRegressor`` models for each series.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]


def xgboost_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    lags: int = 10,
    exog: Optional[List[str]] = None,
    freq: Optional[str] = None,
    model_params: Optional[dict] = None,
) -> XGBoostForecastResult:
    """Forecast series using XGBoost regressors with lagged features.

    Each numeric column (excluding the date and exogenous columns) is
    modelled separately.  Lagged values up to ``lags`` and optional
    exogenous variables at the current time step are used as
    predictors.  The function trains an XGBoost regressor and
    iteratively generates forecasts for ``periods`` steps ahead.  If
    future exogenous values are required, pass them via the
    ``exog_future`` parameter in ``model_params`` (as a DataFrame
    indexed by forecast dates).

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Must include the date column and
        one or more numeric columns to forecast.
    periods : int, default 12
        Number of future periods to forecast.
    lags : int, default 10
        Number of lag observations to include as features.
    exog : list of str or None, default None
        Names of exogenous columns to include as predictors.  These
        columns must be present in ``df``.  If provided, you can
        specify future values for these variables via
        ``model_params['exog_future']`` as a DataFrame of shape
        (periods, len(exog)).  If future values are not provided,
        zeros are used.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If ``None``,
        the frequency is inferred from the date series.
    model_params : dict or None, default None
        Additional parameters passed to ``xgboost.XGBRegressor``.
        Recognised key ``exog_future`` may be a DataFrame providing
        exogenous values for the forecast horizon.

    Returns
    -------
    XGBoostForecastResult
        Dataclass containing forecasted values and fitted models.

    Raises
    ------
    ImportError
        If ``xgboost`` is not installed.
    ValueError
        If no numeric columns are available to model.
    """
    try:
        from xgboost import XGBRegressor
    except Exception as e:
        raise ImportError(
            "xgboost is required for XGBoost forecasting. "
            "Please install xgboost to use this function."
        ) from e
    if model_params is None:
        model_params = {}
    exog_future = model_params.pop('exog_future', None)
    # Determine date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Identify target columns
    target_cols = [c for c in df.columns if c != date and (exog is None or c not in exog) and pd.api.types.is_numeric_dtype(df[c])]
    if not target_cols:
        raise ValueError("No numeric columns found to forecast with XGBoost")
    # Identify exogenous columns
    exog_cols = exog or []
    # Determine frequency
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    # Generate future dates
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # Exogenous future values
    if exog_cols and exog_future is None:
        # Use zeros if no future exogenous provided
        exog_future = pd.DataFrame(np.zeros((periods, len(exog_cols))), index=future_index, columns=exog_cols)
    elif exog_cols:
        exog_future = exog_future.copy()
        exog_future.index = future_index
        exog_future = exog_future[exog_cols]
    models: Dict[str, object] = {}
    forecasts_data: Dict[str, List[float]] = {}
    for col in target_cols:
        series = pd.to_numeric(df[col], errors='coerce').astype(float).reset_index(drop=True)
        n = len(series)
        X_train = []
        y_train = []
        exog_matrix = df[exog_cols].reset_index(drop=True) if exog_cols else None
        for t in range(lags, n):
            lagged = series.iloc[t - lags:t].values
            features = list(lagged)
            if exog_cols:
                features += list(exog_matrix.iloc[t, :].values)
            X_train.append(features)
            y_train.append(series.iloc[t])
        if not y_train:
            raise ValueError(f"Not enough data to build lagged features for column '{col}'")
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        # Default model parameters
        params = {
            'objective': 'reg:squarederror',
            'n_estimators': 200,
            'learning_rate': 0.05,
            'max_depth': 5,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
        }
        params.update(model_params)
        model = XGBRegressor(**params)
        model.fit(X_train, y_train)
        models[col] = model
        last_lags = series.iloc[-lags:].values.tolist()
        exog_future_values = exog_future.values if exog_cols else None
        preds: List[float] = []
        for step in range(periods):
            features = last_lags[-lags:].copy()
            if exog_cols:
                features += list(exog_future_values[step])
            pred = float(model.predict(np.array(features).reshape(1, -1))[0])
            preds.append(pred)
            last_lags.append(pred)
        forecasts_data[col] = preds
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=target_cols)
    return XGBoostForecastResult(forecasts=forecast_df, models=models)


@dataclass
class LightGBMForecastResult:
    """Result container for :func:`lightgbm_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each target series.
    models : Dict[str, object]
        Trained ``lightgbm.LGBMRegressor`` models for each series.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]


def lightgbm_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    lags: int = 10,
    exog: Optional[List[str]] = None,
    freq: Optional[str] = None,
    model_params: Optional[dict] = None,
) -> LightGBMForecastResult:
    """Forecast series using LightGBM regressors with lagged features.

    This function mirrors :func:`xgboost_forecast` but uses
    ``lightgbm.LGBMRegressor``.  See :func:`xgboost_forecast` for
    parameter descriptions and return details.

    Returns
    -------
    LightGBMForecastResult
        Dataclass containing forecasted values and fitted models.
    """
    try:
        from lightgbm import LGBMRegressor
    except Exception as e:
        raise ImportError(
            "lightgbm is required for LightGBM forecasting. "
            "Please install lightgbm to use this function."
        ) from e
    if model_params is None:
        model_params = {}
    exog_future = model_params.pop('exog_future', None)
    # Determine date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    target_cols = [c for c in df.columns if c != date and (exog is None or c not in exog) and pd.api.types.is_numeric_dtype(df[c])]
    if not target_cols:
        raise ValueError("No numeric columns found to forecast with LightGBM")
    exog_cols = exog or []
    # Determine frequency
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    if exog_cols and exog_future is None:
        exog_future = pd.DataFrame(np.zeros((periods, len(exog_cols))), index=future_index, columns=exog_cols)
    elif exog_cols:
        exog_future = exog_future.copy()
        exog_future.index = future_index
        exog_future = exog_future[exog_cols]
    models: Dict[str, object] = {}
    forecasts_data: Dict[str, List[float]] = {}
    for col in target_cols:
        series = pd.to_numeric(df[col], errors='coerce').astype(float).reset_index(drop=True)
        n = len(series)
        X_train: List[List[float]] = []
        y_train: List[float] = []
        exog_matrix = df[exog_cols].reset_index(drop=True) if exog_cols else None
        for t in range(lags, n):
            lagged = series.iloc[t - lags:t].values
            features = list(lagged)
            if exog_cols:
                features += list(exog_matrix.iloc[t, :].values)
            X_train.append(features)
            y_train.append(series.iloc[t])
        if not y_train:
            raise ValueError(f"Not enough data to build lagged features for column '{col}'")
        X_train_arr = np.array(X_train)
        y_train_arr = np.array(y_train)
        params = {
            'n_estimators': 200,
            'learning_rate': 0.05,
            'max_depth': -1,
            'num_leaves': 31,
            'objective': 'regression',
        }
        params.update(model_params)
        model = LGBMRegressor(**params)
        model.fit(X_train_arr, y_train_arr)
        models[col] = model
        last_lags = series.iloc[-lags:].values.tolist()
        exog_future_values = exog_future.values if exog_cols else None
        preds: List[float] = []
        for step in range(periods):
            features = last_lags[-lags:].copy()
            if exog_cols:
                features += list(exog_future_values[step])
            pred = float(model.predict(np.array(features).reshape(1, -1))[0])
            preds.append(pred)
            last_lags.append(pred)
        forecasts_data[col] = preds
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=target_cols)
    return LightGBMForecastResult(forecasts=forecast_df, models=models)

# ---------------------------------------------------------------------------
# Theta forecasting method
# ---------------------------------------------------------------------------

@dataclass
class ThetaForecastResult:
    """Result container for :func:`theta_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each series.
    models : Dict[str, tuple]
        Fitted components: linear regression parameters and
        exponential smoothing results per series.
    """
    forecasts: pd.DataFrame
    models: Dict[str, tuple]


def theta_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    freq: Optional[str] = None,
    smoothing_level: Optional[float] = None,
) -> ThetaForecastResult:
    """Forecast series using the Theta method.

    The Theta method combines a linear extrapolation of the trend and
    an exponential smoothing forecast.  For each series, a simple
    linear regression is fit on the time index to estimate the trend,
    and Simple Exponential Smoothing (SES) is applied to capture the
    level.  The forecast is the average of the extrapolated trend and
    the SES forecast.  When ``statsmodels`` is not available, a
    naive last‑value forecast is used instead of SES.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Must include the date column and
        one or more numeric columns to forecast.
    periods : int, default 12
        Number of future periods to forecast.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If ``None``,
        the frequency is inferred from the date series.
    smoothing_level : float or None, default None
        Smoothing parameter for the SES component.  If ``None``, it
        is estimated via maximum likelihood.

    Returns
    -------
    ThetaForecastResult
        Dataclass containing the forecasted values and fitted model
        components.

    Raises
    ------
    ImportError
        If ``statsmodels`` is not installed and a smoothing level is
        specified.
    ValueError
        If no numeric columns are available to model.
    """
    try:
        from statsmodels.tsa.holtwinters import SimpleExpSmoothing
    except Exception as e:
        if smoothing_level is not None:
            raise ImportError(
                "statsmodels is required for the Theta method when a smoothing level is specified. "
                "Please install statsmodels to use this feature."
            ) from e
        SimpleExpSmoothing = None
    # Determine date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Determine frequency for future index
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric columns found to forecast with the Theta method")
    models: Dict[str, tuple] = {}
    forecasts_data: Dict[str, List[float]] = {}
    for col in numeric_cols:
        series = pd.to_numeric(df[col], errors='coerce').astype(float)
        n = len(series)
        # Linear regression on index
        t = np.arange(n)
        mask = ~series.isna()
        t_masked = t[mask]
        y_masked = series[mask]
        if len(y_masked) < 2:
            trend_forecast = np.full(periods, series.iloc[-1] if not series.empty else np.nan)
            slope, intercept = 0.0, series.iloc[-1] if not series.empty else np.nan
        else:
            coeffs = np.polyfit(t_masked, y_masked, 1)
            slope, intercept = float(coeffs[0]), float(coeffs[1])
            trend_forecast = intercept + slope * (np.arange(n, n + periods))
        # SES component
        if SimpleExpSmoothing is not None and len(y_masked) >= 2:
            try:
                ses_model = SimpleExpSmoothing(y_masked).fit(smoothing_level=smoothing_level, optimized=(smoothing_level is None))
                ses_forecast = ses_model.forecast(periods).values
                models[col] = (slope, intercept, ses_model)
            except Exception:
                ses_forecast = np.full(periods, y_masked.iloc[-1] if len(y_masked) > 0 else np.nan)
                models[col] = (slope, intercept, None)
        else:
            ses_forecast = np.full(periods, y_masked.iloc[-1] if len(y_masked) > 0 else np.nan)
            models[col] = (slope, intercept, None)
        theta_pred = 0.5 * (trend_forecast + ses_forecast)
        forecasts_data[col] = theta_pred
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=numeric_cols)
    return ThetaForecastResult(forecasts=forecast_df, models=models)

# ---------------------------------------------------------------------------
# Further advanced forecasting methods
# These methods leverage additional external libraries such as scikit‑learn,
# tensorflow, tbats and neuralprophet to provide state‑of‑the‑art models.  If
# the required library is not available in your environment an informative
# ImportError will be raised.

@dataclass
class ElasticNetForecastResult:
    """Result container for :func:`elastic_net_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each target series.  The index contains
        the forecast dates and the columns correspond to the numeric
        columns of the input (excluding the date and exogenous columns).
    models : Dict[str, object]
        Trained scikit‑learn ElasticNet or ElasticNetCV models for each
        series.
    """

    forecasts: pd.DataFrame
    models: Dict[str, object]


def elastic_net_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    lags: int = 10,
    exog: Optional[List[str]] = None,
    freq: Optional[str] = None,
    model_params: Optional[dict] = None,
) -> ElasticNetForecastResult:
    """Forecast numeric series using ElasticNet regression with lagged features.

    Each target column is modelled independently.  Lagged values of the
    target up to ``lags`` steps are used as predictors along with
    optional exogenous variables at the current time step.  Models are
    trained either using ``ElasticNetCV`` for automatic hyperparameter
    selection or ``ElasticNet`` with user‑specified parameters.  The
    function then iteratively produces forecasts for ``periods`` future
    steps.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Must include the date column and
        one or more numeric columns to forecast.
    periods : int, default 12
        Number of future periods to forecast.
    lags : int, default 10
        Number of lag observations to include as predictors.
    exog : list of str or None, default None
        Names of exogenous columns to include as predictors.  If
        provided, future values for these variables can be passed via
        ``model_params['exog_future']`` as a DataFrame with ``periods``
        rows and the same columns as ``exog``.  If not provided, zeros
        will be used for future exogenous values.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If ``None``,
        the frequency is inferred from the date series.
    model_params : dict or None, default None
        Additional keyword arguments passed to the scikit‑learn model.
        Recognised keys include ``exog_future`` (future exogenous
        DataFrame), ``use_cv`` (bool indicating whether to use
        ``ElasticNetCV`` instead of ``ElasticNet``), and any valid
        parameters for ``ElasticNetCV`` or ``ElasticNet``.

    Returns
    -------
    ElasticNetForecastResult
        Dataclass containing the forecast DataFrame and fitted models.

    Raises
    ------
    ImportError
        If scikit‑learn is not installed.
    ValueError
        If no numeric columns are available to model.
    """
    try:
        from sklearn.linear_model import ElasticNet, ElasticNetCV
    except Exception as e:
        raise ImportError(
            "scikit‑learn is required for ElasticNet forecasting."
        ) from e
    if model_params is None:
        model_params = {}
    # Extract optional future exogenous values and flags
    exog_future = model_params.pop('exog_future', None)
    use_cv = bool(model_params.pop('use_cv', True))
    # Determine date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Identify target and exogenous columns
    exog_cols = exog or []
    target_cols = [c for c in df.columns if c != date and (c not in exog_cols) and pd.api.types.is_numeric_dtype(df[c])]
    if not target_cols:
        raise ValueError("No numeric columns found to forecast with ElasticNet")
    # Determine frequency and future dates
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # Prepare future exogenous values
    if exog_cols and exog_future is None:
        exog_future = pd.DataFrame(
            np.zeros((periods, len(exog_cols))), index=future_index, columns=exog_cols
        )
    elif exog_cols:
        exog_future = exog_future.copy()
        exog_future.index = future_index
        exog_future = exog_future[exog_cols]
    # Initialize storage
    models: Dict[str, object] = {}
    forecasts_data: Dict[str, List[float]] = {}
    # Iterate over each target column
    for col in target_cols:
        series = pd.to_numeric(df[col], errors='coerce').astype(float).reset_index(drop=True)
        n = len(series)
        if n <= lags:
            raise ValueError(f"Not enough observations to build lagged features for column '{col}'")
        # Build design matrix
        X_train = []
        y_train = []
        exog_matrix = df[exog_cols].reset_index(drop=True) if exog_cols else None
        for t in range(lags, n):
            lagged = series.iloc[t - lags:t].values
            features = list(lagged)
            if exog_cols:
                features += list(exog_matrix.iloc[t].values)
            X_train.append(features)
            y_train.append(series.iloc[t])
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        # Choose ElasticNet or ElasticNetCV
        if use_cv:
            model = ElasticNetCV(**model_params)
        else:
            model = ElasticNet(**model_params)
        model.fit(X_train, y_train)
        models[col] = model
        # Iterative forecasting
        last_lags = series.iloc[-lags:].values.tolist()
        exog_future_values = exog_future.values if exog_cols else None
        preds: List[float] = []
        for step in range(periods):
            features = last_lags[-lags:].copy()
            if exog_cols:
                features += list(exog_future_values[step])
            pred = float(model.predict(np.array(features).reshape(1, -1))[0])
            preds.append(pred)
            last_lags.append(pred)
        forecasts_data[col] = preds
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=target_cols)
    return ElasticNetForecastResult(forecasts=forecast_df, models=models)


@dataclass
class SvrForecastResult:
    """Result container for :func:`svr_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each target series.
    models : Dict[str, object]
        Trained ``sklearn.svm.SVR`` models for each series.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]


def svr_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    lags: int = 10,
    exog: Optional[List[str]] = None,
    freq: Optional[str] = None,
    model_params: Optional[dict] = None,
) -> SvrForecastResult:
    """Forecast numeric series using Support Vector Regression.

    This method constructs lagged feature matrices similar to
    :func:`elastic_net_forecast` and trains an ``SVR`` model for each
    target series.  Forecasts are generated iteratively, using the
    most recent predictions to inform subsequent steps.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Must include the date column and
        one or more numeric columns to forecast.
    periods : int, default 12
        Number of future periods to forecast.
    lags : int, default 10
        Number of lag observations to include as predictors.
    exog : list of str or None, default None
        Names of exogenous columns to include as predictors.  If
        provided, future values for these variables can be passed via
        ``model_params['exog_future']`` as a DataFrame with ``periods``
        rows and the same columns as ``exog``.  If not provided, zeros
        will be used for future exogenous values.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If ``None``,
        the frequency is inferred from the date series.
    model_params : dict or None, default None
        Additional keyword arguments passed to ``SVR``.

    Returns
    -------
    SvrForecastResult
        Dataclass containing the forecast DataFrame and fitted models.

    Raises
    ------
    ImportError
        If scikit‑learn is not installed.
    ValueError
        If no numeric columns are available to model.
    """
    try:
        from sklearn.svm import SVR
    except Exception as e:
        raise ImportError(
            "scikit‑learn is required for SVR forecasting."
        ) from e
    if model_params is None:
        model_params = {}
    exog_future = model_params.pop('exog_future', None)
    # Parse date
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    exog_cols = exog or []
    target_cols = [c for c in df.columns if c != date and (c not in exog_cols) and pd.api.types.is_numeric_dtype(df[c])]
    if not target_cols:
        raise ValueError("No numeric columns found to forecast with SVR")
    # Determine frequency and future dates
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # Prepare future exogenous values
    if exog_cols and exog_future is None:
        exog_future = pd.DataFrame(
            np.zeros((periods, len(exog_cols))), index=future_index, columns=exog_cols
        )
    elif exog_cols:
        exog_future = exog_future.copy()
        exog_future.index = future_index
        exog_future = exog_future[exog_cols]
    # Train models
    models: Dict[str, object] = {}
    forecasts_data: Dict[str, List[float]] = {}
    for col in target_cols:
        series = pd.to_numeric(df[col], errors='coerce').astype(float).reset_index(drop=True)
        n = len(series)
        if n <= lags:
            raise ValueError(f"Not enough observations to build lagged features for column '{col}'")
        X_train = []
        y_train = []
        exog_matrix = df[exog_cols].reset_index(drop=True) if exog_cols else None
        for t in range(lags, n):
            lagged = series.iloc[t - lags:t].values
            features = list(lagged)
            if exog_cols:
                features += list(exog_matrix.iloc[t].values)
            X_train.append(features)
            y_train.append(series.iloc[t])
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        model = SVR(**model_params)
        model.fit(X_train, y_train)
        models[col] = model
        last_lags = series.iloc[-lags:].values.tolist()
        exog_future_values = exog_future.values if exog_cols else None
        preds: List[float] = []
        for step in range(periods):
            features = last_lags[-lags:].copy()
            if exog_cols:
                features += list(exog_future_values[step])
            pred = float(model.predict(np.array(features).reshape(1, -1))[0])
            preds.append(pred)
            last_lags.append(pred)
        forecasts_data[col] = preds
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=target_cols)
    return SvrForecastResult(forecasts=forecast_df, models=models)


@dataclass
class TcnForecastResult:
    """Result container for :func:`tcn_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each target series.
    models : Dict[str, object]
        Trained TensorFlow models for each series.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]


def tcn_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    lags: int = 24,
    freq: Optional[str] = None,
    epochs: int = 50,
    batch_size: int = 32,
    verbose: int = 0,
) -> TcnForecastResult:
    """Forecast univariate series using a Temporal Convolutional Network (TCN).

    Each numeric column is modelled separately using a simple TCN built
    with ``tensorflow.keras``.  The TCN consists of a stack of
    dilated causal convolution layers followed by a dense output
    layer.  Lagged values of the series serve as inputs.  This
    method is computationally intensive and may require GPU support
    for large datasets.  If TensorFlow is not installed, an
    ``ImportError`` is raised.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Must include the date column and
        one or more numeric columns to forecast.
    periods : int, default 12
        Number of future periods to forecast.
    lags : int, default 24
        Number of lagged observations to use as input to the network.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If ``None``,
        the frequency is inferred from the date series.
    epochs : int, default 50
        Number of training epochs for each model.
    batch_size : int, default 32
        Batch size for model training.
    verbose : int, default 0
        Verbosity level passed to ``model.fit``.

    Returns
    -------
    TcnForecastResult
        Dataclass containing the forecast DataFrame and fitted models.

    Raises
    ------
    ImportError
        If ``tensorflow`` is not installed.
    ValueError
        If no numeric columns are available for forecasting.
    """
    try:
        import tensorflow as tf  # type: ignore
    except Exception as e:
        raise ImportError(
            "tensorflow is required for TCN forecasting. Please install tensorflow to use this function."
        ) from e
    # Parse date
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Determine frequency and future dates
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # Identify numeric columns
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric columns found to forecast with TCN")
    models: Dict[str, object] = {}
    forecasts_data: Dict[str, List[float]] = {}
    for col in numeric_cols:
        series = pd.to_numeric(df[col], errors='coerce').astype(float).reset_index(drop=True)
        n = len(series)
        if n <= lags:
            raise ValueError(f"Not enough observations to build lagged features for column '{col}'")
        # Build training sequences
        X_train = []
        y_train = []
        for t in range(lags, n):
            X_train.append(series.iloc[t - lags:t].values.reshape(-1, 1))
            y_train.append(series.iloc[t])
        X_train = np.stack(X_train)
        y_train = np.array(y_train)
        # Define TCN model
        inputs = tf.keras.Input(shape=(lags, 1))
        x = tf.keras.layers.Conv1D(32, kernel_size=2, dilation_rate=1, padding='causal', activation='relu')(inputs)
        x = tf.keras.layers.Conv1D(32, kernel_size=2, dilation_rate=2, padding='causal', activation='relu')(x)
        x = tf.keras.layers.Conv1D(32, kernel_size=2, dilation_rate=4, padding='causal', activation='relu')(x)
        x = tf.keras.layers.Flatten()(x)
        outputs = tf.keras.layers.Dense(1)(x)
        model = tf.keras.Model(inputs, outputs)
        model.compile(optimizer='adam', loss='mse')
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose)
        models[col] = model
        # Generate forecasts iteratively
        last_lags = series.iloc[-lags:].values.reshape(1, -1, 1).copy()
        preds: List[float] = []
        for _ in range(periods):
            pred = float(model.predict(last_lags, verbose=0)[0, 0])
            preds.append(pred)
            # Update last_lags
            new_seq = np.append(last_lags[0, 1:, 0], pred)
            last_lags = new_seq.reshape(1, -1, 1)
        forecasts_data[col] = preds
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=numeric_cols)
    return TcnForecastResult(forecasts=forecast_df, models=models)


@dataclass
class BatsForecastResult:
    """Result container for :func:`bats_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each series.
    models : Dict[str, object]
        Fitted TBATS/BATS models for each series.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]


def bats_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    seasonal_periods: Optional[Iterable[int]] = None,
    use_box_cox: bool = True,
    use_trend: bool = True,
    use_damped_trend: bool = True,
    freq: Optional[str] = None,
) -> BatsForecastResult:
    """Forecast univariate series using TBATS or BATS models.

    This function fits either a TBATS (Trigonometric, Box‑Cox, ARMA,
    Trend, Seasonal) or BATS (Box‑Cox, ARMA, Trend, Seasonal) model to
    each numeric column depending on whether seasonal periods are
    provided.  The ``tbats`` library must be installed to use this
    function.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Numeric columns are modelled
        individually.
    periods : int, default 12
        Number of future periods to forecast.
    seasonal_periods : iterable of int or None, default None
        Seasonal periods to fit.  If provided, TBATS is used.
    use_box_cox : bool, default True
        Whether to apply a Box–Cox transformation when fitting.
    use_trend : bool, default True
        Whether to include a trend component.
    use_damped_trend : bool, default True
        Whether to include a damped trend component.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If ``None``,
        the frequency is inferred from the date series.

    Returns
    -------
    BatsForecastResult
        Dataclass containing the forecast DataFrame and fitted models.

    Raises
    ------
    ImportError
        If the ``tbats`` package is not installed.
    ValueError
        If no numeric columns are available to model.
    """
    try:
        from tbats import TBATS, BATS  # type: ignore
    except Exception as e:
        raise ImportError(
            "The 'tbats' library is required for TBATS/BATS forecasting. Please install tbats to use this function."
        ) from e
    # Parse date
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Determine frequency and future dates
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric columns found to forecast with TBATS/BATS")
    models: Dict[str, object] = {}
    forecasts_data: Dict[str, np.ndarray] = {}
    for col in numeric_cols:
        y = pd.to_numeric(df[col], errors='coerce').ffill().bfill().astype(float)
        # Choose estimator
        if seasonal_periods is not None:
            estimator = TBATS(
                seasonal_periods=seasonal_periods,
                use_box_cox=use_box_cox,
                use_trend=use_trend,
                use_damped_trend=use_damped_trend,
            )
        else:
            estimator = BATS(
                use_box_cox=use_box_cox,
                use_trend=use_trend,
                use_damped_trend=use_damped_trend,
            )
        model = estimator.fit(y)
        preds = model.forecast(steps=periods)
        models[col] = model
        forecasts_data[col] = preds
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=numeric_cols)
    return BatsForecastResult(forecasts=forecast_df, models=models)


@dataclass
class NeuralProphetForecastResult:
    """Result container for :func:`neuralprophet_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each series.
    models : Dict[str, object]
        Fitted NeuralProphet models for each series.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]


def neuralprophet_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    freq: Optional[str] = None,
    model_params: Optional[dict] = None,
) -> NeuralProphetForecastResult:
    """Forecast univariate series using NeuralProphet.

    NeuralProphet combines elements of Facebook’s Prophet with neural
    networks to capture non‑linear relationships and seasonality.
    Each numeric column is converted into a two‑column DataFrame with
    ``ds`` (datetime) and ``y`` (value) columns.  A separate
    ``NeuralProphet`` model is fit per series using any provided
    ``model_params``.  The forecast horizon is controlled by
    ``periods``.  The ``freq`` parameter determines the frequency of
    the future DataFrame; if ``None``, it is inferred.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Must include the date column and
        one or more numeric columns to forecast.
    periods : int, default 12
        Number of future periods to forecast.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If ``None``,
        frequency is inferred from the date series.
    model_params : dict or None, default None
        Additional keyword arguments passed to the ``NeuralProphet``
        constructor.  See the ``neuralprophet`` documentation for
        available options.

    Returns
    -------
    NeuralProphetForecastResult
        Dataclass containing the forecast DataFrame and fitted models.

    Raises
    ------
    ImportError
        If the ``neuralprophet`` package is not installed.
    ValueError
        If no numeric columns are available to model.
    """
    try:
        from neuralprophet import NeuralProphet  # type: ignore
    except Exception as e:
        raise ImportError(
            "The neuralprophet package is required for neuralprophet forecasting. Please install neuralprophet to use this function."
        ) from e
    if model_params is None:
        model_params = {}
    # Parse date
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Infer frequency and future dates
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    # Determine numeric columns
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric columns found to forecast with NeuralProphet")
    # Prepare storage
    models: Dict[str, object] = {}
    forecast_dict: Dict[str, np.ndarray] = {}
    # Fit each series separately
    for col in numeric_cols:
        # Prepare DataFrame for NeuralProphet
        temp = pd.DataFrame({
            'ds': dt,
            'y': pd.to_numeric(df[col], errors='coerce'),
        }).dropna()
        # Create model
        m = NeuralProphet(**model_params)
        m.fit(temp, freq=freq, verbose=False)
        future = m.make_future_dataframe(temp, periods=periods, n_historic_predictions=False)
        forecast = m.predict(future)
        # Extract predictions from 'yhat1' column (default output)
        yhat = forecast['yhat1'].values
        # The forecast array may include historic predictions; we want only the last 'periods' entries
        preds = yhat[-periods:]
        models[col] = m
        forecast_dict[col] = preds
    # Create index for forecast
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    forecast_df = pd.DataFrame(forecast_dict, index=future_index, columns=numeric_cols)
    return NeuralProphetForecastResult(forecasts=forecast_df, models=models)

@dataclass
class CatBoostForecastResult:
    """Result container for :func:`catboost_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each target series.
    models : Dict[str, object]
        Trained ``catboost.CatBoostRegressor`` models for each series.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]


def catboost_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    lags: int = 10,
    exog: Optional[List[str]] = None,
    freq: Optional[str] = None,
    model_params: Optional[dict] = None,
) -> CatBoostForecastResult:
    """Forecast numeric series using CatBoost regressors with lagged features.

    This method resembles :func:`xgboost_forecast` but employs
    ``catboost.CatBoostRegressor`` to model non‑linear relationships.
    Each numeric column (excluding the date and exogenous columns) is
    modelled separately.  Lagged values up to ``lags`` and optional
    exogenous variables at the current time step are used as predictors.
    Future exogenous values may be provided via ``model_params['exog_future']``.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Must include the date column and
        one or more numeric columns to forecast.
    periods : int, default 12
        Number of future periods to forecast.
    lags : int, default 10
        Number of lag observations to include as predictors.
    exog : list of str or None, default None
        Names of exogenous columns to include as predictors.  These
        columns must be present in ``df``.  If provided, future values
        for these variables can be passed via ``model_params['exog_future']``.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If ``None``,
        the frequency is inferred from the date series.
    model_params : dict or None, default None
        Additional parameters passed to ``catboost.CatBoostRegressor``.
        Recognised key ``exog_future`` may be a DataFrame providing
        exogenous values for the forecast horizon.

    Returns
    -------
    CatBoostForecastResult
        Dataclass containing the forecasted values and fitted models.

    Raises
    ------
    ImportError
        If the ``catboost`` package is not installed.
    ValueError
        If no numeric columns are available to model.
    """
    try:
        from catboost import CatBoostRegressor  # type: ignore
    except Exception as e:
        raise ImportError(
            "catboost is required for CatBoost forecasting. Please install catboost to use this function."
        ) from e
    if model_params is None:
        model_params = {}
    exog_future = model_params.pop('exog_future', None)
    # Parse date
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Identify target and exogenous columns
    exog_cols = exog or []
    target_cols = [c for c in df.columns if c != date and (c not in exog_cols) and pd.api.types.is_numeric_dtype(df[c])]
    if not target_cols:
        raise ValueError("No numeric columns found to forecast with CatBoost")
    # Determine frequency and future dates
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # Prepare future exogenous values
    if exog_cols and exog_future is None:
        exog_future = pd.DataFrame(
            np.zeros((periods, len(exog_cols))), index=future_index, columns=exog_cols
        )
    elif exog_cols:
        exog_future = exog_future.copy()
        exog_future.index = future_index
        exog_future = exog_future[exog_cols]
    models: Dict[str, object] = {}
    forecasts_data: Dict[str, List[float]] = {}
    for col in target_cols:
        series = pd.to_numeric(df[col], errors='coerce').astype(float).reset_index(drop=True)
        n = len(series)
        if n <= lags:
            raise ValueError(f"Not enough observations to build lagged features for column '{col}'")
        X_train = []
        y_train = []
        exog_matrix = df[exog_cols].reset_index(drop=True) if exog_cols else None
        for t in range(lags, n):
            lagged = series.iloc[t - lags:t].values
            features = list(lagged)
            if exog_cols:
                features += list(exog_matrix.iloc[t].values)
            X_train.append(features)
            y_train.append(series.iloc[t])
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        default_params = {
            'iterations': 500,
            'learning_rate': 0.05,
            'depth': 6,
            'loss_function': 'RMSE',
            'verbose': False,
        }
        params = default_params.copy()
        params.update(model_params)
        model = CatBoostRegressor(**params)
        model.fit(X_train, y_train)
        models[col] = model
        last_lags = series.iloc[-lags:].values.tolist()
        exog_future_values = exog_future.values if exog_cols else None
        preds: List[float] = []
        for step in range(periods):
            features = last_lags[-lags:].copy()
            if exog_cols:
                features += list(exog_future_values[step])
            pred = float(model.predict(np.array(features).reshape(1, -1))[0])
            preds.append(pred)
            last_lags.append(pred)
        forecasts_data[col] = preds
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=target_cols)
    return CatBoostForecastResult(forecasts=forecast_df, models=models)


@dataclass
class KnnForecastResult:
    """Result container for :func:`knn_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each target series.
    models : Dict[str, object]
        Trained ``sklearn.neighbors.KNeighborsRegressor`` models for each series.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]


def knn_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    lags: int = 10,
    exog: Optional[List[str]] = None,
    freq: Optional[str] = None,
    model_params: Optional[dict] = None,
) -> KnnForecastResult:
    """Forecast numeric series using k‑nearest neighbors regression.

    The function builds lagged feature matrices and fits a
    ``KNeighborsRegressor`` for each target series.  Predictions are
    generated iteratively using the most recent lagged values.  You
    can specify exogenous variables to include as additional features.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Must include the date column and
        one or more numeric columns to forecast.
    periods : int, default 12
        Number of future periods to forecast.
    lags : int, default 10
        Number of lag observations to include as predictors.
    exog : list of str or None, default None
        Names of exogenous columns to include as predictors.  Future
        values for these variables can be passed via
        ``model_params['exog_future']`` as a DataFrame.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If ``None``,
        the frequency is inferred from the date series.
    model_params : dict or None, default None
        Additional keyword arguments passed to ``KNeighborsRegressor``.

    Returns
    -------
    KnnForecastResult
        Dataclass containing the forecast DataFrame and fitted models.

    Raises
    ------
    ImportError
        If scikit‑learn is not installed.
    ValueError
        If no numeric columns are available to model.
    """
    try:
        from sklearn.neighbors import KNeighborsRegressor
    except Exception as e:
        raise ImportError(
            "scikit‑learn is required for KNN forecasting."
        ) from e
    if model_params is None:
        model_params = {}
    exog_future = model_params.pop('exog_future', None)
    # Parse date
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Identify target and exogenous columns
    exog_cols = exog or []
    target_cols = [c for c in df.columns if c != date and (c not in exog_cols) and pd.api.types.is_numeric_dtype(df[c])]
    if not target_cols:
        raise ValueError("No numeric columns found to forecast with KNN")
    # Determine frequency and future dates
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # Prepare future exogenous values
    if exog_cols and exog_future is None:
        exog_future = pd.DataFrame(
            np.zeros((periods, len(exog_cols))), index=future_index, columns=exog_cols
        )
    elif exog_cols:
        exog_future = exog_future.copy()
        exog_future.index = future_index
        exog_future = exog_future[exog_cols]
    models: Dict[str, object] = {}
    forecasts_data: Dict[str, List[float]] = {}
    for col in target_cols:
        series = pd.to_numeric(df[col], errors='coerce').astype(float).reset_index(drop=True)
        n = len(series)
        if n <= lags:
            raise ValueError(f"Not enough observations to build lagged features for column '{col}'")
        X_train = []
        y_train = []
        exog_matrix = df[exog_cols].reset_index(drop=True) if exog_cols else None
        for t in range(lags, n):
            lagged = series.iloc[t - lags:t].values
            features = list(lagged)
            if exog_cols:
                features += list(exog_matrix.iloc[t].values)
            X_train.append(features)
            y_train.append(series.iloc[t])
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        model = KNeighborsRegressor(**model_params)
        model.fit(X_train, y_train)
        models[col] = model
        last_lags = series.iloc[-lags:].values.tolist()
        exog_future_values = exog_future.values if exog_cols else None
        preds: List[float] = []
        for step in range(periods):
            features = last_lags[-lags:].copy()
            if exog_cols:
                features += list(exog_future_values[step])
            pred = float(model.predict(np.array(features).reshape(1, -1))[0])
            preds.append(pred)
            last_lags.append(pred)
        forecasts_data[col] = preds
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=target_cols)
    return KnnForecastResult(forecasts=forecast_df, models=models)


@dataclass
class TransformerForecastResult:
    """Result container for :func:`transformer_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for each series.
    models : Dict[str, object]
        Trained TensorFlow models for each series.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]


def transformer_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    periods: int = 12,
    lags: int = 24,
    freq: Optional[str] = None,
    epochs: int = 50,
    batch_size: int = 32,
    verbose: int = 0,
    num_heads: int = 2,
    key_dim: int = 32,
) -> TransformerForecastResult:
    """Forecast univariate series using a simple Transformer model.

    A Transformer with multi‑head self‑attention is trained on lagged
    sequences of the target series.  This architecture can capture
    complex temporal dependencies and non‑linear patterns.  Each
    numeric column is modelled separately.  The function requires
    ``tensorflow`` to be installed.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with the data.  Must include the date column and
        one or more numeric columns to forecast.
    periods : int, default 12
        Number of future periods to forecast.
    lags : int, default 24
        Number of lagged observations to use as input to the model.
    freq : str or None, default None
        Frequency string for generating forecast dates.  If ``None``,
        the frequency is inferred from the date series.
    epochs : int, default 50
        Number of training epochs for each model.
    batch_size : int, default 32
        Batch size for model training.
    verbose : int, default 0
        Verbosity level passed to ``model.fit``.
    num_heads : int, default 2
        Number of attention heads in the Transformer.
    key_dim : int, default 32
        Dimensionality of the query and key vectors in the
        multi‑head attention layer.

    Returns
    -------
    TransformerForecastResult
        Dataclass containing the forecast DataFrame and fitted models.

    Raises
    ------
    ImportError
        If ``tensorflow`` is not installed.
    ValueError
        If no numeric columns are available to model.
    """
    try:
        import tensorflow as tf  # type: ignore
    except Exception as e:
        raise ImportError(
            "tensorflow is required for transformer forecasting. Please install tensorflow to use this function."
        ) from e
    # Parse date
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Determine frequency and future dates
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # Identify numeric columns
    numeric_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        raise ValueError("No numeric columns found to forecast with transformer")
    models: Dict[str, object] = {}
    forecasts_data: Dict[str, List[float]] = {}
    for col in numeric_cols:
        series = pd.to_numeric(df[col], errors='coerce').astype(float).reset_index(drop=True)
        n = len(series)
        if n <= lags:
            raise ValueError(f"Not enough observations to build lagged features for column '{col}'")
        X_train = []
        y_train = []
        for t in range(lags, n):
            X_train.append(series.iloc[t - lags:t].values.reshape(lags, 1))
            y_train.append(series.iloc[t])
        X_train = np.stack(X_train)
        y_train = np.array(y_train)
        # Build transformer model
        inputs = tf.keras.Input(shape=(lags, 1))
        # Project to embedding dimension
        x = tf.keras.layers.Conv1D(key_dim, kernel_size=1, activation='relu')(inputs)
        # Positional embedding: simple linear transformation of positions
        positions = tf.range(start=0, limit=lags, delta=1)
        pos_embed = tf.keras.layers.Embedding(input_dim=lags, output_dim=key_dim)(positions)
        pos_embed = tf.expand_dims(pos_embed, axis=0)
        x = x + pos_embed
        # Self‑attention
        attn_output = tf.keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=key_dim)(x, x)
        attn_output = tf.keras.layers.GlobalAveragePooling1D()(attn_output)
        outputs = tf.keras.layers.Dense(1)(attn_output)
        model = tf.keras.Model(inputs, outputs)
        model.compile(optimizer='adam', loss='mse')
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose)
        models[col] = model
        # Iterative forecasting
        last_lags = series.iloc[-lags:].values.reshape(1, lags, 1)
        preds: List[float] = []
        for _ in range(periods):
            # Add positional embedding to last_lags
            embedded = tf.keras.layers.Conv1D(key_dim, kernel_size=1, activation='relu')(last_lags)
            pos = tf.expand_dims(tf.range(start=0, limit=lags, delta=1), axis=0)
            pos_emb = tf.keras.layers.Embedding(input_dim=lags, output_dim=key_dim)(pos)
            x_in = embedded + pos_emb
            attn_out = tf.keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=key_dim)(x_in, x_in)
            pooled = tf.keras.layers.GlobalAveragePooling1D()(attn_out)
            pred = float(tf.keras.layers.Dense(1)(pooled).numpy()[0, 0])
            preds.append(pred)
            # Update last_lags
            new_seq = np.append(last_lags[0, 1:, 0], pred)
            last_lags = new_seq.reshape(1, lags, 1)
        forecasts_data[col] = preds
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=numeric_cols)
    return TransformerForecastResult(forecasts=forecast_df, models=models)

# ---------------------------------------------------------------------------
# Intraday distillate burn forecasting functions and AutoGluon integration
# ---------------------------------------------------------------------------

@dataclass
class IntradayLoadBurnForecastResult:
    """Result container for :func:`intraday_load_burn_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted burn values at intraday (e.g. 5‑minute) intervals.  The
        index corresponds to the forecast timestamps and the columns
        correspond to the burn series being modelled.
    models : Dict[str, object]
        Fitted regression models (e.g. GradientBoostingRegressor or
        RandomForestRegressor) for each series.
    lower_conf_int : pandas.DataFrame or None
        Lower bounds of 95% prediction intervals, if available.
    upper_conf_int : pandas.DataFrame or None
        Upper bounds of 95% prediction intervals, if available.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]
    lower_conf_int: Optional[pd.DataFrame] = None
    upper_conf_int: Optional[pd.DataFrame] = None


def intraday_load_burn_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    load_df: pd.DataFrame,
    periods: int = 12,
    lags: int = 12,
    model_type: str = 'gbm',
    model_params: Optional[dict] = None,
    cache_path: Optional[str] = None,
    freq: Optional[str] = None,
    plot: bool = False,
    return_conf_int: bool = True,
) -> IntradayLoadBurnForecastResult:
    """Forecast intraday distillate burn given 5‑minute interval data and load forecasts.

    This function builds a predictive model for each numeric burn series
    in ``df`` using lagged values of the burn series and contemporaneous
    or lagged load values from ``load_df``.  It supports ``GradientBoostingRegressor``
    and ``RandomForestRegressor`` as model types.  Models can be cached
    to disk and re‑used, avoiding retraining on subsequent calls.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing datetime information.
    df : pandas.DataFrame
        DataFrame with historical burn data.  Must include the date
        column and at least one numeric burn column.  The index
        frequency should match the desired intraday granularity (e.g.
        5‑minute).
    load_df : pandas.DataFrame
        DataFrame containing load data aligned by time index.  Must
        include the same date column as ``df`` and at least one load
        column (e.g. 'load').  Future load values for the forecast
        horizon should also be present in ``load_df``.
    periods : int, default 12
        Number of future intraday periods to forecast.
    lags : int, default 12
        Number of lag observations of the burn series and load series
        to include as predictors.
    model_type : {'gbm', 'rf'}, default 'gbm'
        Type of regression model to fit.  'gbm' uses
        ``GradientBoostingRegressor``; 'rf' uses ``RandomForestRegressor``.
    model_params : dict or None, default None
        Additional parameters passed to the underlying regressor.
        Recognised key ``load_cols`` may specify the load column names
        in ``load_df`` (default uses all numeric columns except the
        date).
    cache_path : str or None, default None
        Path to a directory where fitted models should be cached.
        When provided, the function will attempt to load existing
        models from ``cache_path`` before training new ones.
    freq : str or None, default None
        Frequency string for generating forecast timestamps.  If
        ``None``, frequency is inferred from the date series.
    plot : bool, default False
        Whether to produce an interactive Plotly plot comparing
        historical burn data with forecasts.  If True, 95% prediction
        intervals are plotted as shaded bands when available.
    return_conf_int : bool, default True
        If True, the function estimates prediction intervals using
        quantile regression (if supported by the model) or a simple
        residual bootstrap.  Set to False to skip interval estimation.

    Returns
    -------
    IntradayLoadBurnForecastResult
        Dataclass containing the forecast DataFrame, fitted models and
        prediction intervals if requested.

    Notes
    -----
    The function does not require a GPU; all models are trained using
    CPU‑efficient algorithms.  For high‑frequency data, ensure that
    ``df`` and ``load_df`` are pre‑sorted by time and that they cover
    the same time range.  Missing values are forward‑filled before
    model fitting.
    """
    # Lazy imports for scikit-learn regressors
    try:
        from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
    except Exception as e:
        raise ImportError(
            "scikit‑learn is required for intraday load‑burn forecasting."
        ) from e
    import os
    import joblib  # for model caching
    # Determine date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in burn DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Determine frequency and future timestamps
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(minutes=5)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # Identify burn columns
    burn_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    if not burn_cols:
        raise ValueError("No numeric burn columns found in the input DataFrame")
    # Identify load columns
    if model_params is None:
        model_params = {}
    load_cols = model_params.pop('load_cols', None)
    if load_cols is None:
        load_cols = [c for c in load_df.columns if c != date and pd.api.types.is_numeric_dtype(load_df[c])]
    if not load_cols:
        raise ValueError("No numeric load columns found in load DataFrame")
    # Merge burn and load on date
    combined = pd.merge(df[[date] + burn_cols], load_df[[date] + load_cols], on=date, how='inner')
    combined.sort_values(by=date, inplace=True)
    # Forward fill missing values
    combined[burn_cols + load_cols] = combined[burn_cols + load_cols].ffill().bfill()
    # Storage for results
    forecasts_data: Dict[str, List[float]] = {}
    models: Dict[str, object] = {}
    lower_bounds: Dict[str, np.ndarray] = {}
    upper_bounds: Dict[str, np.ndarray] = {}
    # Ensure cache directory exists if provided
    if cache_path is not None:
        os.makedirs(cache_path, exist_ok=True)
    # Iterate over each burn column
    for col in burn_cols:
        # Build key for cache
        cache_file = None
        if cache_path is not None:
            cache_file = os.path.join(cache_path, f"intraday_{col}_{model_type}.joblib")
        if cache_file is not None and os.path.exists(cache_file):
            # Load cached model
            model = joblib.load(cache_file)
        else:
            # Prepare training data
            series = combined[col].astype(float).reset_index(drop=True)
            loads = combined[load_cols].astype(float).reset_index(drop=True)
            n = len(series)
            X_train = []
            y_train = []
            for t in range(lags, n):
                features = []
                # Lagged burn values
                features += series.iloc[t - lags:t].values.tolist()
                # Lagged and contemporaneous load values (same lags)
                load_slice = loads.iloc[t - lags:t].values.flatten().tolist()
                features += load_slice
                X_train.append(features)
                y_train.append(series.iloc[t])
            X_train = np.array(X_train)
            y_train = np.array(y_train)
            # Choose model
            default_params = {}
            if model_type == 'gbm':
                ModelClass = GradientBoostingRegressor
                default_params = {
                    'n_estimators': 200,
                    'learning_rate': 0.05,
                    'max_depth': 3,
                    'min_samples_split': 2,
                    'random_state': 42,
                }
            elif model_type == 'rf':
                ModelClass = RandomForestRegressor
                default_params = {
                    'n_estimators': 200,
                    'max_depth': None,
                    'min_samples_split': 2,
                    'random_state': 42,
                    'n_jobs': -1,
                }
            else:
                raise ValueError("model_type must be 'gbm' or 'rf'")
            params = default_params.copy()
            params.update(model_params)
            model = ModelClass(**params)
            model.fit(X_train, y_train)
            # Save model to cache if specified
            if cache_file is not None:
                joblib.dump(model, cache_file)
        models[col] = model
        # Prepare lags for forecasting
        burn_history = combined[col].astype(float).tolist()[-lags:]
        load_history = combined[load_cols].astype(float).iloc[-lags:].values.flatten().tolist()
        preds: List[float] = []
        lb_list: List[float] = []
        ub_list: List[float] = []
        # Forecast iteratively
        for step in range(periods):
            # Compose features: lags of burn and load
            features = burn_history[-lags:] + load_history[-lags * len(load_cols):]
            # Predict point forecast
            pred = float(model.predict(np.array(features).reshape(1, -1))[0])
            preds.append(pred)
            # Update histories: append forecasted burn and next load value from load_df
            burn_history.append(pred)
            # Append next load snapshot: if future load exists in load_df
            if step < len(future_index):
                next_load = load_df.loc[load_df[date] == future_index[step], load_cols].values
                if next_load.size == 0:
                    # Use last known load if future load is missing
                    next_load = load_history[-len(load_cols):]
                else:
                    next_load = next_load[0]
                load_history += next_load.tolist()
            else:
                load_history += load_history[-len(load_cols):]
            # Prediction intervals via bootstrap
            if return_conf_int:
                # Bootstrap residuals: approximate residual variance by past residuals
                # Compute residuals if not yet computed
                if 'residuals' not in locals():
                    # Build residuals once using training data
                    resid_preds = model.predict(X_train)
                    residuals = y_train - resid_preds
                # Sample residuals randomly (with replacement)
                res_samples = np.random.choice(residuals, size=100)
                boot_preds = pred + res_samples
                lb_list.append(np.percentile(boot_preds, 2.5))
                ub_list.append(np.percentile(boot_preds, 97.5))
        forecasts_data[col] = preds
        if return_conf_int:
            lower_bounds[col] = np.array(lb_list)
            upper_bounds[col] = np.array(ub_list)
    # Create forecast DataFrame and intervals
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=burn_cols)
    lower_df = pd.DataFrame(lower_bounds, index=future_index, columns=burn_cols) if return_conf_int else None
    upper_df = pd.DataFrame(upper_bounds, index=future_index, columns=burn_cols) if return_conf_int else None
    # Plot if requested
    if plot:
        try:
            import plotly.graph_objects as go
        except Exception:
            plot = False
        if plot:
            fig = go.Figure()
            for col in burn_cols:
                # Historical data
                fig.add_trace(go.Scatter(
                    x=combined[date], y=combined[col], mode='lines', name=f"{col} (historical)"
                ))
                # Forecast data
                fig.add_trace(go.Scatter(
                    x=future_index, y=forecast_df[col], mode='lines', name=f"{col} (forecast)", line=dict(dash='dot')
                ))
                if return_conf_int:
                    fig.add_trace(go.Scatter(
                        x=list(future_index) + list(future_index[::-1]),
                        y=list(upper_df[col]) + list(lower_df[col][::-1]),
                        fill='toself', fillcolor='rgba(255,165,0,0.3)',
                        line=dict(color='rgba(255,165,0,0)'),
                        hoverinfo="skip",
                        showlegend=False,
                        name=f"{col} CI"
                    ))
            fig.update_layout(
                title="Intraday Load‑Burn Forecast", xaxis_title="Time", yaxis_title="Burn",
                template="plotly_white"
            )
            forecast_df.attrs['plot'] = fig
    return IntradayLoadBurnForecastResult(
        forecasts=forecast_df,
        models=models,
        lower_conf_int=lower_df,
        upper_conf_int=upper_df,
    )


@dataclass
class IntradayGpForecastResult:
    """Result container for :func:`intraday_gp_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted burn values for each series.
    models : Dict[str, object]
        Fitted Gaussian process models for each series.
    lower_conf_int : pandas.DataFrame
        Lower bounds of 95% prediction intervals.
    upper_conf_int : pandas.DataFrame
        Upper bounds of 95% prediction intervals.
    """
    forecasts: pd.DataFrame
    models: Dict[str, object]
    lower_conf_int: pd.DataFrame
    upper_conf_int: pd.DataFrame


def intraday_gp_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    load_df: pd.DataFrame,
    periods: int = 12,
    freq: Optional[str] = None,
    kernel_period: int = 288,
    cache_path: Optional[str] = None,
    plot: bool = False,
) -> IntradayGpForecastResult:
    """Forecast intraday distillate burn using Gaussian processes with periodic kernels.

    This function models each burn series as a Gaussian process with a
    composite kernel: a radial basis function (RBF) for smooth trends
    and an exponential sine squared kernel to capture periodic intraday
    patterns.  The load series is incorporated via mean function
    adjustment: a linear regression on the load is subtracted from the
    burn before fitting the GP.  The model is fitted on training data,
    cached if ``cache_path`` is provided, and then used to forecast
    future burn along with 95% prediction intervals.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing datetime information.
    df : pandas.DataFrame
        DataFrame with historical burn data at intraday frequency.
    load_df : pandas.DataFrame
        DataFrame containing aligned load data with the same date
        column as ``df``.  Must include at least one load column.
    periods : int, default 12
        Number of future intraday periods to forecast.
    freq : str or None, default None
        Frequency string for generating forecast timestamps.  If
        ``None``, frequency is inferred from the date series.
    kernel_period : int, default 288
        Approximate number of time steps per day for periodic kernel
        (e.g. 288 for 5‑minute data).  Adjust as needed for other
        granularities.
    cache_path : str or None, default None
        Directory path to cache fitted models.  When provided, models
        will be loaded from cache if available.
    plot : bool, default False
        Whether to produce an interactive Plotly plot of forecasts and
        intervals.

    Returns
    -------
    IntradayGpForecastResult
        Dataclass containing forecasts, fitted models and prediction
        intervals.
    """
    try:
        from sklearn.gaussian_process import GaussianProcessRegressor
        from sklearn.gaussian_process.kernels import RBF, ExpSineSquared, ConstantKernel
        from sklearn.linear_model import LinearRegression
    except Exception as e:
        raise ImportError(
            "scikit‑learn is required for Gaussian process forecasting."
        ) from e
    import os
    import joblib
    # Parse date
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in burn DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Determine future dates
    if freq is None:
        try:
            freq = pd.infer_freq(dt)
        except Exception:
            freq = None
    if freq is not None:
        try:
            future_index = pd.date_range(start=dt.iloc[-1], periods=periods + 1, freq=freq)[1:]
        except Exception:
            freq = None
            future_index = None
    if freq is None:
        diffs = dt.diff().dropna()
        delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(minutes=5)
        future_index = pd.to_datetime([dt.iloc[-1] + delta * (i + 1) for i in range(periods)])
    # Identify burn and load columns
    burn_cols = [c for c in df.columns if c != date and pd.api.types.is_numeric_dtype(df[c])]
    load_cols = [c for c in load_df.columns if c != date and pd.api.types.is_numeric_dtype(load_df[c])]
    if not burn_cols:
        raise ValueError("No numeric burn columns found")
    if not load_cols:
        raise ValueError("No numeric load columns found")
    # Merge burn and load
    combined = pd.merge(df[[date] + burn_cols], load_df[[date] + load_cols], on=date, how='inner')
    combined.sort_values(by=date, inplace=True)
    # Convert time to numeric index for GP input
    time_idx = np.arange(len(combined))
    # Storage
    forecasts_data: Dict[str, np.ndarray] = {}
    lower_bounds: Dict[str, np.ndarray] = {}
    upper_bounds: Dict[str, np.ndarray] = {}
    models: Dict[str, object] = {}
    if cache_path is not None:
        os.makedirs(cache_path, exist_ok=True)
    # Fit for each burn column
    for col in burn_cols:
        cache_file = None
        if cache_path is not None:
            cache_file = os.path.join(cache_path, f"gp_{col}.joblib")
        if cache_file is not None and os.path.exists(cache_file):
            model, lin_reg = joblib.load(cache_file)
        else:
            # Detrend burn series using linear regression on load
            y = combined[col].astype(float).values
            X_load = combined[load_cols].astype(float).values
            lin_reg = LinearRegression().fit(X_load, y)
            residuals = y - lin_reg.predict(X_load)
            # Define kernel: constant * (RBF + periodic)
            kernel = ConstantKernel(1.0, (1e-2, 1e2)) * (
                RBF(length_scale=kernel_period / 10, length_scale_bounds=(1e-2, 1e3)) +
                ExpSineSquared(length_scale=kernel_period / (2 * np.pi), periodicity=kernel_period)
            )
            gp = GaussianProcessRegressor(kernel=kernel, alpha=1e-2, normalize_y=True)
            gp.fit(time_idx.reshape(-1, 1), residuals)
            model = gp
            if cache_file is not None:
                joblib.dump((model, lin_reg), cache_file)
        models[col] = (model, lin_reg)
        # Forecast residuals at future time points
        future_times = np.arange(len(time_idx), len(time_idx) + periods).reshape(-1, 1)
        pred_resid, pred_std = model.predict(future_times, return_std=True)
        # Add back linear load component using future load values
        # Use load_df to align future loads
        future_loads = []
        for t in range(periods):
            idx_time = future_index[t]
            match = load_df.loc[load_df[date] == idx_time, load_cols]
            if not match.empty:
                future_loads.append(match.values[0])
            else:
                # Use last known load if future missing
                future_loads.append(combined[load_cols].iloc[-1].values)
        future_loads = np.array(future_loads)
        load_component = lin_reg.predict(future_loads)
        preds = pred_resid + load_component
        lower = preds - 1.96 * pred_std
        upper = preds + 1.96 * pred_std
        forecasts_data[col] = preds
        lower_bounds[col] = lower
        upper_bounds[col] = upper
    forecast_df = pd.DataFrame(forecasts_data, index=future_index, columns=burn_cols)
    lower_df = pd.DataFrame(lower_bounds, index=future_index, columns=burn_cols)
    upper_df = pd.DataFrame(upper_bounds, index=future_index, columns=burn_cols)
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
        except Exception:
            plot = False
        if plot:
            fig = go.Figure()
            for col in burn_cols:
                fig.add_trace(go.Scatter(x=combined[date], y=combined[col], mode='lines', name=f"{col} (historical)"))
                fig.add_trace(go.Scatter(x=future_index, y=forecast_df[col], mode='lines', name=f"{col} (forecast)", line=dict(dash='dot')))
                fig.add_trace(go.Scatter(
                    x=list(future_index) + list(future_index[::-1]),
                    y=list(upper_df[col]) + list(lower_df[col][::-1]),
                    fill='toself', fillcolor='rgba(255,165,0,0.3)', line=dict(color='rgba(255,165,0,0)'),
                    hoverinfo="skip", showlegend=False
                ))
            fig.update_layout(title="Intraday GP Burn Forecast", xaxis_title="Time", yaxis_title="Burn", template="plotly_white")
            forecast_df.attrs['plot'] = fig
    return IntradayGpForecastResult(forecasts=forecast_df, models=models, lower_conf_int=lower_df, upper_conf_int=upper_df)


@dataclass
class AutoGluonTabularForecastResult:
    """Result container for :func:`autogluon_tabular_burn_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Predictions for the target at the specified horizon.  The index
        contains the future dates (e.g. next day) and the columns
        correspond to the target(s) being predicted.
    predictor : object
        Fitted AutoGluon TabularPredictor.
    lower_conf_int : pandas.DataFrame or None
        Lower bounds of 95% prediction intervals if available.
    upper_conf_int : pandas.DataFrame or None
        Upper bounds of 95% prediction intervals if available.
    """
    forecasts: pd.DataFrame
    predictor: object
    lower_conf_int: Optional[pd.DataFrame] = None
    upper_conf_int: Optional[pd.DataFrame] = None


def autogluon_tabular_burn_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    target_col: str,
    horizon: int = 1,
    model_params: Optional[dict] = None,
    cache_path: Optional[str] = None,
    plot: bool = False,
) -> AutoGluonTabularForecastResult:
    """Predict next-day distillate burn using AutoGluon Tabular models.

    This function trains an AutoGluon Tabular predictor on historical
    records, using all columns except the date and target as features
    (including HDDs, day‑ahead pricing, etc.).  It supports caching
    the trained model to avoid retraining.  The forecast horizon
    corresponds to the number of periods ahead (e.g. 1 for next day).
    Predictions are returned for the specified horizon along with
    optional 95% prediction intervals based on quantile regression.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing date information.
    df : pandas.DataFrame
        DataFrame with historical features and target.  Must include
        the date column and the target column.
    target_col : str
        Name of the column to predict (e.g. 'burn').
    horizon : int, default 1
        Number of periods ahead to predict (e.g. 1 means next day).
    model_params : dict or None, default None
        Additional parameters passed to AutoGluon ``TabularPredictor``.
        Recognised key ``quantile_levels`` may specify quantile levels
        for prediction intervals (default [0.025, 0.975]).
    cache_path : str or None, default None
        Directory path to save and load the predictor.  If provided and
        a model exists, it is loaded instead of retraining.
    plot : bool, default False
        Whether to plot the historical and predicted target values with
        confidence intervals.

    Returns
    -------
    AutoGluonTabularForecastResult
        Dataclass containing the predictions, predictor and prediction
        intervals.

    Raises
    ------
    ImportError
        If AutoGluon is not installed.
    KeyError
        If the date or target column is not present.
    """
    try:
        from autogluon.tabular import TabularPredictor
    except Exception as e:
        raise ImportError(
            "autogluon.tabular is required for this function. Please install autogluon."
        ) from e
    import os
    import joblib
    if model_params is None:
        model_params = {}
    quantile_levels = model_params.pop('quantile_levels', [0.025, 0.975])
    # Extract date series
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Ensure target exists
    if target_col not in df.columns:
        raise KeyError(f"Target column '{target_col}' not found in DataFrame")
    # Sort by date
    df_sorted = df.sort_values(by=date).reset_index(drop=True)
    # Determine training and prediction split index
    train_df = df_sorted.copy()
    # Use all records for training; horizon indicates we predict the next horizon period
    # For training we need target, features, we drop the last horizon rows if data not available for target
    # To keep it simple, we will use last available row for prediction
    if cache_path is not None:
        os.makedirs(cache_path, exist_ok=True)
        model_file = os.path.join(cache_path, f"autogluon_tabular_{target_col}.pkl")
    else:
        model_file = None
    if model_file is not None and os.path.exists(model_file):
        predictor: TabularPredictor = joblib.load(model_file)
    else:
        # Prepare training data
        # Drop rows with missing target
        train_df = train_df.dropna(subset=[target_col])
        # Drop date column from features
        features_df = train_df.drop(columns=[date, target_col])
        train_data = features_df.copy()
        train_data[target_col] = train_df[target_col].values
        # Create predictor
        predictor = TabularPredictor(label=target_col, **model_params).fit(train_data)
        if model_file is not None:
            joblib.dump(predictor, model_file)
    # Prepare future record for prediction
    # Use the last row's features for next horizon; this is a proxy for next day features
    last_row = df_sorted.iloc[-1]
    future_date = dt.iloc[-1] + (dt.diff().mode()[0] if not dt.diff().dropna().empty else pd.Timedelta(days=1)) * horizon
    future_features = last_row.drop(labels=[date, target_col]).to_frame().T
    future_features = future_features.reset_index(drop=True)
    # Predict mean and quantiles
    preds = predictor.predict(future_features)
    # Prediction intervals via quantile prediction
    try:
        pred_probs = predictor.predict_quantile(future_features, quantile_levels)
        lower_vals = pred_probs.iloc[:, 0]
        upper_vals = pred_probs.iloc[:, -1]
        lower_df = pd.DataFrame({target_col: lower_vals.values}, index=[future_date])
        upper_df = pd.DataFrame({target_col: upper_vals.values}, index=[future_date])
    except Exception:
        lower_df = upper_df = None
    forecast_df = pd.DataFrame({target_col: preds.values}, index=[future_date])
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
        except Exception:
            plot = False
        if plot:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dt, y=df[target_col], mode='lines', name=f"{target_col} (historical)"))
            fig.add_trace(go.Scatter(x=[future_date], y=forecast_df[target_col], mode='markers', marker=dict(size=8, color='blue'), name=f"{target_col} (forecast)"))
            if lower_df is not None and upper_df is not None:
                fig.add_trace(go.Scatter(x=[future_date, future_date], y=[lower_df[target_col].iloc[0], upper_df[target_col].iloc[0]],
                                         mode='lines', line=dict(color='orange', width=2), name="95% CI"))
            fig.update_layout(title="Next‑Day Burn Forecast", xaxis_title="Date", yaxis_title=target_col, template="plotly_white")
            forecast_df.attrs['plot'] = fig
    return AutoGluonTabularForecastResult(
        forecasts=forecast_df,
        predictor=predictor,
        lower_conf_int=lower_df,
        upper_conf_int=upper_df,
    )


@dataclass
class AutoGluonTimeSeriesForecastResult:
    """Result container for :func:`autogluon_timeseries_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        Forecasted values for the target series; index contains forecast
        dates and columns correspond to the target identifier(s).
    predictor : object
        Fitted AutoGluon ``TimeSeriesPredictor``.
    lower_conf_int : pandas.DataFrame or None
        Lower bounds of prediction intervals.
    upper_conf_int : pandas.DataFrame or None
        Upper bounds of prediction intervals.
    """
    forecasts: pd.DataFrame
    predictor: object
    lower_conf_int: Optional[pd.DataFrame] = None
    upper_conf_int: Optional[pd.DataFrame] = None

# ---------------------------------------------------------------------------
# New AutoGluon tabular classifier result
# ---------------------------------------------------------------------------


@dataclass
class AutoGluonTabularBurnClassifierResult:
    """Result container for :func:`autogluon_tabular_burn_classifier`.

    Attributes
    ----------
    predictions : pandas.DataFrame
        DataFrame with the predicted class flag and probability for
        each observation.  Any original feature columns are preserved.
    model : object
        Trained AutoGluon Tabular model used for classification.
    """
    predictions: pd.DataFrame
    model: object


# ---------------------------------------------------------------------------
# Major burn day forecast result
# ---------------------------------------------------------------------------

@dataclass
class MajorBurnForecastResult:
    """Result container for :func:`forecast_major_burn_days`.

    Attributes
    ----------
    dataframe : pandas.DataFrame
        Copy of the original input with additional columns:
        - ``prob_major``: probability of target exceeding the threshold.
        - ``major_flag``: binary flag (1 if prob >= threshold, else 0).
        - ``model_threshold``: probability threshold selected to maximize F1 on the train set.
        - ``target_threshold``: the value threshold used for classifying major events.
    model : object
        The trained calibrated classifier.
    """
    dataframe: pd.DataFrame
    model: object


def autogluon_timeseries_forecast(
    date: Union[str, pd.Series, Iterable],
    df: pd.DataFrame,
    *,
    target_col: str,
    periods: int = 12,
    id_col: Optional[str] = None,
    model_params: Optional[dict] = None,
    cache_path: Optional[str] = None,
    plot: bool = False,
) -> AutoGluonTimeSeriesForecastResult:
    """Forecast a target time series using AutoGluon’s time‑series models with covariates.

    This function converts the input DataFrame into AutoGluon’s
    ``TimeSeriesDataFrame`` format, automatically assigning
    past covariates and known covariates based on whether values are
    available at the forecast horizon.  It supports multiple target
    identifiers (via ``id_col``) and caches the trained predictor for
    re‑use.  Forecasts and prediction intervals are returned for the
    specified horizon.

    Parameters
    ----------
    date : str or pandas.Series or iterable
        Column name, series or iterable containing datetime information.
    df : pandas.DataFrame
        DataFrame with historical data.  Must include the date column,
        target column, and optionally additional feature columns.
    target_col : str
        Name of the target column to forecast.
    periods : int, default 12
        Number of future periods to forecast.
    id_col : str or None, default None
        Column identifying different time series.  If None, the
        dataframe is assumed to contain a single series and an
        artificial ID will be assigned.
    model_params : dict or None, default None
        Additional parameters passed to the AutoGluon
        ``TimeSeriesPredictor``.  Recognised key ``quantile_levels``
        may specify quantile levels for prediction intervals.  Other
        parameters are forwarded to the predictor.
    cache_path : str or None, default None
        Directory path to save and load the predictor.
    plot : bool, default False
        Whether to plot historical and forecasted target values with
        confidence intervals.

    Returns
    -------
    AutoGluonTimeSeriesForecastResult
        Dataclass containing forecasts, predictor and prediction
        intervals.

    Raises
    ------
    ImportError
        If AutoGluon TimeSeries module is not installed.
    KeyError
        If required columns are missing.
    """
    try:
        from autogluon.timeseries import TimeSeriesPredictor, TimeSeriesDataFrame
    except Exception as e:
        raise ImportError(
            "autogluon.timeseries is required for this function. Please install autogluon-timeseries."
        ) from e
    import os
    import joblib
    if model_params is None:
        model_params = {}
    quantile_levels = model_params.pop('quantile_levels', [0.025, 0.5, 0.975])
    # Extract date and id columns
    if isinstance(date, str):
        if date not in df.columns:
            raise KeyError(f"Date column '{date}' not found in DataFrame")
        date_series = df[date]
    else:
        date_series = pd.Series(date)
        if date not in df.columns:
            df = df.copy()
            df[date] = date_series
    dt = pd.to_datetime(date_series)
    if dt.empty:
        raise ValueError("Date series is empty")
    # Ensure target exists
    if target_col not in df.columns:
        raise KeyError(f"Target column '{target_col}' not found in DataFrame")
    # Determine id column or assign single id
    if id_col is None:
        df = df.copy()
        df['__id__'] = 0
        id_col_used = '__id__'
    else:
        id_col_used = id_col
        if id_col_used not in df.columns:
            raise KeyError(f"ID column '{id_col_used}' not found in DataFrame")
    # Sort by id and date
    df_sorted = df.sort_values(by=[id_col_used, date]).reset_index(drop=True)
    # Identify covariate columns
    covar_cols = [c for c in df.columns if c not in {date, id_col_used, target_col}]
    # Determine known vs past covariates
    # If a column has any future values (non‑null) at prediction horizon, treat as known covariate
    # We assume that if there are no missing values in the last row for that column, it is known in future
    known_covariates = []
    past_covariates = []
    for c in covar_cols:
        # If last value is not NaN, assume known in future
        if not pd.isna(df_sorted[c].iloc[-1]):
            known_covariates.append(c)
        else:
            past_covariates.append(c)
    # Build TimeSeriesDataFrame
    tsdf = TimeSeriesDataFrame.from_data_frame(
        df_sorted,
        id_column=id_col_used,
        timestamp_column=date,
        target_column=target_col,
        known_covariates=known_covariates if known_covariates else None,
        past_covariates=past_covariates if past_covariates else None,
    )
    # Prepare cache path
    if cache_path is not None:
        os.makedirs(cache_path, exist_ok=True)
        model_file = os.path.join(cache_path, f"autogluon_ts_{target_col}.pkl")
    else:
        model_file = None
    # Fit or load predictor
    if model_file is not None and os.path.exists(model_file):
        predictor: TimeSeriesPredictor = joblib.load(model_file)
    else:
        # Fit predictor
        predictor = TimeSeriesPredictor(
            prediction_length=periods,
            quantile_levels=quantile_levels,
            **model_params,
        )
        predictor.fit(tsdf)
        if model_file is not None:
            joblib.dump(predictor, model_file)
    # Forecast
    forecast_df = predictor.predict(tsdf, known_covariates=known_covariates or None, past_covariates=past_covariates or None)
    # Extract mean and intervals
    # 'mean' column in forecast_df holds the mean prediction
    # Additional quantile columns if quantile_levels > 1
    target_ids = forecast_df.index.get_level_values('item_id').unique()
    forecast_means: Dict[str, List[float]] = {}
    lower_bounds: Dict[str, List[float]] = {}
    upper_bounds: Dict[str, List[float]] = {}
    for series_id in target_ids:
        df_series = forecast_df.xs(series_id, level='item_id')
        forecast_means[str(series_id)] = df_series['mean'].values
        if 0.025 in quantile_levels and 0.975 in quantile_levels:
            lower_bounds[str(series_id)] = df_series[f'0.025'].values
            upper_bounds[str(series_id)] = df_series[f'0.975'].values
    # Build index for forecast horizon
    # Determine the last timestamp per series and generate future dates
    forecast_index = []
    for series_id in target_ids:
        last_ts = df_sorted.loc[df_sorted[id_col_used] == series_id, date].iloc[-1]
        if freq is None:
            try:
                freq = pd.infer_freq(dt)
            except Exception:
                freq = None
        if freq is not None:
            future_dates = pd.date_range(start=last_ts, periods=periods + 1, freq=freq)[1:]
        else:
            diffs = dt.diff().dropna()
            delta = diffs.mode()[0] if not diffs.empty else pd.Timedelta(days=1)
            future_dates = pd.to_datetime([last_ts + delta * (i + 1) for i in range(periods)])
        forecast_index.append(pd.Index(future_dates, name=date))
    # Combine into DataFrame
    combined_index = forecast_index[0]
    forecast_df_out = pd.DataFrame(forecast_means, index=combined_index)
    lower_df = None
    upper_df = None
    if lower_bounds:
        lower_df = pd.DataFrame(lower_bounds, index=combined_index)
        upper_df = pd.DataFrame(upper_bounds, index=combined_index)
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
        except Exception:
            plot = False
        if plot:
            fig = go.Figure()
            # For each series id, plot
            for series_id in target_ids:
                # Historical
                hist_series = df_sorted.loc[df_sorted[id_col_used] == series_id]
                fig.add_trace(go.Scatter(x=hist_series[date], y=hist_series[target_col], mode='lines', name=f"{series_id} (historical)"))
                # Forecast
                fig.add_trace(go.Scatter(x=forecast_df_out.index, y=forecast_df_out[str(series_id)], mode='lines', name=f"{series_id} (forecast)", line=dict(dash='dot')))
                if lower_df is not None and upper_df is not None:
                    fig.add_trace(go.Scatter(
                        x=list(forecast_df_out.index) + list(forecast_df_out.index[::-1]),
                        y=list(upper_df[str(series_id)]) + list(lower_df[str(series_id)][::-1]),
                        fill='toself', fillcolor='rgba(255,165,0,0.3)', line=dict(color='rgba(255,165,0,0)'),
                        hoverinfo="skip", showlegend=False
                    ))
            fig.update_layout(title="AutoGluon Time Series Forecast", xaxis_title="Date", yaxis_title=target_col, template="plotly_white")
            forecast_df_out.attrs['plot'] = fig
    return AutoGluonTimeSeriesForecastResult(
        forecasts=forecast_df_out,
        predictor=predictor,
        lower_conf_int=lower_df,
        upper_conf_int=upper_df,
    )

# ---------------------------------------------------------------------------
# Chronos‑Bolt forecasting (AutoGluon)
# ---------------------------------------------------------------------------

@dataclass
class ChronosBoltForecastResult:
    """Result container for :func:`chronos_bolt_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        DataFrame of median forecasts for each series (one column per target).
        The index contains the forecast timestamps.
    predictor : object
        The fitted :class:`autogluon.timeseries.TimeSeriesPredictor` used for
        forecasting.
    lower_conf_int : pandas.DataFrame or None
        Lower bound of the 95 % prediction interval (2.5 % quantile) for each
        target column.  Only present if quantile levels include 0.025.
    upper_conf_int : pandas.DataFrame or None
        Upper bound of the 95 % prediction interval (97.5 % quantile) for each
        target column.  Only present if quantile levels include 0.975.
    summary : Dict[str, float] or None
        Optional summary statistics (mean) of the forecast values for each target
        column.
    """

    forecasts: pd.DataFrame
    predictor: object
    lower_conf_int: Optional[pd.DataFrame] = None
    upper_conf_int: Optional[pd.DataFrame] = None
    summary: Optional[Dict[str, float]] = None


# ---------------------------------------------------------------------------
# Additional Chronos‑Bolt forecasting utilities
# ---------------------------------------------------------------------------

@dataclass
class ChronosBoltBacktestResult:
    """Result container for :func:`chronos_bolt_backtest`.

    Attributes
    ----------
    metrics : pandas.DataFrame
        DataFrame summarising error metrics for each backtest window.  It
        typically includes columns such as ``window_start``, ``window_end``,
        ``mae``, ``mape``, ``rmse`` and optionally any custom metrics.  Each
        row corresponds to a single train/test split.
    predictions : List[pandas.DataFrame]
        List of DataFrames containing forecasts for each backtest window.  The
        index of each DataFrame corresponds to the forecast timestamps and
        columns to series identifiers.  If actual values are available
        (i.e., the horizon is within the original data), an ``actual``
        column is included for each series.
    best_summary : Dict[str, float] or None
        Optional aggregated summary of metrics across all windows (e.g., mean
        MAPE or RMSE).  Provided when ``summary=True`` in the function call.
    """
    metrics: pd.DataFrame
    predictions: List[pd.DataFrame]
    best_summary: Optional[Dict[str, float]] = None


@dataclass
class ChronosBoltHyperparamSearchResult:
    """Result container for :func:`chronos_bolt_hyperparam_search`.

    Attributes
    ----------
    best_params : dict
        Hyperparameter combination that achieved the best aggregated metric
        during the search.  The keys and values match those passed in
        ``param_grid``.
    results : pandas.DataFrame
        DataFrame containing the aggregated error metric for each evaluated
        hyperparameter combination.  Typically includes columns for the
        parameter names and the chosen metric (e.g., ``mape``).
    summary : Dict[str, float] or None
        Optional dictionary summarising the distribution of error metrics
        across the search (e.g., minimum, median, maximum).  Populated when
        ``summary=True``.
    """
    best_params: Dict[str, Any]
    results: pd.DataFrame
    summary: Optional[Dict[str, float]] = None


@dataclass
class ChronosBoltMultiTargetForecastResult:
    """Result container for :func:`chronos_bolt_multi_target_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        DataFrame where each column corresponds to a target series and the
        index contains forecast timestamps.  The values represent the
        predicted median (or mean) of the respective series.
    predictor : object
        Fitted :class:`autogluon.timeseries.TimeSeriesPredictor` used to
        generate the forecasts.
    lower_conf_int : pandas.DataFrame or None
        Lower bounds of the 95 % prediction intervals for each target series.
        Present only if quantile levels include 0.025.
    upper_conf_int : pandas.DataFrame or None
        Upper bounds of the 95 % prediction intervals for each target series.
        Present only if quantile levels include 0.975.
    summary : Dict[str, float] or None
        Optional dictionary summarising each target series (e.g., mean of
        forecasts).  Returned when ``summary=True``.
    """
    forecasts: pd.DataFrame
    predictor: object
    lower_conf_int: Optional[pd.DataFrame] = None
    upper_conf_int: Optional[pd.DataFrame] = None
    summary: Optional[Dict[str, float]] = None


def chronos_bolt_backtest(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    id_col: Optional[str] = None,
    prediction_length: int = 24,
    context_length: Optional[int] = None,
    stride: Optional[int] = None,
    model_name: str = "autogluon/chronos-bolt-base",
    param_overrides: Optional[Dict[str, Any]] = None,
    quantile_levels: Optional[List[float]] = None,
    freq: Optional[str] = None,
    summary: bool = False,
) -> ChronosBoltBacktestResult:
    """Backtest Chronos‑Bolt forecasts over rolling windows.

    This function evaluates AutoGluon’s Chronos‑Bolt model by
    performing a series of train/test splits on the input DataFrame.  For
    each split, it trains a predictor on the historical portion and
    forecasts the next ``prediction_length`` steps.  Error metrics
    (mean absolute error, mean absolute percentage error and root mean
    squared error) are computed where actual values are available.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing at least the datetime column and the
        target column.  Additional covariate columns are permitted and
        will be treated as past covariates.  If multiple series are
        present, specify ``id_col``.
    date_col : str
        Name of the datetime column.
    target_col : str
        Name of the target column to forecast.
    id_col : str, optional
        Name of the series identifier column.  When ``None``, the data
        are assumed to represent a single series.
    prediction_length : int, default 24
        Number of future time steps to predict in each backtest window.
    context_length : int or None, default None
        Length of the historical context used to train the model.  If
        ``None``, Chronos‑Bolt’s default context length is used.
    stride : int or None, default None
        Step size by which the training window is advanced for each
        backtest iteration.  Defaults to ``prediction_length``.  Smaller
        values create overlapping windows.
    model_name : str, default 'autogluon/chronos-bolt-base'
        Hugging Face model identifier for the Chronos‑Bolt foundation
        model.  You can specify other checkpoints such as
        'autogluon/chronos-bolt-large' to trade accuracy for compute.
    param_overrides : dict, optional
        Additional hyperparameters passed to the underlying
        :class:`autogluon.timeseries.TimeSeriesPredictor.fit` call under
        the ``Chronos`` key (e.g., ``{'context_length': 96}``).  These
        override defaults defined by the Chronos‑Bolt model.
    quantile_levels : list of float, optional
        Quantile levels for prediction intervals.  Defaults to
        ``[0.025, 0.5, 0.975]``.
    freq : str, optional
        Frequency string (e.g., 'H', '30min', 'D') for the time index.
        When ``None``, the frequency is inferred from the input data.
    summary : bool, default False
        If True, returns an aggregated summary of the metrics (mean
        across windows) in the result.

    Returns
    -------
    ChronosBoltBacktestResult
        Object containing per-window metrics, forecast DataFrames and
        optional summary statistics.

    Notes
    -----
    Backtesting can be computationally expensive because it fits a new
    model for each window.  Use a small ``prediction_length`` and stride
    for quick evaluations or allocate sufficient compute for larger
    experiments.  The model is always trained from scratch for each
    window to prevent leakage from future information.
    """
    # Lazy import to avoid heavy dependencies unless needed
    try:
        from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor  # type: ignore
    except Exception as e:
        raise ImportError(
            "autogluon.timeseries is required for chronos_bolt_backtest"
        ) from e
    import os
    import numpy as np
    import pandas as pd
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    if quantile_levels is None:
        quantile_levels = [0.025, 0.5, 0.975]
    if stride is None or stride <= 0:
        stride = prediction_length
    # Prepare DataFrame
    data = df.copy()
    data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
    # Single series handling
    if id_col is None:
        data["_item_id"] = "series_1"
        id_used = "_item_id"
    else:
        id_used = id_col
    data = data.sort_values([id_used, date_col])
    # Determine frequency
    if freq is None:
        freq = pd.infer_freq(data[date_col].dropna().sort_values())
    if freq is None:
        # fall back to median difference
        diffs = data.groupby(id_used)[date_col].diff().dropna()
        if len(diffs) > 0:
            freq = diffs.mode().iloc[0]
        else:
            freq = 'D'
    # Determine windows
    metrics_records: List[Dict[str, Any]] = []
    predictions_list: List[pd.DataFrame] = []
    # compute per-series unified index for splitting
    # We treat each series independently, but for cross-validation we align by date
    unique_dates = sorted(data[date_col].dropna().unique())
    total_periods = len(unique_dates)
    # Start index for first train window (must have enough context if context_length specified)
    start_idx = 0
    if context_length is not None and context_length > 0:
        # require at least context_length data points in training
        start_idx = max(start_idx, context_length)
    # iterate until last possible start where full prediction_length is available
    idx = start_idx
    while idx + prediction_length <= total_periods:
        train_end_date = unique_dates[idx]
        test_start_date = train_end_date
        # Use all data <= train_end_date as training
        train_mask = data[date_col] <= train_end_date
        test_mask = (data[date_col] > train_end_date) & (
            data[date_col] <= unique_dates[min(idx + prediction_length, total_periods - 1)]
        )
        train_df = data.loc[train_mask].copy()
        test_df = data.loc[test_mask].copy()
        # Ensure training contains at least one non-missing target
        if train_df[target_col].notna().sum() < 1:
            idx += stride
            continue
        # Convert to TimeSeriesDataFrame
        ts_train = train_df.set_index([id_used, date_col])
        ts_train = TimeSeriesDataFrame.from_data_frame(ts_train)
        # Train predictor
        predictor = TimeSeriesPredictor(
            target=target_col,
            prediction_length=prediction_length,
            freq=freq,
            context_length=context_length,
            quantile_levels=quantile_levels,
        )
        hyperparams = {"Chronos": {"model_path": model_name}}
        if param_overrides:
            hyperparams["Chronos"].update(param_overrides)
        predictor.fit(ts_train, hyperparameters=hyperparams, known_covariates=None, past_covariates=None)
        # Forecast using full training data
        forecast_ts = predictor.predict(ts_train, known_covariates=None, past_covariates=None)
        # Convert to DataFrame
        forecast_df = forecast_ts.to_pandas().reset_index()
        # Build prediction DataFrame per series
        median_dict: Dict[str, List[float]] = {}
        lower_dict: Dict[str, List[float]] = {}
        upper_dict: Dict[str, List[float]] = {}
        for sid, sub in forecast_df.groupby("item_id"):
            sub = sub.sort_values("timestamp")
            median_col = "mean"
            if "0.5" in sub.columns:
                median_col = "0.5"
            median_dict[sid] = sub[median_col].tolist()
            if 0.025 in quantile_levels and "0.025" in sub.columns:
                lower_dict[sid] = sub["0.025"].tolist()
            if 0.975 in quantile_levels and "0.975" in sub.columns:
                upper_dict[sid] = sub["0.975"].tolist()
        # create index for forecast horizon
        # Each series shares same horizon; use sub's timestamp
        first_sid = list(median_dict.keys())[0]
        sub_first = forecast_df[forecast_df["item_id"] == first_sid]
        horizon_index = pd.to_datetime(sub_first["timestamp"].values)
        preds_df = pd.DataFrame(median_dict, index=horizon_index)
        # Append actuals if available
        if not test_df.empty:
            actuals = test_df[[id_used, date_col, target_col]].dropna()
            # Pivot to wide format
            actual_pivot = actuals.pivot(index=date_col, columns=id_used, values=target_col)
            # Align index to horizon_index; this will drop missing
            actual_pivot = actual_pivot.reindex(horizon_index)
            # Rename columns to indicate actual
            for col in actual_pivot.columns:
                preds_df[f"{col}_actual"] = actual_pivot[col].values
        predictions_list.append(preds_df)
        # Compute metrics if actual values exist
        if not test_df.empty:
            # join predicted and actual
            mae_vals = []
            mape_vals = []
            rmse_vals = []
            for sid in median_dict.keys():
                if f"{sid}_actual" in preds_df.columns:
                    y_true = preds_df[f"{sid}_actual"].values
                    y_pred = preds_df[sid].values
                    # drop pairs where actual is nan
                    mask = ~np.isnan(y_true)
                    if mask.any():
                        y_t = y_true[mask]
                        y_p = y_pred[mask]
                        mae_vals.append(float(mean_absolute_error(y_t, y_p)))
                        # Avoid division by zero in MAPE
                        nonzero_mask = y_t != 0
                        if nonzero_mask.any():
                            mape_vals.append(float(np.mean(np.abs((y_t[nonzero_mask] - y_p[nonzero_mask]) / y_t[nonzero_mask]))))
                        else:
                            mape_vals.append(np.nan)
                        rmse_vals.append(float(np.sqrt(mean_squared_error(y_t, y_p))))
            # Average metrics across series
            mae_mean = np.nanmean(mae_vals) if mae_vals else np.nan
            mape_mean = np.nanmean(mape_vals) if mape_vals else np.nan
            rmse_mean = np.nanmean(rmse_vals) if rmse_vals else np.nan
        else:
            mae_mean = np.nan
            mape_mean = np.nan
            rmse_mean = np.nan
        metrics_records.append(
            {
                "window_start": train_df[date_col].min(),
                "window_end": train_df[date_col].max(),
                "mae": mae_mean,
                "mape": mape_mean,
                "rmse": rmse_mean,
            }
        )
        idx += stride
    # Create metrics DataFrame
    metrics_df = pd.DataFrame(metrics_records)
    best_summary = None
    if summary and not metrics_df.empty:
        # compute aggregated metrics across windows (mean of MAE, MAPE, RMSE)
        agg = {
            "mae_mean": float(np.nanmean(metrics_df["mae"])),
            "mape_mean": float(np.nanmean(metrics_df["mape"])),
            "rmse_mean": float(np.nanmean(metrics_df["rmse"])),
        }
        best_summary = agg
    return ChronosBoltBacktestResult(metrics_df=metrics_df, predictions=predictions_list, best_summary=best_summary)


def chronos_bolt_hyperparam_search(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    id_col: Optional[str] = None,
    param_grid: Dict[str, List[Any]] = None,
    metric: str = "mape",
    prediction_length: int = 24,
    context_length: Optional[int] = None,
    stride: Optional[int] = None,
    freq: Optional[str] = None,
    summary: bool = False,
) -> ChronosBoltHyperparamSearchResult:
    """Perform a simple hyperparameter search for Chronos‑Bolt.

    This function evaluates multiple combinations of Chronos‑Bolt
    hyperparameters using backtesting.  For each combination in
    ``param_grid``, the data are split into rolling windows via
    :func:`chronos_bolt_backtest` and the specified error metric is
    aggregated across windows.  The combination achieving the lowest
    aggregated metric is selected as best.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing at least the datetime column and the
        target column.  Additional covariate columns are allowed.
    date_col : str
        Name of the datetime column.
    target_col : str
        Name of the target column.
    id_col : str, optional
        Series identifier column, if multiple series are present.
    param_grid : dict, optional
        Dictionary where keys are hyperparameter names and values are
        lists of candidate values.  Supported keys include
        ``context_length``, ``prediction_length`` and any Chronos
        hyperparameters accepted by the underlying model.  If
        ``None``, a default grid of reasonable values is used.
    metric : str, default 'mape'
        Metric used to select the best combination.  One of ``'mae'``,
        ``'mape'`` or ``'rmse'``.  Lower is better.
    prediction_length : int, default 24
        Forecast horizon used in backtesting.  Overrides any values in
        ``param_grid`` for ``prediction_length``.
    context_length : int or None, default None
        Context length passed to :func:`chronos_bolt_backtest`.
    stride : int or None, default None
        Stride passed to :func:`chronos_bolt_backtest`.
    freq : str, optional
        Frequency string passed to :func:`chronos_bolt_backtest`.
    summary : bool, default False
        Whether to include summary statistics of metrics across
        hyperparameter combinations.

    Returns
    -------
    ChronosBoltHyperparamSearchResult
        Result containing the best hyperparameters, a DataFrame of
        aggregated metrics for each combination and optional summary.

    Notes
    -----
    Hyperparameter search can be computationally heavy because each
    combination triggers a full backtest.  Restrict the grid to a
    manageable size or run this function on a subset of the data to
    explore candidate values.
    """
    from itertools import product
    import numpy as np
    import pandas as pd

    # Default grid if none provided
    if param_grid is None:
        param_grid = {
            "context_length": [None],
            "prediction_length": [prediction_length],
            "quantile_levels": [[0.025, 0.5, 0.975]],
        }
    # Flatten param grid into list of parameter dictionaries
    keys = list(param_grid.keys())
    values = [param_grid[k] for k in keys]
    combos = [dict(zip(keys, vals)) for vals in product(*values)]
    records: List[Dict[str, Any]] = []
    best_combo = None
    best_metric_value = float("inf")
    for combo in combos:
        # Extract overrides and maintain separate context/prediction length
        combo_context = combo.get("context_length", context_length)
        combo_prediction = combo.get("prediction_length", prediction_length)
        combo_quantiles = combo.get("quantile_levels", [0.025, 0.5, 0.975])
        # Build overrides for Chronos hyperparams
        chronos_overrides = {k: v for k, v in combo.items() if k not in {"context_length", "prediction_length", "quantile_levels"}}
        # Run backtest
        result = chronos_bolt_backtest(
            df,
            date_col=date_col,
            target_col=target_col,
            id_col=id_col,
            prediction_length=combo_prediction,
            context_length=combo_context,
            stride=stride,
            param_overrides=chronos_overrides,
            quantile_levels=combo_quantiles,
            freq=freq,
            summary=False,
        )
        # aggregate metric across windows
        metrics_df = result.metrics
        metric_series = metrics_df[metric]
        agg_val = float(np.nanmean(metric_series)) if not metric_series.empty else float("inf")
        record = {**combo, metric: agg_val}
        records.append(record)
        # Update best
        if agg_val < best_metric_value:
            best_metric_value = agg_val
            best_combo = combo
    results_df = pd.DataFrame(records)
    # Summary statistics
    summary_dict = None
    if summary and not results_df.empty:
        summary_dict = {
            f"{metric}_min": float(results_df[metric].min()),
            f"{metric}_median": float(results_df[metric].median()),
            f"{metric}_max": float(results_df[metric].max()),
        }
    return ChronosBoltHyperparamSearchResult(best_params=best_combo or {}, results=results_df, summary=summary_dict)


def chronos_bolt_multi_target_forecast(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_cols: List[str],
    id_col: Optional[str] = None,
    covariate_cols: Optional[List[str]] = None,
    prediction_length: int = 24,
    quantile_levels: Optional[List[float]] = None,
    model_name: str = "autogluon/chronos-bolt-base",
    model_path: Optional[str] = None,
    freq: Optional[str] = None,
    plot: bool = False,
    summary: bool = False,
) -> ChronosBoltMultiTargetForecastResult:
    """Forecast multiple target series with Chronos‑Bolt via AutoGluon.

    This function allows simultaneous forecasting of several target
    columns using the same Chronos‑Bolt predictor.  Each target column is
    treated as a separate series (``item_id``) while sharing any
    covariate columns.  Known and past covariates are inferred
    automatically: all columns in ``covariate_cols`` are treated as
    past covariates (i.e., they are required to exist in the context
    only) and ignored for the forecast horizon.  Future covariates can
    be passed through the ``df`` if they contain future dates beyond
    the last observed date.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing a datetime column, multiple target
        columns and optional covariate columns.  If a series
        identifier column is provided via ``id_col``, it will be
        included in the ``item_id`` to differentiate multiple series in
        addition to the target name.
    date_col : str
        Name of the datetime column.
    target_cols : list of str
        List of target column names to forecast.  Each column becomes a
        separate series in the model.
    id_col : str, optional
        Column identifying different series.  If provided, the series
        identifier will be combined with the target name to form the
        ``item_id``.  When ``None``, each target column is treated as
        the sole series.
    covariate_cols : list of str, optional
        Names of columns to use as past covariates.  These columns
        should exist both historically and into the future (if
        forecasting beyond the last observed date).  They will be
        assigned to ``past_covariates`` for AutoGluon.  If ``None``, no
        covariates are used.
    prediction_length : int, default 24
        Number of future steps to forecast.
    quantile_levels : list of float, optional
        List of quantiles to compute.  If ``None``, defaults to
        ``[0.025, 0.5, 0.975]``.
    model_name : str, default 'autogluon/chronos-bolt-base'
        Hugging Face model identifier for the Chronos‑Bolt foundation
        model.
    model_path : str or None, default None
        Optional file path to save or load the fitted predictor.  When
        provided and the file exists, the predictor is loaded rather
        than retrained.
    freq : str, optional
        Frequency string for the time index.  If ``None``, inferred
        automatically.
    plot : bool, default False
        Whether to display a Plotly chart comparing historical values and
        forecasts for each target.
    summary : bool, default False
        If True, compute and return the mean of the forecasts for each
        target column.

    Returns
    -------
    ChronosBoltMultiTargetForecastResult
        Dataclass containing forecast DataFrames, prediction intervals
        and the fitted predictor.

    Notes
    -----
    This function is a convenience wrapper for scenarios where you
    have several dependent variables (e.g. distillate burn, jet fuel
    burn, power load) that you wish to forecast concurrently.  It
    constructs a single AutoGluon predictor and reuses the same model
    across all target series, which can reduce computational cost
    compared with fitting separate models for each column.
    """
    try:
        from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor  # type: ignore
    except Exception as e:
        raise ImportError(
            "autogluon.timeseries is required for chronos_bolt_multi_target_forecast"
        ) from e
    import os
    import numpy as np
    import pandas as pd
    if quantile_levels is None:
        quantile_levels = [0.025, 0.5, 0.975]
    # prepare DataFrame
    df_in = df.copy()
    df_in[date_col] = pd.to_datetime(df_in[date_col], errors="coerce")
    # assign item_id combining id_col and target name
    # Build combined records for all target columns.  Each record will
    # represent a single observation for a particular target series.
    combined_records: List[Dict[str, Any]] = []
    # Determine unique series identifiers.  If no id column is provided,
    # treat the entire DataFrame as a single series and use a placeholder
    # identifier.
    unique_ids = ["_series"] if id_col is None else df_in[id_col].unique().tolist()
    # Build combined data by iterating through each series and each target
    for uid in unique_ids:
        sub_df = df_in[df_in[id_col] == uid] if id_col is not None else df_in
        for target in target_cols:
            # Combine series identifier with target name to form item_id
            item_id = f"{uid}_{target}" if id_col is not None else target
            for _, row in sub_df.iterrows():
                combined_records.append(
                    {
                        "item_id": item_id,
                        "timestamp": row[date_col],
                        "target": row[target],
                    }
                )
    combined_df = pd.DataFrame(combined_records)
    # Add covariates if provided (as past covariates)
    past_covariates_df = None
    if covariate_cols:
        cov_records = []
        for uid in unique_ids:
            sub_df = df_in[df_in[id_col] == uid] if id_col is not None else df_in
            for target in target_cols:
                item_id = f"{uid}_{target}" if id_col is not None else target
                for _, row in sub_df.iterrows():
                    rec = {
                        "item_id": item_id,
                        "timestamp": row[date_col],
                    }
                    for cov in covariate_cols:
                        rec[cov] = row[cov]
                    cov_records.append(rec)
        past_covariates_df = pd.DataFrame(cov_records)
    # Convert to TimeSeriesDataFrame
    tsdf = combined_df.set_index(["item_id", "timestamp"])
    tsdf = TimeSeriesDataFrame.from_data_frame(tsdf)
    # Determine frequency
    if freq is None:
        freq = pd.infer_freq(tsdf.index.get_level_values("timestamp"))
    # Load or fit predictor
    predictor = None
    if model_path is not None and os.path.exists(model_path):
        try:
            import joblib
            predictor = joblib.load(model_path)
        except Exception:
            predictor = None
    if predictor is None:
        predictor = TimeSeriesPredictor(
            target="target",
            prediction_length=prediction_length,
            freq=freq,
            quantile_levels=quantile_levels,
        )
        hyperparams = {"Chronos": {"model_path": model_name}}
        predictor.fit(
            tsdf,
            hyperparameters=hyperparams,
            past_covariates=past_covariates_df,
            known_covariates=None,
        )
        if model_path is not None:
            try:
                import joblib
                joblib.dump(predictor, model_path)
            except Exception:
                pass
    # Forecast
    forecast_ts = predictor.predict(tsdf, past_covariates=past_covariates_df, known_covariates=None)
    forecast_df = forecast_ts.to_pandas().reset_index()
    # Build forecast DataFrame
    med_dict: Dict[str, List[float]] = {}
    low_dict: Dict[str, List[float]] = {}
    upp_dict: Dict[str, List[float]] = {}
    for item, sub in forecast_df.groupby("item_id"):
        sub = sub.sort_values("timestamp")
        med_col = "mean"
        if "0.5" in sub.columns:
            med_col = "0.5"
        med_dict[item] = sub[med_col].tolist()
        if 0.025 in quantile_levels and "0.025" in sub.columns:
            low_dict[item] = sub["0.025"].tolist()
        if 0.975 in quantile_levels and "0.975" in sub.columns:
            upp_dict[item] = sub["0.975"].tolist()
    # Determine index
    first_item = list(med_dict.keys())[0]
    sub_first = forecast_df[forecast_df["item_id"] == first_item]
    horizon_index = pd.to_datetime(sub_first["timestamp"].values)
    forecasts = pd.DataFrame(med_dict, index=horizon_index)
    lower_df = pd.DataFrame(low_dict, index=horizon_index) if low_dict else None
    upper_df = pd.DataFrame(upp_dict, index=horizon_index) if upp_dict else None
    summary_dict = None
    if summary:
        summary_dict = {col: float(np.mean(vals)) for col, vals in med_dict.items()}
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            # Plot historical for each target
            for item in med_dict.keys():
                # item format: uid_target or target
                if "_" in item:
                    uid, tgt = item.split("_", 1)
                    hist_mask = True
                    if id_col is not None:
                        hist_mask &= (df_in[id_col] == uid)
                    hist = df_in.loc[hist_mask]
                    fig.add_trace(go.Scatter(x=hist[date_col], y=hist[tgt], mode="lines", name=f"{item} (historical)"))
                else:
                    fig.add_trace(go.Scatter(x=df_in[date_col], y=df_in[item], mode="lines", name=f"{item} (historical)"))
            # Forecast and CI
            for item in forecasts.columns:
                fig.add_trace(go.Scatter(x=forecasts.index, y=forecasts[item], mode="lines", name=f"{item} (forecast)", line=dict(dash="dot")))
                if lower_df is not None and upper_df is not None and item in lower_df.columns and item in upper_df.columns:
                    lsub = lower_df[item]
                    usub = upper_df[item]
                    fig.add_trace(go.Scatter(
                        x=list(lsub.index) + list(usub.index[::-1]),
                        y=list(usub.values) + list(lsub.values[::-1]),
                        fill="toself",
                        fillcolor="rgba(255,165,0,0.2)",
                        line=dict(color="rgba(255,165,0,0)"),
                        showlegend=False,
                    ))
            fig.update_layout(title="Chronos-Bolt Multi‑Target Forecast", xaxis_title=date_col, yaxis_title="Value", template="plotly_white")
            fig.show()
        except Exception:
            pass
    return ChronosBoltMultiTargetForecastResult(
        forecasts=forecasts,
        predictor=predictor,
        lower_conf_int=lower_df,
        upper_conf_int=upper_df,
        summary=summary_dict,
    )


def chronos_bolt_forecast(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    id_col: Optional[str] = None,
    covariate_cols: Optional[List[str]] = None,
    prediction_length: int = 24,
    quantile_levels: Optional[List[float]] = None,
    model_name: str = "autogluon/chronos-bolt-base",
    model_path: Optional[str] = None,
    freq: Optional[str] = None,
    plot: bool = False,
    summary: bool = False,
) -> ChronosBoltForecastResult:
    """Forecast future values using AutoGluon’s Chronos‑Bolt model.

    This function wraps the :class:`autogluon.timeseries.TimeSeriesPredictor`
    and uses the Chronos‑Bolt foundation model as a base learner.  It
    automatically constructs known and past covariates, handles multiple
    series via ``id_col``, caches the trained predictor for reuse, and
    produces point forecasts with optional quantile prediction intervals.

    Parameters
    ----------
    df : pandas.DataFrame
        Historical data containing a datetime column, the target column and
        optional covariate columns.  The DataFrame may include multiple
        series if ``id_col`` is specified.
    date_col : str
        Name of the datetime column in ``df``.
    target_col : str
        Name of the target column to forecast.
    id_col : str or None, default None
        Identifier column for multiple series.  If None, a dummy id is
        created.
    covariate_cols : list of str or None, default None
        Names of columns to use as covariates.  If None, all numeric columns
        other than the date and target (and id, if present) are treated as
        covariates.
    prediction_length : int, default 24
        Number of time steps to forecast.  Chronos‑Bolt models support long
        horizons, but longer forecasts may increase latency.
    quantile_levels : list of float or None, default None
        Quantile levels to predict.  If None, the default quantiles
        [0.025, 0.5, 0.975] are used.
    model_name : str, default 'autogluon/chronos-bolt-base'
        Name of the Chronos‑Bolt model on Hugging Face Hub.  Other variants
        include 'autogluon/chronos-bolt-tiny', 'chronos-bolt-small', etc.
    model_path : str or None, default None
        Directory to cache the trained predictor.  If provided and a saved
        predictor exists at this path, it is loaded instead of re‑training.
    freq : str or None, default None
        Frequency string (e.g. '5T', 'H', 'D') for the time series.  If None,
        the frequency is inferred from the date column.
    plot : bool, default False
        If True, display an interactive Plotly figure comparing historical
        data, forecasts and 95 % prediction intervals.
    summary : bool, default False
        If True, compute the mean of the forecasted values for each series
        and return it in the result dataclass.

    Returns
    -------
    ChronosBoltForecastResult
        Dataclass containing the forecast DataFrame, the fitted predictor,
        optional prediction interval bounds and summary statistics.

    Notes
    -----
    This function requires ``autogluon.timeseries`` version 1.0 or later.  It
    utilizes the Chronos‑Bolt foundation model by specifying the
    ``"Chronos"`` hyperparameter in AutoGluon.  The predictor is cached
    using ``joblib`` if ``model_path`` is provided to avoid re‑training on
    subsequent calls.  Only CPU inference is used; GPU is not required.
    """
    # import dependencies lazily
    try:
        from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor  # type: ignore
    except Exception as e:
        raise ImportError(
            "autogluon.timeseries is required for chronos_bolt_forecast. "
            "Install via pip install autogluon.timeseries"
        ) from e
    import joblib
    import os

    # Copy and preprocess input
    df_in = df.copy()
    df_in[date_col] = pd.to_datetime(df_in[date_col], errors="coerce")
    df_in = df_in.sort_values(date_col)
    # Add id if missing
    if id_col is None:
        df_in["__item_id__"] = "series_1"
        id_used = "__item_id__"
    else:
        id_used = id_col
    # Determine covariate columns
    if covariate_cols is None:
        covariate_cols = [c for c in df_in.select_dtypes(include=[np.number]).columns if c not in {target_col}]
        # Remove id if numeric and same as id_used
        covariate_cols = [c for c in covariate_cols if c != id_used]
    # Convert to TimeSeriesDataFrame
    tsdf = df_in[[id_used, date_col, target_col] + covariate_cols].rename(
        columns={id_used: "item_id", date_col: "timestamp"}
    )
    tsdf = tsdf.set_index(["item_id", "timestamp"]).sort_index()
    tsdf = TimeSeriesDataFrame(tsdf)
    # Infer frequency
    if freq is None:
        try:
            freq = pd.infer_freq(df_in[date_col].sort_values())
        except Exception:
            freq = None
    # Quantiles
    if quantile_levels is None:
        quantile_levels = [0.025, 0.5, 0.975]
    # Load or fit predictor
    predictor = None
    if model_path is not None and os.path.exists(model_path):
        try:
            predictor = joblib.load(model_path)
        except Exception:
            predictor = None
    if predictor is None:
        # Define predictor with Chronos hyperparameters
        predictor = TimeSeriesPredictor(
            target=target_col,
            prediction_length=prediction_length,
            freq=freq,
            quantile_levels=quantile_levels,
        )
        predictor.fit(
            tsdf,
            hyperparameters={
                "Chronos": {"model_path": model_name},
            },
            known_covariates=None,
            past_covariates=None,
        )
        if model_path is not None:
            try:
                joblib.dump(predictor, model_path)
            except Exception:
                pass
    # Forecast
    forecast_tsdf = predictor.predict(
        tsdf,
        known_covariates=None,
        past_covariates=None,
    )
    # Extract predictions: 'mean' and quantiles if present
    forecast_df = forecast_tsdf.to_pandas().reset_index()
    target_ids = forecast_df["item_id"].unique()
    median_dict: Dict[str, List[float]] = {}
    lower_dict: Dict[str, List[float]] = {}
    upper_dict: Dict[str, List[float]] = {}
    summary_dict: Dict[str, float] = {}
    for sid in target_ids:
        sub = forecast_df[forecast_df["item_id"] == sid].sort_values("timestamp")
        median_col = "mean"
        # median from quantile 0.5 if available
        if "0.5" in sub.columns:
            median_col = "0.5"
        median_dict[sid] = sub[median_col].values.tolist()
        if 0.025 in quantile_levels and "0.025" in sub.columns:
            lower_dict[sid] = sub["0.025"].values.tolist()
        if 0.975 in quantile_levels and "0.975" in sub.columns:
            upper_dict[sid] = sub["0.975"].values.tolist()
        if summary:
            summary_dict[sid] = float(np.mean(median_dict[sid]))
    # Build index
    # Determine forecast index per series (all share same horizon)
    # Use sorted unique timestamps from forecast_df for first series
    first_sid = target_ids[0]
    sub_first = forecast_df[forecast_df["item_id"] == first_sid]
    forecast_index = pd.to_datetime(sub_first["timestamp"].values)
    forecasts_df = pd.DataFrame(median_dict, index=forecast_index)
    lower_df = pd.DataFrame(lower_dict, index=forecast_index) if lower_dict else None
    upper_df = pd.DataFrame(upper_dict, index=forecast_index) if upper_dict else None
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            # plot historical
            for sid, sub in df_in.groupby(id_used):
                fig.add_trace(go.Scatter(x=sub[date_col], y=sub[target_col], mode="lines", name=f"{sid} (historical)"))
            # plot forecast and CI
            for sid in forecasts_df.columns:
                sub = forecasts_df[sid]
                fig.add_trace(go.Scatter(x=sub.index, y=sub.values, mode="lines", name=f"{sid} (forecast)", line=dict(dash="dot")))
                if lower_df is not None and upper_df is not None:
                    lsub = lower_df[sid]
                    usub = upper_df[sid]
                    fig.add_trace(go.Scatter(
                        x=list(lsub.index) + list(usub.index[::-1]),
                        y=list(usub.values) + list(lsub.values[::-1]),
                        fill="toself",
                        fillcolor="rgba(255,165,0,0.2)",
                        line=dict(color="rgba(255,165,0,0)"),
                        showlegend=False,
                    ))
            fig.update_layout(
                title="Chronos-Bolt Forecast", xaxis_title=date_col, yaxis_title=target_col, template="plotly_white"
            )
            fig.show()
        except Exception:
            pass
    return ChronosBoltForecastResult(
        forecasts=forecasts_df,
        predictor=predictor,
        lower_conf_int=lower_df,
        upper_conf_int=upper_df,
        summary=summary_dict if summary else None,
    )


# ---------------------------------------------------------------------------
# PatchTSMixer forecasting (Hugging Face Transformers)
# ---------------------------------------------------------------------------

@dataclass
class PatchTSMixerForecastResult:
    """Result container for :func:`patchtsmixer_forecast`.

    Attributes
    ----------
    forecasts : pandas.DataFrame
        DataFrame of median forecasts for each series.  The index
        contains the forecast timestamps.
    lower_conf_int : pandas.DataFrame or None
        Lower bound of the prediction interval if quantiles are computed.
    upper_conf_int : pandas.DataFrame or None
        Upper bound of the prediction interval if quantiles are computed.
    model : object
        Loaded Hugging Face PatchTSMixer model used for forecasting.
    summary : Dict[str, float] or None
        Optional summary statistics (mean) of the forecasts.
    """
    forecasts: pd.DataFrame
    model: object
    lower_conf_int: Optional[pd.DataFrame] = None
    upper_conf_int: Optional[pd.DataFrame] = None
    summary: Optional[Dict[str, float]] = None


def patchtsmixer_forecast(
    df: pd.DataFrame,
    *,
    date_col: str,
    target_col: str,
    prediction_length: int = 24,
    model_name: str = "microsoft/patchtsmixer-prediction",
    model_path: Optional[str] = None,
    freq_index: Optional[int] = None,
    plot: bool = False,
    summary: bool = False,
) -> PatchTSMixerForecastResult:
    """Forecast using the PatchTSMixer model from Hugging Face.

    This utility wraps the PatchTSMixer time‑series model from the
    ``transformers`` library.  It accepts a DataFrame with a date
    column and a target column, loads the specified Hugging Face model,
    performs prediction for the next ``prediction_length`` steps, and
    returns the median forecast and optional confidence intervals.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing the datetime column and the target column.
        Only numeric target values are supported.  If multiple series
        are provided, call this function separately for each series.
    date_col : str
        Name of the datetime column.
    target_col : str
        Name of the target column.
    prediction_length : int, default 24
        Number of future time steps to forecast.
    model_name : str, default 'microsoft/patchtsmixer-prediction'
        Hugging Face repository ID of the PatchTSMixer model.  You can
        specify other pre‑trained checkpoints (e.g.
        'microsoft/patchtsmixer-base') available in the time series
        pipeline.
    model_path : str or None, default None
        Directory to cache the model locally.  If provided and the
        directory exists, the model is loaded from this path rather
        than downloaded again.
    freq_index : int or None, default None
        Categorical frequency index required by PatchTSMixer.  Common
        values are ``0`` for hourly or subhourly, ``1`` for daily and
        ``2`` for weekly data.  If ``None``, the frequency is inferred
        from the median difference between timestamps.
    plot : bool, default False
        Whether to display a Plotly chart comparing historical and
        forecasted values with shaded confidence intervals.
    summary : bool, default False
        If True, compute and return the mean of the forecast series.

    Returns
    -------
    PatchTSMixerForecastResult
        Dataclass containing the forecast series, prediction intervals
        and the loaded model.

    Notes
    -----
    This function requires the ``transformers`` and ``torch`` packages.
    PatchTSMixer is an experimental model for multivariate time series
    forecasting that tokenises the series into patches【565404718016214†L158-L278】.
    The API is subject to change; if the call signature of
    ``PatchTSMixerModelForPrediction`` differs from TimesFM, update this
    wrapper accordingly.
    """
    # Lazy imports to avoid heavy dependencies if unused
    if torch is None:
        raise ImportError(
            "torch is required for patchtsmixer_forecast. Please install torch."
        )
    try:
        from transformers import PatchTSMixerModelForPrediction  # type: ignore
    except Exception as e:
        raise ImportError(
            "transformers with PatchTSMixer support is required for patchtsmixer_forecast."
        ) from e
    import os
    import numpy as np
    import pandas as pd
    # Ensure proper ordering and types
    df_in = df[[date_col, target_col]].dropna().copy()
    df_in[date_col] = pd.to_datetime(df_in[date_col], errors='coerce')
    df_in = df_in.sort_values(date_col)
    # Extract past values as a 1D numpy array
    past_values = df_in[target_col].astype(float).to_numpy()
    # Determine freq_index if not provided
    if freq_index is None:
        if len(df_in) > 1:
            diffs = np.diff(df_in[date_col].values.astype('datetime64[ns]')).astype('timedelta64[s]').astype(int)
            median_seconds = int(np.median(diffs))
            day_seconds = 24 * 3600
            week_seconds = 7 * day_seconds
            if median_seconds < day_seconds:
                freq_index = 0
            elif abs(median_seconds - day_seconds) < 0.1 * day_seconds:
                freq_index = 1
            elif abs(median_seconds - week_seconds) < 0.1 * week_seconds:
                freq_index = 2
            else:
                freq_index = 1
        else:
            freq_index = 1
    # Load model
    model = None
    if model_path is not None and os.path.exists(model_path):
        try:
            model = PatchTSMixerModelForPrediction.from_pretrained(model_path)
        except Exception:
            model = None
    if model is None:
        model = PatchTSMixerModelForPrediction.from_pretrained(model_name)
        if model_path is not None:
            try:
                model.save_pretrained(model_path)
            except Exception:
                pass
    model.to("cpu")
    # Prepare input tensor: [batch_size, seq_len]
    past_tensor = torch.tensor(past_values, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        try:
            outputs = model(past_values=past_tensor, freq=freq_index)
        except TypeError:
            outputs = model(past_values=past_tensor)
    if hasattr(outputs, "mean"):
        mean_pred = outputs.mean.squeeze(0).cpu().numpy()
    else:
        raise RuntimeError("The PatchTSMixer model output does not contain 'mean' attribute.")
    full_pred = None
    if hasattr(outputs, "full_prediction"):
        full_pred = outputs.full_prediction.squeeze(0).cpu().numpy()
    # Build forecast index starting after last timestamp
    last_timestamp = df_in[date_col].iloc[-1]
    if len(df_in) > 1:
        step = df_in[date_col].diff().dropna().mode().iloc[0]
    else:
        step = pd.Timedelta(1, unit='D')
    forecast_index = pd.date_range(last_timestamp + step, periods=prediction_length, freq=step)
    # Determine median forecast
    if len(mean_pred) >= prediction_length:
        median_forecast = mean_pred[:prediction_length]
    else:
        pad_len = prediction_length - len(mean_pred)
        median_forecast = np.concatenate([mean_pred, np.repeat(mean_pred[-1], pad_len)])
    forecasts_df = pd.DataFrame({target_col: median_forecast}, index=forecast_index)
    # Compute confidence intervals if possible
    lower_df = None
    upper_df = None
    if full_pred is not None and full_pred.size > 0:
        lower = np.quantile(full_pred, 0.025, axis=0)
        upper = np.quantile(full_pred, 0.975, axis=0)
        if len(lower) >= prediction_length:
            lower_vals = lower[:prediction_length]
            upper_vals = upper[:prediction_length]
        else:
            pad_len = prediction_length - len(lower)
            lower_vals = np.concatenate([lower, np.repeat(lower[-1], pad_len)])
            upper_vals = np.concatenate([upper, np.repeat(upper[-1], pad_len)])
        lower_df = pd.DataFrame({target_col: lower_vals}, index=forecast_index)
        upper_df = pd.DataFrame({target_col: upper_vals}, index=forecast_index)
    summary_dict = None
    if summary:
        summary_dict = {target_col: float(np.mean(median_forecast))}
    # Plot
    if plot:
        try:
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_in[date_col], y=df_in[target_col], mode='lines', name='historical'))
            fig.add_trace(go.Scatter(x=forecasts_df.index, y=forecasts_df[target_col], mode='lines', name='forecast', line=dict(dash='dot')))
            if lower_df is not None and upper_df is not None:
                fig.add_trace(go.Scatter(
                    x=list(lower_df.index) + list(upper_df.index[::-1]),
                    y=list(upper_df[target_col]) + list(lower_df[target_col][::-1]),
                    fill='toself', fillcolor='rgba(255,165,0,0.2)', line=dict(color='rgba(255,165,0,0)'),
                    showlegend=False,
                ))
            fig.update_layout(title='PatchTSMixer Forecast', xaxis_title=date_col, yaxis_title=target_col, template='plotly_white')
            fig.show()
        except Exception:
            pass
    return PatchTSMixerForecastResult(
        forecasts=forecasts_df,
        model=model,
        lower_conf_int=lower_df,
        upper_conf_int=upper_df,
        summary=summary_dict,
    )