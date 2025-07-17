import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load Data ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/shakir91/Proyek_Analisis_Data_LaskarAI/main/data/hour.csv"
    df = pd.read_csv(url)
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['weekday'] = df['weekday'].map({
        0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
        4: 'Thursday', 5: 'Friday', 6: 'Saturday'
    })
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filter")
selected_weekday = st.sidebar.multiselect("Select Weekday(s)", options=df['weekday'].unique(), default=df['weekday'].unique())
selected_hour = st.sidebar.slider("Select Hour Range", 0, 23, (0, 23))

# Filter Data
filtered_df = df[(df['weekday'].isin(selected_weekday)) & (df['hr'].between(*selected_hour))]

# --- Dashboard Title ---
st.title("🚲 Bike Sharing Dashboard")

# --- Average Hourly Rentals Pattern ---
st.subheader("📊 Average Hourly Rentals Pattern")
avg_hourly = filtered_df.groupby('hr')['cnt'].mean().reset_index()
fig_avg = px.line(avg_hourly, x='hr', y='cnt', title='Average Rentals per Hour', labels={'cnt': 'Average Rentals', 'hr': 'Hour'})
st.plotly_chart(fig_avg, use_container_width=True)

# --- Hourly Usage by User Type ---
st.subheader("👥 Hourly Usage by User Type")
user_hourly = filtered_df.groupby(['hr'])[['registered', 'casual']].mean().reset_index()
fig_user = px.line(user_hourly, x='hr', y=['registered', 'casual'], labels={'value': 'Average Users', 'hr': 'Hour'}, title='Hourly Usage by User Type')
st.plotly_chart(fig_user, use_container_width=True)

# --- Weekly Rental Patterns ---
st.subheader("📆 Weekly Rental Patterns")
weekly = filtered_df.groupby('weekday')['cnt'].sum().reset_index()
fig_week = px.bar(weekly, x='weekday', y='cnt', title='Total Rentals by Weekday', labels={'cnt': 'Total Rentals'})
st.plotly_chart(fig_week, use_container_width=True)

# --- Raw Data ---
with st.expander("🧾 View Raw Data"):
    st.dataframe(filtered_df.head(100))