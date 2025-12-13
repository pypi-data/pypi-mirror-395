def all():
    print( """This is all the content from the module.

Lab - 01

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error

train_size = int(len(data) * 0.8)
train, test = data[:train_size], data[train_size:]

# i. Different forecasting techniques

# Simple Exponential Smoothing (SES)
ses_model = SimpleExpSmoothing(train).fit()
ses_pred = ses_model.forecast(len(test))

# Simple Moving Average (SMA)
window = 3
sma_pred = train.rolling(window=window).mean().iloc[-1]
sma_forecast = pd.Series([sma_pred] * len(test), index=test.index)

# Holt-Winters Smoothing
hw_model = ExponentialSmoothing(train, seasonal='add', seasonal_periods=12).fit()
hw_pred = hw_model.forecast(len(test))

# ii. Calculate evaluation metrics
def calc_metrics(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    mse = mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse)
    return {'MAE': mae, 'MSE': mse, 'RMSE': rmse}

print("SES Metrics:", calc_metrics(test, ses_pred))
print("SMA Metrics:", calc_metrics(test, sma_forecast))
print("HW Metrics:", calc_metrics(test, hw_pred))

# iii. Identify trends and seasonal patterns
plt.plot(train.index, train, label='Train')
plt.plot(test.index, test, label='Actual', marker='o')
plt.plot(test.index, ses_pred, label='SES', marker='x')
plt.plot(test.index, hw_pred, label='Holt-Winters', marker='s')
plt.legend()
plt.show()
----------------------------------------------------------------------


          
Lab - 02

          

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss

# i. Generate white noise
white_noise = np.random.normal(0, 1, len(data))

# ii. Compare graphs
fig, axes = plt.subplots(2, 1, figsize=(12, 6))
axes[0].plot(white_noise)
axes[0].set_title('White Noise')
axes[1].plot(data)
axes[1].set_title('Time Series Data')
plt.show()

# iii. Statistical tests for stationarity
# Augmented Dickey-Fuller Test
adf_result = adfuller(data)
print(f"ADF Statistic: {adf_result[0]}")
print(f"p-value: {adf_result[1]}")
print(f"Stationary: {adf_result[1] < 0.05}")

# KPSS Test
kpss_result = kpss(data)
print(f"\nKPSS Statistic: {kpss_result[0]}")
print(f"p-value: {kpss_result[1]}")
----------------------------------------------------------------------



Lab - 3

import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# i. Detect trends using moving averages
ma_trend = data.rolling(window=12).mean()
plt.plot(data, label='Original')
plt.plot(ma_trend, label='Trend (MA-12)', linewidth=2)
plt.show()

# ii. Plot ACF and PACF
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
plot_acf(data.dropna(), lags=40, ax=axes[0])
plot_pacf(data.dropna(), lags=40, ax=axes[1])
plt.show()
----------------------------------------------------------------------



Lab - 4

          
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AutoReg

# i. Examine ACF and PACF (already plotted above)
# PACF cuts off at lag p → AR(p) model

# ii. Fit AR(1) model
ar1_model = AutoReg(train, lags=1).fit()
ar1_pred = ar1_model.predict(start=len(train), end=len(train)+len(test)-1)
print(f"AR(1) AIC: {ar1_model.aic}")

# iii. Fit higher lag AR models
ar3_model = AutoReg(train, lags=3).fit()
ar3_pred = ar3_model.predict(start=len(train), end=len(train)+len(test)-1)
print(f"AR(3) AIC: {ar3_model.aic}")

plt.plot(test.values, label='Actual')
plt.plot(ar1_pred, label='AR(1)')
plt.plot(ar3_pred, label='AR(3)')
plt.legend()
plt.title('AR Model Comparison')
plt.show()
----------------------------------------------------------------------


          
Lab - 5

import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# i. Plot ACF and PACF (already done in Lab 6)

# ii. Fit MA(1) model
ma1_model = ARIMA(train, order=(0, 0, 1)).fit()
ma1_pred = ma1_model.forecast(steps=len(test))
print(f"MA(1) AIC: {ma1_model.aic}")

# iii. Fit higher lag MA model
ma3_model = ARIMA(train, order=(0, 0, 3)).fit()
ma3_pred = ma3_model.forecast(steps=len(test))
print(f"MA(3) AIC: {ma3_model.aic}")

# iv. Compare performances
print("MA(1) Metrics:", calc_metrics(test, ma1_pred))
print("MA(3) Metrics:", calc_metrics(test, ma3_pred))

plt.figure(figsize=(12, 4))
plt.plot(test.values, label='Actual')
plt.plot(ma1_pred.values, label='MA(1)')
plt.plot(ma3_pred.values, label='MA(3)')
plt.legend()
plt.title('MA Model Comparison')
plt.show()
----------------------------------------------------------------------


          
Lab - 6
          

import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# i. Initialize ARMA model
arma_model = ARIMA(train, order=(1, 0, 1))

# ii. Train the model
arma_fit = arma_model.fit()
print(f"ARMA(1,1) Summary:\n{arma_fit.summary()}")

# iii. Generate forecasts
arma_pred = arma_fit.forecast(steps=len(test))
print("ARMA Metrics:", calc_metrics(test, arma_pred))

plt.plot(test.values, label='Actual')
plt.plot(arma_pred.values, label='ARMA(1,1)')
plt.legend()
plt.title('ARMA Model Forecast')
plt.show()
----------------------------------------------------------------------


          

Lab - 07        

          
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# i. Initialize ARIMA model with p, d, q parameters
# p=1 (AR terms), d=1 (differencing), q=1 (MA terms)
arima_model = ARIMA(train, order=(1, 1, 1))

# ii. Train the model
arima_fit = arima_model.fit()
print(f"ARIMA(1,1,1) Summary:\n{arima_fit.summary()}")

# iii. Generate forecasts
arima_pred = arima_fit.forecast(steps=len(test))
print("ARIMA Metrics:", calc_metrics(test, arima_pred))

plt.plot(test.values, label='Actual')
plt.plot(arima_pred.values, label='ARIMA(1,1,1)')
plt.legend()
plt.title('ARIMA Model Forecast')
plt.show()
----------------------------------------------------------------------
    """)

def alln():
    print( """This is all the content from the module.

Lab - 01
          
data=pd.read_csv('/content/yahoo_stock - yahoo_stock.csv')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


ts_data=data.iloc[:,[0,3]]
summary_stats=ts_data['Open'].describe()

ts_data["Date"]=pd.to_datetime(ts_data['Date'], format="%Y-%m-%d")
ts_data.set_index('Date',inplace=True)

plt.plot(ts_data.index,ts_data["Open"])
plt.ylabel('Price')
plt.xlabel('Date')
plt.title("Opening Price of Stocks")
plt.xticks(rotation=90)
plt.xlim(ts_data.index.min(),ts_data.index.max())
plt.show()

from statsmodels.tsa.seasonal import seasonal_decompose
Decompose=seasonal_decompose(ts_data["Open"],model='multiplicative',period=340)
Decompose.plot()
plt.show()	
----------------------------------------------------------------------

  
Lab - 02

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error

# --- Load & prepare data ---
data = pd.read_csv('airline-passengers.csv')     # make sure file path is correct
data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['Month'])
data.set_index('Month', inplace=True)
data = data.asfreq('MS')   # monthly start frequency (fills missing index if any)

# --- Train/Test split ---
train_size = int(len(data) * 0.8)
train = data.iloc[:train_size]['Passengers']
test = data.iloc[train_size:]['Passengers']

def print_split_info():
    print(f"Total points: {len(data)}  Train: {len(train)}  Test: {len(test)}")
print_split_info()

# --------------------------
# 1) Simple Moving Average
# --------------------------
window = 12

# Use last rolling mean from train as a simple forecast (common and simple approach)
last_sma = train.rolling(window=window).mean().iloc[-1]
sma_forecast = pd.Series([last_sma] * len(test), index=test.index)

# --------------------------
# 2) Simple Exponential Smoothing (manual)
# --------------------------
def simple_exponential_smoothing_series(series, alpha):
    ses = [series.iloc[0]]
    for i in range(1, len(series)):
        ses.append(alpha * series.iloc[i] + (1 - alpha) * ses[i-1])
    return pd.Series(ses, index=series.index)

alpha = 0.2
ses_train_series = simple_exponential_smoothing_series(train, alpha)
# For forecasting horizon, use last smoothed value repeated (basic approach)
last_ses = ses_train_series.iloc[-1]
ses_forecast = pd.Series([last_ses] * len(test), index=test.index)

# --------------------------
# 3) Holt-Winters (statsmodels)
# --------------------------
hw_model = ExponentialSmoothing(train, seasonal='add', seasonal_periods=12, trend='add').fit()
hw_forecast = hw_model.forecast(len(test))
hw_forecast = pd.Series(hw_forecast, index=test.index)

# --------------------------
# Evaluation function
# --------------------------
def calc_metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    return mae, mse, rmse

print("\n--- Evaluation (Test set) ---")
for name, pred in [('SMA', sma_forecast), ('SES', ses_forecast), ('Holt-Winters', hw_forecast)]:
    mae, mse, rmse = calc_metrics(test, pred)
    print(f"{name}: MAE={mae:.3f}, MSE={mse:.3f}, RMSE={rmse:.3f}")

# --------------------------
# Plots
# --------------------------
plt.figure(figsize=(12,5))
plt.plot(train.index, train, label='Train')
plt.plot(test.index, test, marker='o', label='Test (actual)')
plt.plot(test.index, sma_forecast, label=f'SMA (w={window}) forecast', linestyle='--')
plt.plot(test.index, ses_forecast, label=f'SES (alpha={alpha}) forecast', linestyle='--')
plt.plot(test.index, hw_forecast, label='Holt-Winters forecast', linestyle='--')
plt.title('Forecasts vs Actuals')
plt.xlabel('Date')
plt.ylabel('Passengers')
plt.legend()
plt.tight_layout()
plt.show()

----------------------------------------------------------------------



Lab - 3 (ADF AND KPSS)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
df=sm.datasets.sunspots.load_pandas().data

df["Year"]=pd.Index(sm.tsa.datetools.dates_from_range('1700','2008'))
np.random.seed(0)
n_samples = 1000
white_noise = np.random.randn(n_samples)
plt.figure(figsize=(10, 4))
plt.plot(white_noise)
plt.title('White Noise')
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

plt.figure(figsize=(10, 4))
plt.plot(df['Year'], df['SUNACTIVITY'], label='Sunspots Data')
plt.title('Sunspots Data')
plt.xlabel('Year')
plt.ylabel('Sunspot Activity')
plt.legend()
plt.show()

adf_result = sm.tsa.adfuller(df['SUNACTIVITY'])
print('ADF Statistic:', adf_result[0])
print('p-value:', adf_result[1])
print('Critical Values:', adf_result[4])

kpss_result = sm.tsa.kpss(df['SUNACTIVITY'])
print('\nKPSS Statistic:', kpss_result[0])
print('p-value:', kpss_result[1])
print('Critical Values:', kpss_result[3])
----------------------------------------------------------------------


Lab - 4 ( AR )

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.ar_model import AutoReg
import warnings
warnings.filterwarnings("ignore")
data = pd.read_csv('/content/airline-passengers - airline-passengers (1).csv')
data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['Month'])
data.set_index('Month', inplace=True)
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plot_acf(data, lags=30, ax=plt.gca(), title='Autocorrelation Function (ACF)')
plt.subplot(2, 1, 2)
plot_pacf(data, lags=30, ax=plt.gca(), title='Partial Autocorrelation Function (PACF)')
plt.tight_layout()
plt.show()
ar_model_1 = AutoReg(data, lags=1)
ar_model_fit_1 = ar_model_1.fit()
print(ar_model_fit_1.summary())
lag_value = 5
ar_model_lag = AutoReg(data, lags=lag_value)
ar_model_fit_lag = ar_model_lag.fit()
print(ar_model_fit_lag.summary())
ar_coeffs = ar_model_fit_lag.params
print("AR Coefficients:")
print(ar_coeffs)
print("\nAR Equation:")
equation = f"y(t) = {ar_coeffs[0]:.4f}"
for i in range(1, len(ar_coeffs)):
equation += f" + {ar_coeffs[i]:.4f}*y(t-{i})"
print(equation)
----------------------------------------------------------------------


Lab - 5 ( MA )
          
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")
data = pd.read_csv('/content/airline-passengers - airline-passengers (1).csv')
data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['Month'])
data.set_index('Month', inplace=True)
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plot_acf(data, lags=30, ax=plt.gca(), title='Autocorrelation Function (ACF)')
plt.subplot(2, 1, 2)
plot_pacf(data, lags=30, ax=plt.gca(), title='Partial Autocorrelation Function (PACF)')
plt.tight_layout()
plt.show()
ma_model_1 = ARIMA(data, order=(0, 0, 1))
ma_model_fit_1 = ma_model_1.fit()
print(ma_model_fit_1.summary())
lag_value = 5
ma_model_lag = ARIMA(data, order=(0, 0, lag_value))
ma_model_fit_lag = ma_model_lag.fit()
print(ma_model_fit_lag.summary())
ma_coeffs = ma_model_fit_lag.params
print("MA Coefficients:")
print(ma_coeffs)
print("\nMA Equation:")
equation = f"y(t) = {ma_coeffs[0]:.4f}"
for i in range(1, len(ma_coeffs)):
equation += f" + {ma_coeffs[i]:.4f}*ε(t-{i})"
print(equation)
          
----------------------------------------------------------------------

       
Lab - 6 (ARMA)
          
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")
# Load data
data = pd.read_csv('/content/airline-passengers - airline-passengers (1).csv')
data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['Month'])
data.set_index('Month', inplace=True)
# Plot ACF and PACF
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plot_acf(data, lags=30, ax=plt.gca(), title='Autocorrelation Function (ACF)')
plt.subplot(2, 1, 2)
plot_pacf(data, lags=30, ax=plt.gca(), title='Partial Autocorrelation Function (PACF)')
plt.tight_layout()
plt.show()
# Fit ARMA(1,1) model
arma_model_1_1 = ARIMA(data, order=(1, 0, 1))
arma_model_fit_1_1 = arma_model_1_1.fit()
print(arma_model_fit_1_1.summary())
# Fit higher lag ARMA models
lag_value = 5
arma_model_higher_lag = ARIMA(data, order=(lag_value, 0, lag_value))
arma_model_fit_higher_lag = arma_model_higher_lag.fit()
print(arma_model_fit_higher_lag.summary())
arma_coeffs = arma_model_fit_higher_lag.params
print("ARMA Coefficients:")
print(arma_coeffs)
# ARMA Equation
equation = f"y(t) = {arma_coeffs[0]:.4f}"
for i in range(1, len(arma_coeffs)):
equation += f" + {arma_coeffs[i]:.4f}*y(t-{i})"
print("ARMA Equation:")
print(equation)
----------------------------------------------------------------------


Lab - 07   ( arima )

          
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import warnings
# Suppress warnings
warnings.filterwarnings("ignore")
# Load and preprocess the data (replace 'airline-passengers.csv' with your dataset)
data = pd.read_csv('/content/airline-passengers - airline-passengers (1).csv')
data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['Month'])
data.set_index('Month', inplace=True)
# Plot ACF and PACF plots for ARIMA(1,1)
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plot_acf(data, lags=30, ax=plt.gca(), title='Autocorrelation Function (ACF) - ARIMA(1,1)')
plt.subplot(2, 1, 2)
plot_pacf(data, lags=30, ax=plt.gca(), title='Partial Autocorrelation Function (PACF) - ARIMA(1,1)')
plt.tight_layout()
plt.show()
# Fit ARIMA(1,1) model
arima11_model = ARIMA(data, order=(1, 1, 0))
arima11_model_fit = arima11_model.fit()
# Print model summary for ARIMA(1,1)
print(arima11_model_fit.summary())
# Get ARIMA(1,1) model coefficients
arima11_coefficients = arima11_model_fit.params
# Print ARIMA(1,1) model equation
print("\nARIMA(1,1) Model Equation:")
print("Y(t) = ", end="")
for i in range(len(arima11_coefficients)):
if i == 0:
print(f"{arima11_coefficients[i]:.4f}", end="")
else:
print(f" + {arima11_coefficients[i]:.4f} * ΔY(t-{i}) ", end="")
print()
# Plot ACF and PACF plots for ARIMA(2)
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plot_acf(data, lags=30, ax=plt.gca(), title='Autocorrelation Function (ACF) - ARIMA(2)')
plt.subplot(2, 1, 2)
plot_pacf(data, lags=30, ax=plt.gca(), title='Partial Autocorrelation Function (PACF) - ARIMA(2)')
plt.tight_layout()
plt.show()
# Fit ARIMA(2) model
arima2_model = ARIMA(data, order=(2, 0, 0))
arima2_model_fit = arima2_model.fit()
# Print model summary for ARIMA(2)
print(arima2_model_fit.summary())
# Get ARIMA(2) model coefficients
arima2_coefficients = arima2_model_fit.params
# Print ARIMA(2) model equation
print("\nARIMA(2) Model Equation:")
print("Y(t) = ", end="")
for i in range(len(arima2_coefficients)):
if i == 0:
print(f"{arima2_coefficients[i]:.4f}", end="")
else:
print(f" + {arima2_coefficients[i]:.4f} * Y(t-{i}) ", end="")
print()
----------------------------------------------------------------------
          
ACF AND PACF 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings
warnings.filterwarnings("ignore")
# Load data
data = pd.read_csv('/content/airline-passengers - airline-passengers (1).csv')
data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['Month'])
data.set_index('Month', inplace=True)
# Plot ACF and PACF
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plot_acf(data, lags=30, ax=plt.gca(), title='Autocorrelation Function (ACF)')
plt.subplot(2, 1, 2)
plot_pacf(data, lags=30, ax=plt.gca(), title='Partial Autocorrelation Function (PACF)')
plt.tight_layout()
plt.show()
    """)


def alls():
    print( """This is all the content from the module.

# Lab - 01
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

data = pd.read_csv('/content/yahoo_stock - yahoo_stock.csv')

ts_data = data.iloc[:, [0, 3]]
summary_stats = ts_data['Open'].describe()

ts_data["Date"] = pd.to_datetime(ts_data['Date'], format="%Y-%m-%d")
ts_data.set_index('Date', inplace=True)

plt.plot(ts_data.index, ts_data["Open"])
plt.ylabel('Price')
plt.xlabel('Date')
plt.title("Opening Price of Stocks")
plt.xticks(rotation=90)
plt.xlim(ts_data.index.min(), ts_data.index.max())
plt.show()

Decompose = seasonal_decompose(ts_data["Open"], model='multiplicative', period=340)
Decompose.plot()
plt.show()


# ----------------------------------------------------------------------
# Lab - 02
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error

# --- Load & prepare data ---
data = pd.read_csv('airline-passengers.csv')     # make sure file path is correct
data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['Month'])
data.set_index('Month', inplace=True)
data = data.asfreq('MS')   # monthly start frequency (fills missing index if any)

# --- Train/Test split ---
train_size = int(len(data) * 0.8)
train = data.iloc[:train_size]['Passengers']
test = data.iloc[train_size:]['Passengers']

def print_split_info():
    print(f"Total points: {len(data)}  Train: {len(train)}  Test: {len(test)}")
print_split_info()

# --------------------------
# 1) Simple Moving Average
# --------------------------
window = 12

# Use last rolling mean from train as a simple forecast (common and simple approach)
last_sma = train.rolling(window=window).mean().iloc[-1]
sma_forecast = pd.Series([last_sma] * len(test), index=test.index)

# --------------------------
# 2) Simple Exponential Smoothing (manual)
# --------------------------
def simple_exponential_smoothing_series(series, alpha):
    ses = [series.iloc[0]]
    for i in range(1, len(series)):
        ses.append(alpha * series.iloc[i] + (1 - alpha) * ses[i - 1])
    return pd.Series(ses, index=series.index)

alpha = 0.2
ses_train_series = simple_exponential_smoothing_series(train, alpha)
# For forecasting horizon, use last smoothed value repeated (basic approach)
last_ses = ses_train_series.iloc[-1]
ses_forecast = pd.Series([last_ses] * len(test), index=test.index)

# --------------------------
# 3) Holt-Winters (statsmodels)
# --------------------------
hw_model = ExponentialSmoothing(train, seasonal='add', seasonal_periods=12, trend='add').fit()
hw_forecast = hw_model.forecast(len(test))
hw_forecast = pd.Series(hw_forecast, index=test.index)

# --------------------------
# Evaluation function
# --------------------------
def calc_metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    return mae, mse, rmse

print("\n--- Evaluation (Test set) ---")
for name, pred in [('SMA', sma_forecast), ('SES', ses_forecast), ('Holt-Winters', hw_forecast)]:
    mae, mse, rmse = calc_metrics(test, pred)
    print(f"{name}: MAE={mae:.3f}, MSE={mse:.3f}, RMSE={rmse:.3f}")

# --------------------------
# Plots
# --------------------------
plt.figure(figsize=(12, 5))
plt.plot(train.index, train, label='Train')
plt.plot(test.index, test, marker='o', label='Test (actual)')
plt.plot(test.index, sma_forecast, label=f'SMA (w={window}) forecast', linestyle='--')
plt.plot(test.index, ses_forecast, label=f'SES (alpha={alpha}) forecast', linestyle='--')
plt.plot(test.index, hw_forecast, label='Holt-Winters forecast', linestyle='--')
plt.title('Forecasts vs Actuals')
plt.xlabel('Date')
plt.ylabel('Passengers')
plt.legend()
plt.tight_layout()
plt.show()


# ----------------------------------------------------------------------
# Lab - 3 (ADF AND KPSS)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss

# Load sunspots dataset
ds = sm.datasets.sunspots.load_pandas()
df = ds.data.copy()

# Ensure Year column exists and convert to datetime index
if 'YEAR' in df.columns:
    df.rename(columns={'YEAR': 'Year'}, inplace=True)
elif 'year' in df.columns:
    df.rename(columns={'year': 'Year'}, inplace=True)

if 'Year' not in df.columns:
    df['Year'] = np.arange(1700, 1700 + len(df))

df['Date'] = pd.to_datetime(df['Year'].astype(int), format='%Y')
df.set_index('Date', inplace=True)

# White noise plot (length same as dataset)
np.random.seed(0)
n_samples = len(df)
white_noise = np.random.randn(n_samples)

plt.figure(figsize=(10, 4))
plt.plot(white_noise)
plt.title('White Noise (length = dataset)')
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

# Sunspots plot
plt.figure(figsize=(10, 4))
plt.plot(df.index.year, df['SUNACTIVITY'], label='Sunspots Data')
plt.title('Sunspots Data')
plt.xlabel('Year')
plt.ylabel('Sunspot Activity')
plt.legend()
plt.show()

# ADF test
adf_result = adfuller(df['SUNACTIVITY'].dropna(), autolag='AIC')
print('ADF Statistic:', adf_result[0])
print('p-value:', adf_result[1])
print('Critical Values:', adf_result[4])

# KPSS test
kpss_stat, kpss_p, kpss_lags, kpss_crit = kpss(df['SUNACTIVITY'].dropna(), regression='c', nlags='auto')
print('\nKPSS Statistic:', kpss_stat)
print('p-value:', kpss_p)
print('Critical Values:', kpss_crit)


# ----------------------------------------------------------------------
# Lab - 4 ( AR )
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.ar_model import AutoReg
import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv('/content/airline-passengers - airline-passengers (1).csv')
data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['Month'])
data.set_index('Month', inplace=True)

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plot_acf(data, lags=30, ax=plt.gca(), title='Autocorrelation Function (ACF)')
plt.subplot(2, 1, 2)
plot_pacf(data, lags=30, ax=plt.gca(), title='Partial Autocorrelation Function (PACF)')
plt.tight_layout()
plt.show()

ar_model_1 = AutoReg(data, lags=1)
ar_model_fit_1 = ar_model_1.fit()
print(ar_model_fit_1.summary())

lag_value = 5
ar_model_lag = AutoReg(data, lags=lag_value)
ar_model_fit_lag = ar_model_lag.fit()
print(ar_model_fit_lag.summary())

ar_coeffs = ar_model_fit_lag.params
print("AR Coefficients:")
print(ar_coeffs)
print("\nAR Equation:")
equation = f"y(t) = {ar_coeffs[0]:.4f}"
for i in range(1, len(ar_coeffs)):
    equation += f" + {ar_coeffs[i]:.4f}*y(t-{i})"
print(equation)


# ----------------------------------------------------------------------
# Lab - 5 ( MA )
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv('/content/airline-passengers - airline-passengers (1).csv')
data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['Month'])
data.set_index('Month', inplace=True)

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plot_acf(data, lags=30, ax=plt.gca(), title='Autocorrelation Function (ACF)')
plt.subplot(2, 1, 2)
plot_pacf(data, lags=30, ax=plt.gca(), title='Partial Autocorrelation Function (PACF)')
plt.tight_layout()
plt.show()

ma_model_1 = ARIMA(data, order=(0, 0, 1))
ma_model_fit_1 = ma_model_1.fit()
print(ma_model_fit_1.summary())

lag_value = 5
ma_model_lag = ARIMA(data, order=(0, 0, lag_value))
ma_model_fit_lag = ma_model_lag.fit()
print(ma_model_fit_lag.summary())

ma_coeffs = ma_model_fit_lag.params
print("MA Coefficients:")
print(ma_coeffs)
print("\nMA Equation:")
equation = f"y(t) = {ma_coeffs[0]:.4f}"
for i in range(1, len(ma_coeffs)):
    equation += f" + {ma_coeffs[i]:.4f}*ε(t-{i})"
print(equation)


# ----------------------------------------------------------------------
# Lab - 6 (ARMA)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")

# Load data
data = pd.read_csv('/content/airline-passengers - airline-passengers (1).csv')
data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['Month'])
data.set_index('Month', inplace=True)

# Plot ACF and PACF
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plot_acf(data, lags=30, ax=plt.gca(), title='Autocorrelation Function (ACF)')
plt.subplot(2, 1, 2)
plot_pacf(data, lags=30, ax=plt.gca(), title='Partial Autocorrelation Function (PACF)')
plt.tight_layout()
plt.show()

# Fit ARMA(1,1) model
arma_model_1_1 = ARIMA(data, order=(1, 0, 1))
arma_model_fit_1_1 = arma_model_1_1.fit()
print(arma_model_fit_1_1.summary())

# Fit higher lag ARMA models
lag_value = 5
arma_model_higher_lag = ARIMA(data, order=(lag_value, 0, lag_value))
arma_model_fit_higher_lag = arma_model_higher_lag.fit()
print(arma_model_fit_higher_lag.summary())

arma_coeffs = arma_model_fit_higher_lag.params
print("ARMA Coefficients:")
print(arma_coeffs)

# ARMA Equation
equation = f"y(t) = {arma_coeffs[0]:.4f}"
for i in range(1, len(arma_coeffs)):
    equation += f" + {arma_coeffs[i]:.4f}*y(t-{i})"
print("ARMA Equation:")
print(equation)


# ----------------------------------------------------------------------
# Lab - 07   ( arima )
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import warnings
# Suppress warnings
warnings.filterwarnings("ignore")

# Load and preprocess the data (replace 'airline-passengers.csv' with your dataset)
data = pd.read_csv('/content/airline-passengers - airline-passengers (1).csv')
data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['Month'])
data.set_index('Month', inplace=True)

# Plot ACF and PACF plots for ARIMA(1,1)
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plot_acf(data, lags=30, ax=plt.gca(), title='Autocorrelation Function (ACF) - ARIMA(1,1)')
plt.subplot(2, 1, 2)
plot_pacf(data, lags=30, ax=plt.gca(), title='Partial Autocorrelation Function (PACF) - ARIMA(1,1)')
plt.tight_layout()
plt.show()

# Fit ARIMA(1,1) model
arima11_model = ARIMA(data, order=(1, 1, 0))
arima11_model_fit = arima11_model.fit()

# Print model summary for ARIMA(1,1)
print(arima11_model_fit.summary())

# Get ARIMA(1,1) model coefficients
arima11_coefficients = arima11_model_fit.params

# Print ARIMA(1,1) model equation
print("\nARIMA(1,1) Model Equation:")
print("Y(t) = ", end="")
for i in range(len(arima11_coefficients)):
    if i == 0:
        print(f"{arima11_coefficients[i]:.4f}", end="")
    else:
        print(f" + {arima11_coefficients[i]:.4f} * ΔY(t-{i}) ", end="")
print()

# Plot ACF and PACF plots for ARIMA(2)
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plot_acf(data, lags=30, ax=plt.gca(), title='Autocorrelation Function (ACF) - ARIMA(2)')
plt.subplot(2, 1, 2)
plot_pacf(data, lags=30, ax=plt.gca(), title='Partial Autocorrelation Function (PACF) - ARIMA(2)')
plt.tight_layout()
plt.show()

# Fit ARIMA(2) model
arima2_model = ARIMA(data, order=(2, 0, 0))
arima2_model_fit = arima2_model.fit()

# Print model summary for ARIMA(2)
print(arima2_model_fit.summary())

# Get ARIMA(2) model coefficients
arima2_coefficients = arima2_model_fit.params

# Print ARIMA(2) model equation
print("\nARIMA(2) Model Equation:")
print("Y(t) = ", end="")
for i in range(len(arima2_coefficients)):
    if i == 0:
        print(f"{arima2_coefficients[i]:.4f}", end="")
    else:
        print(f" + {arima2_coefficients[i]:.4f} * Y(t-{i}) ", end="")
print()


# ----------------------------------------------------------------------
# ACF AND PACF
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings
warnings.filterwarnings("ignore")

# Load data
data = pd.read_csv('/content/airline-passengers - airline-passengers (1).csv')
data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['Month'])
data.set_index('Month', inplace=True)

# Plot ACF and PACF
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plot_acf(data, lags=30, ax=plt.gca(), title='Autocorrelation Function (ACF)')
plt.subplot(2, 1, 2)
plot_pacf(data, lags=30, ax=plt.gca(), title='Partial Autocorrelation Function (PACF)')
plt.tight_layout()
plt.show()
    """)
#kdjfklasdjfkl;asdjf;laskdfjasl;kfjasl;kkfjas;lkfjsa;lfkjasdl;fasd
#l;fkjsd;lfjsdd;fklkasj;flasjf;lkaskjf;lkjf;slkjfas;slkfjasd;lfjas;lkkfjas;lk
def modelsum():
    print( """This is all the content from the module.

                  
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error,mean_absolute_error
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import warnings

warnings.filterwarnings('ignore')

data = pd.read_csv('AirPassengers.csv')
data['date'] = pd.to_datetime(data['date'])
data.set_index('date',inplace=True)

tl = int(len(data)*.8)
train,test = data[:tl],data[tl:]

# # plt.figuresize(10,6
plt.subplot(2,1,1)
plot_acf(data['value'],lags = 30,ax=plt.gca())
plt.subplot(2,1,2)
plot_pacf(data['value'],lags = 30,ax=plt.gca())
plt.tight_layout()
plt.show()

def cal_met(a,p):
    mse = mean_squared_error(a,p)
    mae = mean_absolute_error(a,p)
    rmse = mse**(1/2)
    return {'mse':mse,'mae':mae,'rmse':rmse}

a_m = ARIMA(train,order=(1,1,1))
a_m_f = a_m.fit()
print(a_m_f.summary())
a_m_c = a_m_f.params
a_m_f_f = a_m_f.forecast(len(test))

print('\n\n\n')
print(a_m_c)

print(cal_met(test['value'],a_m_f_f))
        
plt.subplot(2,1,1)
plt.plot(train['value'],label='Actual')
plt.plot(test['value'],label='Actual')
plt.plot(a_m_f_f,label="forecast")
plt.tight_layout()
plt.show()









































# ===========================================================
# LAB 3 — SUNSPOTS, WHITE NOISE, ADF, KPSS (Week 5 & 6)
# ===========================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings
warnings.filterwarnings("ignore")

# Load Sunspots dataset
df = sm.datasets.sunspots.load_pandas().data
df["Year"] = pd.Index(sm.tsa.datetools.dates_from_range('1700', '2008'))
# -----------------------------------------------------------
# 1. Generate White Noise
# -----------------------------------------------------------
np.random.seed(0)
white_noise = np.random.randn(1000)

plt.figure(figsize=(10, 4))
plt.plot(white_noise)
plt.title("White Noise")
plt.show()
# -----------------------------------------------------------
# 2. Plot Time Series (Sunspots)
# -----------------------------------------------------------
plt.figure(figsize=(10, 4))
plt.plot(df["Year"], df["SUNACTIVITY"])
plt.title("Sunspots Data")
plt.show()
# -----------------------------------------------------------
# 3. Stationarity Tests (ADF & KPSS)
# -----------------------------------------------------------
adf_result = sm.tsa.adfuller(df["SUNACTIVITY"])
print("ADF Statistic:", adf_result[0])
print("ADF p-value:", adf_result[1])

kpss_result = sm.tsa.kpss(df["SUNACTIVITY"])
print("KPSS Statistic:", kpss_result[0])
print("KPSS p-value:", kpss_result[1])
# -----------------------------------------------------------
# 4. Trend Detection using Simple Moving Average (SMA)
# -----------------------------------------------------------
df["SMA_20"] = df["SUNACTIVITY"].rolling(window=20).mean()

plt.figure(figsize=(10, 6))
plt.plot(df["Year"], df["SUNACTIVITY"], label="Original Data")
plt.plot(df["Year"], df["SMA_20"], label="Trend (20-Year SMA)")
plt.title("Trend Detection in Sunspots Data")
plt.legend()
plt.show()
# -----------------------------------------------------------
# 5. ACF & PACF Plots
# -----------------------------------------------------------
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plot_acf(df["SUNACTIVITY"], lags=40, ax=plt.gca(), title="Autocorrelation (Sunspots)")

plt.subplot(2, 1, 2)
plot_pacf(df["SUNACTIVITY"], lags=40, ax=plt.gca(), title="Partial Autocorrelation (Sunspots)")

plt.tight_layout()
plt.show()





































# ===========================================================
# LAB 2 — MOVING AVERAGE, SES, HOLT-WINTERS (Week 4)
# ===========================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

data = pd.read_csv("AirPassengers.csv")
data['Passengers'] = data["value"]
# data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['date'])
data.set_index('Month', inplace=True)

# --- 1. Simple Moving Average (SMA) ---
def simple_moving_average(series, window_size):
    sma_values = []
    for i in range(len(series) - window_size + 1):
        window = series[i:i + window_size]
        sma_values.append(np.mean(window))
    return sma_values

window_size = 12
sma_values = simple_moving_average(data['Passengers'], window_size)

plt.figure(figsize=(10, 6))
plt.plot(data.index, data['Passengers'], label='Original Data')
plt.plot(data.index[window_size - 1:], sma_values, label='SMA')
plt.title("Simple Moving Average")
plt.legend()
plt.show()

# Evaluation for SMA
train_size = int(len(data) * 0.8)
train_data, test_data = data.iloc[:train_size], data.iloc[train_size:]

sma_forecast_full = simple_moving_average(pd.concat([train_data, test_data])['Passengers'], window_size)
sma_forecast_test = sma_forecast_full[len(train_data) - (window_size - 1):len(train_data) - (window_size - 1) + len(test_data)]

print("--- SMA Metrics ---")
print("SMA MAE:", mean_absolute_error(test_data['Passengers'], sma_forecast_test))
print("SMA MSE:", mean_squared_error(test_data['Passengers'], sma_forecast_test)) # Added MSE
print("SMA RMSE:", np.sqrt(mean_squared_error(test_data['Passengers'], sma_forecast_test)))

plt.figure(figsize=(10, 6))
plt.plot(train_data.index, train_data['Passengers'], label='Train')
plt.plot(test_data.index, test_data['Passengers'], label='Test')
plt.plot(test_data.index, sma_forecast_test, linestyle='--', label='Forecast')
plt.legend()
plt.show()

# --- 2. Simple Exponential Smoothing (SES) ---
def simple_exponential_smoothing(series, alpha):
    ses_values = [series[0]]
    for i in range(1, len(series)):
        ses_values.append(alpha * series[i] + (1 - alpha) * ses_values[i - 1])
    return np.array(ses_values)

alpha = 0.2
ses_train = simple_exponential_smoothing(train_data['Passengers'].values, alpha)
ses_full = simple_exponential_smoothing(pd.concat([train_data, test_data])['Passengers'].values, alpha)
ses_test = ses_full[len(train_data):len(train_data) + len(test_data)]

print("\n--- SES Metrics ---")
print("SES MAE:", mean_absolute_error(test_data['Passengers'], ses_test))
print("SES MSE:", mean_squared_error(test_data['Passengers'], ses_test)) # Added MSE
print("SES RMSE:", np.sqrt(mean_squared_error(test_data['Passengers'], ses_test)))

plt.figure(figsize=(10, 6))
plt.plot(train_data.index, ses_train, linestyle='--', label='SES Train')
plt.plot(test_data.index, ses_test, linestyle='--', label='SES Test')
plt.legend()
plt.show()

# --- 3. Holt-Winters Smoothing ---
from statsmodels.tsa.holtwinters import ExponentialSmoothing
seasonal_periods = 12

hw_model = ExponentialSmoothing(train_data['Passengers'], trend='add', seasonal='add', seasonal_periods=seasonal_periods)
hw_fit = hw_model.fit()
hw_forecast = hw_fit.forecast(len(test_data))

print("\n--- Holt-Winters Metrics ---")
print("HW MAE:", mean_absolute_error(test_data['Passengers'], hw_forecast))
print("HW MSE:", mean_squared_error(test_data['Passengers'], hw_forecast)) # Added MSE
print("HW RMSE:", np.sqrt(mean_squared_error(test_data['Passengers'], hw_forecast)))

# Identify trends and seasonal patterns (Visualize Components)
# This satisfies "Identify the trends and seasonal patterns"
pd.DataFrame({
    'Level': hw_fit.level,
    'Trend': hw_fit.trend,
    'Season': hw_fit.season
}).plot(subplots=True, figsize=(10, 8), title="Holt-Winters Components")
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(test_data.index, test_data['Passengers'], label='Actual')
plt.plot(test_data.index, hw_forecast, linestyle='--', label='HW Forecast')
plt.title("Holt-Winters Forecast")
plt.legend()
plt.show()









































# ===========================================================
# LAB 2 — MOVING AVERAGE, SES, HOLT-WINTERS (Week 4)
# ===========================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

data = pd.read_csv("AirPassengers.csv")
data['Passengers'] = data["value"]
# data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['date'])
data.set_index('Month', inplace=True)

def simple_moving_average(series, window_size):
    sma_values = []
    for i in range(len(series) - window_size + 1):
        window = series[i:i + window_size]
        sma_values.append(np.mean(window))
    return sma_values
window_size = 12
sma_values = simple_moving_average(data['Passengers'], window_size)
plt.figure(figsize=(10, 6))
plt.plot(data.index, data['Passengers'], label='Original Data')
plt.plot(data.index[window_size - 1:], sma_values, label='SMA')
plt.legend()
plt.show()
train_size = int(len(data) * 0.8)
train_data, test_data = data.iloc[:train_size], data.iloc[train_size:]
sma_forecast_full = simple_moving_average(pd.concat([train_data, test_data])['Passengers'], window_size)
sma_forecast_test = sma_forecast_full[len(train_data) - (window_size - 1):len(train_data) - (window_size - 1) + len(test_data)]
print("SMA MAE:", mean_absolute_error(test_data['Passengers'], sma_forecast_test))
print("SMA RMSE:", np.sqrt(mean_squared_error(test_data['Passengers'], sma_forecast_test)))
plt.figure(figsize=(10, 6))
plt.plot(train_data.index, train_data['Passengers'])
plt.plot(test_data.index, test_data['Passengers'])
plt.plot(test_data.index, sma_forecast_test, linestyle='--')
plt.show()
# SES
def simple_exponential_smoothing(series, alpha):
    ses_values = [series[0]]
    for i in range(1, len(series)):
        ses_values.append(alpha * series[i] + (1 - alpha) * ses_values[i - 1])
    return np.array(ses_values)
alpha = 0.2
ses_train = simple_exponential_smoothing(train_data['Passengers'].values, alpha)
ses_full = simple_exponential_smoothing(pd.concat([train_data, test_data])['Passengers'].values, alpha)
ses_test = ses_full[len(train_data):len(train_data) + len(test_data)]
print("SES MAE:", mean_absolute_error(test_data['Passengers'], ses_test))
print("SES RMSE:", np.sqrt(mean_squared_error(test_data['Passengers'], ses_test)))
plt.figure(figsize=(10, 6))
plt.plot(train_data.index, ses_train, linestyle='--')
plt.plot(test_data.index, ses_test, linestyle='--')
plt.show()
# Holt-Winters
from statsmodels.tsa.holtwinters import ExponentialSmoothing
seasonal_periods = 12
hw_model = ExponentialSmoothing(train_data['Passengers'], trend='add', seasonal='add', seasonal_periods=seasonal_periods)
hw_fit = hw_model.fit()
hw_forecast = hw_fit.forecast(len(test_data))
print("HW MAE:", mean_absolute_error(test_data['Passengers'], hw_forecast))
print("HW RMSE:", np.sqrt(mean_squared_error(test_data['Passengers'], hw_forecast)))
plt.figure(figsize=(10, 6))
plt.plot(test_data.index, test_data['Passengers'])
plt.plot(test_data.index, hw_forecast, linestyle='--')
plt.show()

"""  )





















