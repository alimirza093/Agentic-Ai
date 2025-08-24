import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
file_path = "covid-19_data.csv"
df = pd.read_csv(file_path)

# Convert date column
df['last_updated_date'] = pd.to_datetime(df['last_updated_date'])

# Filter for Pakistan
country = "Pakistan"
df_country = df[df['location'] == country].copy()

# Ensure numeric columns
numeric_cols = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths']
df_country[numeric_cols] = df_country[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Calculate CFR
df_country['CFR'] = (df_country['total_deaths'] / df_country['total_cases']) * 100

# Combined plot: New Cases + CFR
plt.figure(figsize=(10, 5))
plt.plot(df_country['last_updated_date'], df_country['new_cases'], label="New Cases", color='red', alpha=0.7)
plt.plot(df_country['last_updated_date'], df_country['CFR'], label="CFR (%)", color='purple', alpha=0.7)
plt.title(f"COVID-19 in {country} - New Cases & Case Fatality Rate")
plt.xlabel("Date")
plt.ylabel("Values")
plt.legend()
plt.grid()
plt.show()
