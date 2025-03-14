import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

hourly_url = "https://raw.githubusercontent.com/shakir91/Proyek_Analisis_Data_LaskarAI/main/data/hour.csv"
hour_df = pd.read_csv(hourly_url)

hourly_avg = hour_df.groupby('hour')['cnt'].mean()
user_types = hour_df.groupby('hr')[['casual', 'registered']].mean()
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
heatmap_data = hour_df.groupby(['weekday', 'hour'])['cnt'].mean().unstack()
heatmap_data.describe(include=("all"))

#Data Pre-Processing
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
hour_df['datetime'] = hour_df['dteday'] + pd.to_timedelta(hour_df['hr'], unit='h')
hour_df['hour'] = hour_df['datetime'].dt.hour
hour_df['weekday'] = hour_df['datetime'].dt.day_name()
hour_df['season'] = hour_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
hour_df['weathersit'] = hour_df['weathersit'].map({1: 'Clear', 2: 'Mist', 3: 'Light Rain', 4: 'Heavy Rain'})
hourly_avg = hour_df.groupby('hour')['cnt'].mean()

plt.figure(figsize=(12, 6))
sns.lineplot(x=hourly_avg.index, y=hourly_avg.values, color='#2ca02c')
plt.title('Average Hourly Rentals Pattern', fontsize=14)
plt.xlabel('Hour of Day')
plt.ylabel('Average Rentals')
plt.xticks(range(0, 24))
plt.grid(True, alpha=0.3)
plt.show()



