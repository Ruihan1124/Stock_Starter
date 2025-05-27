from prophet import Prophet

# 使用 Facebook Prophet 对 df（含 ds 和 y）做预测
def forecast_stock(df, periods=7):
    model = Prophet(daily_seasonality=True)
    model.fit(df)  # df 必须有 'ds' 和 'y'
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast
