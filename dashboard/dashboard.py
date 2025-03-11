import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# Load both datasets
daily_url = "https://raw.githubusercontent.com/shakir91/Proyek_Analisis_Data_LaskarAI/main/data/day.csv"
hourly_url = "https://raw.githubusercontent.com/shakir91/Proyek_Analisis_Data_LaskarAI/main/data/hour.csv"

daily_df = pd.read_csv(daily_url)
hourly_df = pd.read_csv(hourly_url)

# Convert dates and prepare for merging
daily_df['dteday'] = pd.to_datetime(daily_df['dteday'])
hourly_df['dteday'] = pd.to_datetime(hourly_df['dteday'])

# Create a merged dataframe
merged_df = pd.merge(hourly_df, daily_df, on='dteday', suffixes=('_hourly', '_daily'))

#Judul
st.title("Bike Sharing Data Analytics")

st.subheader("Daily vs Hourly Totals Validation")
# Check if hourly sums match daily totals
validation_df = merged_df.groupby('dteday').agg(
    hourly_total=('cnt_hourly', 'sum'),
    daily_total=('cnt_daily', 'first')
).reset_index()

fig = px.scatter(validation_df, x='daily_total', y='hourly_total', 
                title='Validation: Daily vs Summed Hourly Rentals',
                labels={'daily_total': 'Daily Reported Total', 
                        'hourly_total': 'Hourly Summed Total'})
fig.add_trace(go.Scatter(x=[0, 10000], y=[0, 10000], 
             mode='lines', name='Perfect Match'))
fig.show()

st.subheader("Hourly Contribution to Daily Demand")
merged_df['hourly_contribution'] = merged_df['cnt_hourly'] / merged_df['cnt_daily']

fig = px.box(merged_df, x='hr', y='hourly_contribution', color='workingday_hourly',
            labels={'hr': 'Hour of Day', 
                    'hourly_contribution': 'Proportion of Daily Total',
                    'workingday_hourly': 'Working Day'},
            title='Hourly Contribution to Daily Demand')
fig.show()

st.subheader("Daily-Hourly Pattern Explorer")
fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

# Daily trend
fig.add_trace(go.Scatter(x=daily_df['dteday'], y=daily_df['cnt'],
                        name='Daily Total', line=dict(color='blue')),
             row=1, col=1)

# Hourly heatmap
hourly_pivot = merged_df.pivot_table(index='dteday', columns='hr', values='cnt_hourly')
fig.add_trace(go.Heatmap(z=hourly_pivot.values.T,
                        x=hourly_pivot.index,
                        y=hourly_pivot.columns,
                        colorscale='Viridis',
                        colorbar=dict(title='Hourly Rentals')),
             row=2, col=1)

fig.update_layout(height=600, title_text='Combined Daily Trend & Hourly Patterns')
fig.show()

st.subheader("Interactive Cross-Filtering")
fig = px.scatter(merged_df, x='temp_daily', y='cnt_hourly', 
                animation_frame='hr',
                color='weathersit_daily',
                size='cnt_hourly',
                range_x=[0,1], range_y=[0,1000],
                labels={'temp_daily': 'Daily Temperature',
                        'cnt_hourly': 'Hourly Rentals',
                        'weathersit_daily': 'Weather Condition'},
                title='Hourly Rentals vs Daily Temperature (Animation by Hour)')
fig.show()

st.subheader("Correlation Matrix (Daily vs Hourly Features)")
corr_matrix = merged_df[['cnt_daily', 'cnt_hourly', 'temp_daily',
                        'hum_daily', 'windspeed_daily', 'hr',
                        'workingday_hourly']].corr()

fig = px.imshow(corr_matrix, 
               x=corr_matrix.columns,
               y=corr_matrix.columns,
               color_continuous_scale='RdBu',
               title='Feature Correlation Matrix')
fig.show()
