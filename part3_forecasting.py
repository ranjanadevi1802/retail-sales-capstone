import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
import os
warnings.filterwarnings('ignore')

os.makedirs('outputs', exist_ok=True)

def prepare_timeseries(csv_path='data/cleaned_superstore.csv'):
    df = pd.read_csv(csv_path, parse_dates=['Order_Date'])
    df['Month'] = df['Order_Date'].dt.to_period('M').dt.to_timestamp()
    monthly = df.groupby('Month')['Sales'].sum().reset_index()
    monthly.columns = ['ds', 'y']
    monthly = monthly.sort_values('ds').reset_index(drop=True)
    print(f"✅ Time series ready: {len(monthly)} monthly points")
    print(monthly.tail())
    return monthly

def run_arima(monthly_df, forecast_months=6):
    from statsmodels.tsa.arima.model import ARIMA
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    print("\n===== ARIMA FORECASTING =====")
    train = monthly_df[:-forecast_months]
    test  = monthly_df[-forecast_months:]

    model  = ARIMA(train['y'], order=(2, 1, 2))
    fitted = model.fit()
    forecast_test = fitted.forecast(steps=forecast_months)

    mae  = mean_absolute_error(test['y'], forecast_test)
    rmse = np.sqrt(mean_squared_error(test['y'], forecast_test))
    print(f"  MAE  : ${mae:,.2f}")
    print(f"  RMSE : ${rmse:,.2f}")

    model_full  = ARIMA(monthly_df['y'], order=(2, 1, 2))
    fitted_full = model_full.fit()
    future_preds = fitted_full.forecast(steps=forecast_months)

    last_date    = monthly_df['ds'].max()
    future_dates = pd.date_range(
        start=last_date + pd.DateOffset(months=1),
        periods=forecast_months, freq='MS')
    forecast_df  = pd.DataFrame({'ds': future_dates, 'forecast': future_preds})

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(monthly_df['ds'], monthly_df['y'], label='Historical', color='steelblue')
    ax.plot(test['ds'], forecast_test, label='ARIMA Test', color='orange', linestyle='--')
    ax.plot(forecast_df['ds'], forecast_df['forecast'],
            label='ARIMA Forecast', color='crimson', linestyle='--', marker='o')
    ax.set_title('ARIMA Sales Forecast', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Sales ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.legend()
    plt.tight_layout()
    plt.savefig('outputs/09_arima_forecast.png')
    plt.close()
    print("✅ Saved: outputs/09_arima_forecast.png")

    forecast_df.to_csv('outputs/arima_forecast.csv', index=False)
    print("✅ Saved: outputs/arima_forecast.csv")

    return forecast_df, mae, rmse

def run_prophet(monthly_df, forecast_months=6):
    from prophet import Prophet
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    print("\n===== PROPHET FORECASTING =====")
    train = monthly_df[:-forecast_months].copy()
    test  = monthly_df[-forecast_months:].copy()

    model = Prophet(yearly_seasonality=True,
                    weekly_seasonality=False,
                    daily_seasonality=False,
                    seasonality_mode='multiplicative')
    model.fit(train)

    future_test = model.make_future_dataframe(periods=forecast_months, freq='MS')
    forecast    = model.predict(future_test)

    test_preds = forecast[forecast['ds'].isin(test['ds'])]['yhat'].values
    mae  = mean_absolute_error(test['y'].values, test_preds)
    rmse = np.sqrt(mean_squared_error(test['y'].values, test_preds))
    print(f"  MAE  : ${mae:,.2f}")
    print(f"  RMSE : ${rmse:,.2f}")

    future      = model.make_future_dataframe(
        periods=len(monthly_df) + forecast_months, freq='MS')
    forecast_full = model.predict(future)

    fig = model.plot(forecast_full)
    plt.title('Prophet Sales Forecast', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/10_prophet_forecast.png')
    plt.close()
    print("✅ Saved: outputs/10_prophet_forecast.png")

    fig2 = model.plot_components(forecast_full)
    plt.tight_layout()
    plt.savefig('outputs/11_prophet_components.png')
    plt.close()
    print("✅ Saved: outputs/11_prophet_components.png")

    future_only = forecast_full[
        forecast_full['ds'] > monthly_df['ds'].max()
    ][['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head(forecast_months)
    future_only.columns = ['ds', 'forecast', 'lower_bound', 'upper_bound']
    future_only.to_csv('outputs/prophet_forecast.csv', index=False)
    print("✅ Saved: outputs/prophet_forecast.csv")

    return future_only, mae, rmse

def compare_models(arima_metrics, prophet_metrics):
    print("\n===== MODEL COMPARISON =====")
    print(f"{'Model':<10} {'MAE':>12} {'RMSE':>12}")
    print("-" * 36)
    print(f"{'ARIMA':<10} ${arima_metrics[0]:>10,.2f} ${arima_metrics[1]:>10,.2f}")
    print(f"{'Prophet':<10} ${prophet_metrics[0]:>10,.2f} ${prophet_metrics[1]:>10,.2f}")
    winner = "ARIMA" if arima_metrics[1] < prophet_metrics[1] else "Prophet"
    print(f"\n🏆 Better model (lower RMSE): {winner}")

if __name__ == "__main__":
    print("=" * 50)
    print(" PART 3: FORECASTING")
    print("=" * 50)

    monthly = prepare_timeseries()

    arima_result   = run_arima(monthly, forecast_months=6)
    prophet_result = run_prophet(monthly, forecast_months=6)

    _, arima_mae, arima_rmse     = arima_result
    _, prophet_mae, prophet_rmse = prophet_result
    compare_models((arima_mae, arima_rmse), (prophet_mae, prophet_rmse))

    print("\n✅ Part 3 complete! Forecasts saved in outputs/ folder.")
