import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

# Set up visualization parameters
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (14, 8)
%matplotlib inline

# Load dataset from GitHub
url = "https://raw.githubusercontent.com/shakir91/Proyek_Analisis_Data_LaskarAI/refs/heads/main/data/day.csv"
df = pd.read_csv(url)

# Convert and prepare datetime
df['dteday'] = pd.to_datetime(df['dteday'])
df.set_index('dteday', inplace=True)
df = df.sort_index()

# 1. Basic Time Series Plot
plt.figure(figsize=(16, 8))
plt.plot(df.index, df['cnt'], color='#2ca02c', linewidth=1.5)
plt.title('Daily Bike Rentals (2011-2012)', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Rentals', fontsize=12)
plt.grid(alpha=0.4)
plt.show()

# 2. Trend Analysis with Rolling Means
plt.figure(figsize=(16, 8))
plt.plot(df.index, df['cnt'], color='#1f77b4', alpha=0.3, label='Daily')
plt.plot(df.index, df['cnt'].rolling(7).mean(), color='#ff7f0e', linewidth=2, label='7D Moving Avg')
plt.plot(df.index, df['cnt'].rolling(30).mean(), color='#d62728', linewidth=2, label='30D Moving Avg')
plt.title('Bike Rental Trends with Moving Averages', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Rentals', fontsize=12)
plt.legend()
plt.grid(alpha=0.4)
plt.show()

# 3. Seasonal Decomposition (Multiplicative Model)
result = seasonal_decompose(df['cnt'], model='multiplicative', period=365)

plt.figure(figsize=(16, 12))
plt.subplot(4, 1, 1)
plt.plot(result.trend, color='#2ca02c')
plt.title('Trend Component', fontsize=12)

plt.subplot(4, 1, 2)
plt.plot(result.seasonal, color='#d62728')
plt.title('Seasonal Component', fontsize=12)

plt.subplot(4, 1, 3)
plt.plot(result.resid, color='#9467bd')
plt.title('Residual Component', fontsize=12)

plt.suptitle('Seasonal Decomposition of Bike Rentals', y=1.02, fontsize=16)
plt.tight_layout()
plt.show()

# 4. Year-over-Year Monthly Comparison
monthly_avg = df.groupby([df.index.year, df.index.month])['cnt'].mean().unstack(0)
monthly_avg.columns = ['2011', '2012']

plt.figure(figsize=(14, 7))
sns.lineplot(data=monthly_avg, markers=True, dashes=False, 
             palette=['#1f77b4', '#ff7f0e'], linewidth=2.5)
plt.title('Monthly Rental Patterns: 2011 vs 2012', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Average Rentals', fontsize=12)
plt.xticks(range(1,13), ['Jan','Feb','Mar','Apr','May','Jun',
                          'Jul','Aug','Sep','Oct','Nov','Dec'])
plt.grid(alpha=0.4)
plt.legend(title='Year')
plt.show()

# 5. Boxplot for Monthly Distribution (Corrected)
plt.figure(figsize=(14, 7))
sns.boxplot(
    x=df.index.month_name(),
    y=df['cnt'],
    hue=df.index.month_name(),  # Added hue parameter
    palette='viridis',
    dodge=False,  # Prevent automatic dodging
    legend=False,  # Suppress legend
    order=df.index.month_name().unique()
)
plt.title('Monthly Distribution of Bike Rentals', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Total Rentals', fontsize=12)
plt.xticks(rotation=45)
plt.grid(alpha=0.4)
plt.show()
