import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(creds)


sheet = client.open_by_key("1DrqIrvowucKFuiDpVxHXSEhtnEXeZDz9zTfFKYAE4LE").sheet1
data = sheet.get_all_records()  
df = pd.DataFrame(data)  


# ... (your existing imports and data loading code) ...

# Fix date parsing (keep as datetime object - remove string conversion!)
df["Date"] = pd.to_datetime(
    df["Date"].str.strip(),
    format='%m/%d/%Y %H:%M:%S',
    errors="coerce"
).dt.tz_localize(None)  # Remove timezone if needed

df = df.dropna(subset=["Date"]).sort_values("Date")

# Add helper columns
df["Day"] = df["Date"].dt.date
df["Hour"] = df["Date"].dt.strftime("%H:%M")

# --- Feature 1: Day/Hour Selection or Manual Input ---
st.subheader("Find Temperature by Time")

# Option 1: Select from dropdowns
selected_day = st.selectbox("Choose a day", df["Day"].unique())
day_data = df[df["Day"] == selected_day]

if not day_data.empty:
    selected_hour = st.selectbox("Choose hour", day_data["Hour"].unique())
    temp = day_data[day_data["Hour"] == selected_hour]["Temperature"].values[0]
    st.write(f"Temperature on {selected_day} at {selected_hour}: **{temp}°C**")
else:
    st.warning("No data for selected day")
manual_time = st.text_input("Or enter exact time (YYYY-MM-DD HH:MM):")
if manual_time:
    try:
        target_time = pd.to_datetime(manual_time)
        closest_row = df.iloc[(df["Date"] - target_time).abs().argsort()[0]]
        st.write(f"Closest record ({closest_row['Date']}): **{closest_row['Temperature']}°C**")
    except:
        st.error("Invalid format! Use YYYY-MM-DD HH:MM")
# --- Feature 2: Daily Line Graph ---
st.divider()
st.subheader("Daily Temperature Chart")

# Date selector with default to middle date
center_date = st.selectbox(
    "Choose a day to analyze:",
    df["Day"].unique(),
    index=len(df["Day"].unique())//2  # Auto-center
)

# Filter and plot
daily_data = df[df["Day"] == center_date]
if not daily_data.empty:
    st.line_chart(daily_data, x="Hour", y="Temperature")
else:
    st.warning("No data for selected day")
"""
df["Date"] = pd.to_datetime(
    df["Date"].str.strip(),
    format='%m/%d/%Y %H:%M:%S',  
    errors="coerce"
)


df = df.dropna(subset=["Date"]).sort_values("Date")
df["Date"] = df["Date"].dt.strftime('%Y-%m-%d %H:%M:%S')
st.subheader("This is a line graph")
st.line_chart(df, x = "Date", y = "Temperature")
st.divider()
st.subheader("Full data table")
st.table(df)
"""
