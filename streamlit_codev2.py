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


df["Date"] = pd.to_datetime(
    df["Date"].str.strip(),
    format='%m/%d/%Y %H:%M:%S',
    errors="coerce"
).dt.tz_localize(None)  # Remove timezone if needed

df = df.dropna(subset=["Date"]).sort_values("Date")

# Add helper columns
df["Day"] = df["Date"].dt.date
df["Hour"] = df["Date"].dt.strftime("%H:%M")

st.subheader("Find Temperature by Time")

selected_day = st.selectbox("Choose a day", df["Day"].unique())
day_data = df[df["Day"] == selected_day]

if not day_data.empty:
    selected_hour = st.selectbox("Choose hour", day_data["Hour"].unique())
    temp = day_data[day_data["Hour"] == selected_hour]["Temperature"].values[0]
    st.write(f"Temperature on {selected_day} at {selected_hour}: **{temp}°C**")
else:
    st.warning("No data for selected day")
st.divider()
st.subheader("Daily Temperature Chart")

center_date = st.selectbox(
    "Choose a day to analyze:",
    df["Day"].unique(),
    index=len(df["Day"].unique())//2  
)

daily_data = df[df["Day"] == center_date]
if not daily_data.empty:
    st.line_chart(daily_data, x="Hour", y="Temperature")
else:
    st.warning("No data for selected day")
st.write("All temperature is in degrees celsius.")
st.write("The point of this webiste is to prodive river temperatures. The river temperature has been collected appropriately with no damage to the natural environment.")
