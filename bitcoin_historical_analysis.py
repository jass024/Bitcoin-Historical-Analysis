import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

# 1. Read the CSV file into a DataFrame
df = pd.read_csv('bitcoin_2010-07-27_2024-04-25.csv')

# 2. Convert date columns to datetime format
df['Start'] = pd.to_datetime(df['Start'])

# 3. Aggregate the `Volume` by month using `pd.Grouper` and calculate the sum for each month.
df_agg = df.groupby(pd.Grouper(key='Start', freq='ME'))['Volume'].sum().reset_index()

# 4. Rename the columns to `Month` and `Total_Volume`.
df_agg.columns = ['Month', 'Total_Volume']

# 5. Convert the `Month` column to datetime format.
df_agg['Month'] = pd.to_datetime(df_agg['Month'])

# 6. Save the aggregated DataFrame to a new CSV file
df_agg.to_csv('bitcoin_volume_agg_updated.csv', index=False)

# 7. Calculate daily returns
df['Daily Returns'] = df['Close'].pct_change() * 100

# 8. Calculate 30-day rolling volatility
df['Volatility'] = df['Daily Returns'].rolling(window=30).std()

# 9. Calculate moving averages
df['SMA_10'] = df['Close'].rolling(window=10).mean()
df['SMA_50'] = df['Close'].rolling(window=50).mean()
df['SMA_200'] = df['Close'].rolling(window=200).mean()

# 10. Calculate the difference between the current day's close price and the previous day's close price
df['Price_Change'] = df['Close'].diff()

# 11. Calculate Average Gain and Average Loss over 14 days
df['Gain'] = df['Price_Change'].apply(lambda x: x if x > 0 else 0)
df['Loss'] = df['Price_Change'].apply(lambda x: abs(x) if x < 0 else 0)
df['Average_Gain'] = df['Gain'].rolling(window=14).mean()
df['Average_Loss'] = df['Loss'].rolling(window=14).mean()

# 12. Calculate RS and RSI
df['RS'] = df['Average_Gain'] / df['Average_Loss']
df['RSI'] = 100 - (100 / (1 + df['RS']))

# 13. Calculate 200-day EMA
df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()

# 14. Drop rows with NaN values
df.dropna(inplace=True)

# 15. Create a Plotly line chart of the closing price over time
fig_close = go.Figure()
fig_close.add_trace(go.Scatter(x=df['Start'], y=df['Close'], mode='lines', name='Close Price'))
fig_close.update_layout(title='Bitcoin Closing Price Over Time', xaxis_title='Date', yaxis_title='Closing Price')

# 16. Create a Plotly histogram of the daily returns
fig_returns = go.Figure()
fig_returns.add_trace(go.Histogram(x=df['Daily Returns'], nbinsx=30, name='Daily Returns'))
fig_returns.update_layout(title='Distribution of Bitcoin Daily Returns', xaxis_title='Daily Returns (%)', yaxis_title='Frequency')

# 17. Create a Plotly line chart of the 30-day rolling volatility over time
fig_volatility = go.Figure()
fig_volatility.add_trace(go.Scatter(x=df['Start'], y=df['Volatility'], mode='lines', name='30-Day Rolling Volatility'))
fig_volatility.update_layout(title='Bitcoin 30-Day Rolling Volatility Over Time', xaxis_title='Date', yaxis_title='Volatility')

# 18. Create a Plotly line chart of the RSI over time, with horizontal lines at 30 and 70
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=df['Start'], y=df['RSI'], mode='lines', name='RSI'))
fig_rsi.add_hline(y=70, line_width=1, line_dash="dash", line_color="red", annotation_text="Overbought", annotation_position="top right")
fig_rsi.add_hline(y=30, line_width=1, line_dash="dash", line_color="green", annotation_text="Oversold", annotation_position="bottom right")
fig_rsi.update_layout(title='Bitcoin Relative Strength Index (RSI) Over Time', xaxis_title='Date', yaxis_title='RSI')

# 19. Create a Plotly line chart with multiple lines for closing price, SMA_10, SMA_50, SMA_200, and EMA_200
fig_sma = go.Figure()
fig_sma.add_trace(go.Scatter(x=df['Start'], y=df['Close'], mode='lines', name='Close Price'))
fig_sma.add_trace(go.Scatter(x=df['Start'], y=df['SMA_10'], mode='lines', name='SMA 10'))
fig_sma.add_trace(go.Scatter(x=df['Start'], y=df['SMA_50'], mode='lines', name='SMA 50'))
fig_sma.add_trace(go.Scatter(x=df['Start'], y=df['SMA_200'], mode='lines', name='SMA 200'))
fig_sma.add_trace(go.Scatter(x=df['Start'], y=df['EMA_200'], mode='lines', name='EMA 200'))
fig_sma.update_layout(title='Bitcoin Closing Price and Moving Averages Over Time', xaxis_title='Date', yaxis_title='Price')

# 20. Create a Plotly bar chart of total volume by month
fig_volume = go.Figure()
fig_volume.add_trace(go.Bar(x=df_agg['Month'], y=df_agg['Total_Volume'], name='Total Volume'))
fig_volume.update_layout(title='Total Bitcoin Volume by Month (2010-2024)', xaxis_title='Month', yaxis_title='Total Volume')

# 21. Save each chart as a separate HTML file
fig_close.write_html('bitcoin_closing_price_line_chart.html')
fig_returns.write_html('bitcoin_daily_returns_histogram.html')
fig_volatility.write_html('bitcoin_volatility_line_chart.html')
fig_rsi.write_html('bitcoin_rsi_line_chart.html')
fig_sma.write_html('bitcoin_closing_price_and_moving_averages_line_chart.html')
fig_volume.write_html('bitcoin_volume_by_month_bar_chart.html')

# 22. Display each chart
fig_close.show()
fig_returns.show()
fig_volatility.show()
fig_rsi.show()
fig_sma.show()
fig_volume.show()
