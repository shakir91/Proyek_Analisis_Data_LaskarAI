import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/shakir91/Proyek_Analisis_Data_LaskarAI/main/data/hour.csv"
    df = pd.read_csv(url)
    
    # Data preprocessing
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

# Additional visualizations
st.header("Advanced Visualizations")

col1, col2 = st.columns(2)

with col1:
    st.subheader("User Type Distribution")
    user_types = filtered_df[['casual', 'registered']].sum().reset_index()
    user_types.columns = ['user_type', 'count']
    
    fig = px.pie(user_types, values='count', names='user_type', 
                 title='Registered vs Casual Users')
    st.plotly_chart(fig)

with col2:
    st.subheader("Weekly Patterns")
    heatmap_data = filtered_df.groupby(['weekday', 'hour'])['cnt'].mean().unstack()
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex(days_order)
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Blues'))
    fig.update_layout(title='Average Rentals by Hour and Weekday',
                      xaxis_title='Hour of Day',
                      yaxis_title='Day of Week')
    st.plotly_chart(fig)