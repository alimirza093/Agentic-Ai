import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('apple_stock_datas.csv')

# Strip spaces from column names
df.columns = df.columns.str.strip()

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Convert numerical columns (remove '$' and ',' before converting to float)
numeric_cols = ['Close', 'Open', 'High', 'Low']
for col in numeric_cols:
    df[col] = df[col].replace({'\$': '', ',': ''}, regex=True).astype(float)

# Set Date as index
df.set_index('Date', inplace=True)

# Plot closing price over time
plt.figure(figsize=(10,5))
plt.plot(df.index, df['Close'], label="Closing Price", color='blue')
plt.title("Apple Stock Prices")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid()
plt.show()

# Calculate moving average (50-day and 200-day)
df['50-day MA'] = df['Close'].rolling(window=50).mean()
df['200-day MA'] = df['Close'].rolling(window=200).mean()

# Plot Moving Averages
plt.figure(figsize=(10,5))
plt.plot(df.index, df['Close'], label="Closing Price", color='blue', alpha=0.5)
plt.plot(df.index, df['50-day MA'], label="50-Day Moving Average", color='red')
plt.plot(df.index, df['200-day MA'], label="200-Day Moving Average", color='green')
plt.title("Apple Stock Price with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid()
plt.show()