import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose

# Load data
url = "https://raw.githubusercontent.com/shakir91/Proyek_Analisis_Data_LaskarAI/refs/heads/main/data/day.csv"
df = pd.read_csv(url)
df['dteday'] = pd.to_datetime(df['dteday'])
df = df.sort_values('dteday')

# 1. Interactive Time Series Plot
fig1 = px.line(df, x='dteday', y='cnt', 
              labels={'cnt': 'Total Rentals', 'dteday': 'Date'},
              title='Daily Bike Rentals (2011-2012)',
              template='plotly_white')
fig1.update_layout(hovermode="x unified")
fig1.update_traces(line_color='#2ca02c', hovertemplate='Date: %{x}<br>Rentals: %{y}')
fig1.update_xaxes(rangeslider_visible=True)
fig1.show()

# 2. Interactive Trend Analysis
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df['dteday'], y=df['cnt'],
                         name='Daily',
                         line=dict(color='#1f77b4', width=1),
                         opacity=0.3))
fig2.add_trace(go.Scatter(x=df['dteday'], y=df['cnt'].rolling(7).mean(),
                         name='7D Moving Avg',
                         line=dict(color='#ff7f0e', width=2)))
fig2.add_trace(go.Scatter(x=df['dteday'], y=df['cnt'].rolling(30).mean(),
                         name='30D Moving Avg',
                         line=dict(color='#d62728', width=2)))

fig2.update_layout(title='Bike Rental Trends with Moving Averages',
                 xaxis_title='Date',
                 yaxis_title='Total Rentals',
                 template='plotly_white',
                 hovermode="x unified",
                 xaxis=dict(rangeslider=dict(visible=True)))
fig2.show()

# 3. Interactive Seasonal Decomposition
result = seasonal_decompose(df.set_index('dteday')['cnt'], model='multiplicative', period=365)

fig3 = make_subplots(rows=4, cols=1, shared_xaxes=True,
                    subplot_titles=("Observed", "Trend", "Seasonal", "Residual"))

fig3.add_trace(go.Scatter(x=df['dteday'], y=df['cnt'],
                         name='Observed',
                         line=dict(color='#2ca02c')),
              row=1, col=1)

fig3.add_trace(go.Scatter(x=result.trend.index, y=result.trend,
                         name='Trend',
                         line=dict(color='#d62728')),
              row=2, col=1)

fig3.add_trace(go.Scatter(x=result.seasonal.index, y=result.seasonal,
                         name='Seasonal',
                         line=dict(color='#9467bd')),
              row=3, col=1)

fig3.add_trace(go.Scatter(x=result.resid.index, y=result.resid,
                         name='Residual',
                         line=dict(color='#8c564b')),
              row=4, col=1)

fig3.update_layout(height=800, title_text="Seasonal Decomposition of Bike Rentals",
                 template='plotly_white', showlegend=False)
fig3.show()

# 4. Interactive Year-over-Year Comparison
monthly_avg = df.groupby([df['dteday'].dt.year, df['dteday'].dt.month])['cnt'].mean().unstack(0)
monthly_avg.columns = ['2011', '2012']
monthly_avg = monthly_avg.reset_index().melt(id_vars='dteday', var_name='Year', value_name='Average Rentals')

fig4 = px.line(monthly_avg, x='dteday', y='Average Rentals', color='Year',
              labels={'dteday': 'Month'},
              title='Monthly Rental Patterns: 2011 vs 2012',
              template='plotly_white',
              color_discrete_sequence=['#1f77b4', '#ff7f0e'],
              markers=True)

fig4.update_xaxes(tickvals=list(range(1,13)), 
                 ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
fig4.update_layout(hovermode="x unified",
                 xaxis_title="Month",
                 yaxis_title="Average Rentals")
fig4.show()

# 5. Interactive Boxplot
df['month_name'] = df['dteday'].dt.month_name()
fig5 = px.box(df, x='month_name', y='cnt', 
             title='Monthly Distribution of Bike Rentals',
             labels={'cnt': 'Total Rentals', 'month_name': 'Month'},
             category_orders={'month_name': ['January', 'February', 'March', 'April',
                                            'May', 'June', 'July', 'August',
                                            'September', 'October', 'November', 'December']},
             color_discrete_sequence=['#636EFA'],
             template='plotly_white')

fig5.update_traces(hovertemplate='Month: %{x}<br>Max: %{max}<br>Q3: %{q3}<br>Median: %{median}<br>Q1: %{q1}<br>Min: %{min}')
fig5.update_layout(showlegend=False,
                 xaxis=dict(tickangle=45))
fig5.show()
