import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/shakir91/Proyek_Analisis_Data_LaskarAI/main/data/hour.csv"
    df = pd.read_csv(url)
    
    # Data preprocessing (replicate from notebook)
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['datetime'] = df['dteday'] + pd.to_timedelta(df['hr'], unit='h')
    df['hour'] = df['datetime'].dt.hour
    df['weekday'] = df['datetime'].dt.day_name()
    df['season'] = df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    df['weathersit'] = df['weathersit'].map({1: 'Clear', 2: 'Mist', 3: 'Light Rain', 4: 'Heavy Rain'})
    
    return df

df = load_data()

# Streamlit app
st.title('Bike Sharing Analysis Dashboard')

# Dataset preview
with st.expander("View Raw Data"):
    st.write(df.describe())
    st.write(df.head())

# Main analysis tabs
tab1, tab2, tab3 = st.tabs(["Weather Impact", "Yearly Trends", "Workday vs Holiday"])

with tab1:
    st.header("Impact of Weather Conditions")
    weather_counts = df.groupby('weathersit')['cnt'].mean().reset_index()
    
    fig = px.bar(weather_counts, x='weathersit', y='cnt', 
                 labels={'cnt': 'Average Rentals', 'weathersit': 'Weather Condition'},
                 color='weathersit')
    st.plotly_chart(fig)

with tab2:
    st.header("Yearly Growth Trends")
    
    # Convert yr (0=2011, 1=2012)
    yearly = df.groupby('yr')['cnt'].sum().reset_index()
    yearly['year'] = yearly['yr'].map({0: 2011, 1: 2012})
    
    fig = px.line(yearly, x='year', y='cnt', markers=True,
                  labels={'cnt': 'Total Rentals', 'year': 'Year'},
                  title='Total Rentals by Year')
    fig.update_layout(yaxis_range=[0, yearly['cnt'].max()*1.1])
    st.plotly_chart(fig)

with tab3:
    st.header("Workday vs Holiday Comparison")
    
    day_comparison = df.groupby(['workingday', 'hr'])['cnt'].mean().reset_index()
    day_comparison['day_type'] = day_comparison['workingday'].map({1: 'Working Day', 0: 'Holiday'})
    
    fig = px.line(day_comparison, x='hr', y='cnt', color='day_type',
                  labels={'cnt': 'Average Rentals', 'hr': 'Hour of Day'},
                  title='Hourly Rental Patterns')
    st.plotly_chart(fig)
