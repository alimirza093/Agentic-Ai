import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
url = "IMDB-Movie-Data.csv"  # Replace with the actual path or URL to the dataset
df = pd.read_csv(url)

# Display first few rows
print(df.head())

# Convert 'Released_Year' column to numeric
df['Released_Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Top 10 highest-rated movies
top_movies = df[['Title', 'Rating']].sort_values(by='Rating', ascending=False).head(10)
print("\nTop 10 Highest-Rated Movies:\n", top_movies)

# Count movies by genre
df['Genre'] = df['Genre'].apply(lambda x: x.split(',')[0])  # Take first genre if multiple
genre_counts = df['Genre'].value_counts()

# Plot genres
plt.figure(figsize=(10,5))
genre_counts.head(10).plot(kind='bar', color='skyblue')
plt.title("Top 10 Movie Genres in IMDb Dataset")
plt.xlabel("Genre")
plt.ylabel("Number of Movies")
plt.xticks(rotation=45)
plt.show()

# Trend of movies released over years
df.groupby('Released_Year').size().plot(kind='line', figsize=(10,5), color='red', marker='o')
plt.title("Movies Released Over the Years")
plt.xlabel("Year")
plt.ylabel("Number of Movies")
plt.grid()
plt.show()