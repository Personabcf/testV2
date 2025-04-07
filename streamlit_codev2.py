import streamlit as st
st.write("Hello")
"""import streamlit as st
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
)


df = df.dropna(subset=["Date"]).sort_values("Date")
df["Date"] = df["Date"].dt.strftime('%Y-%m-%d %H:%M:%S')
st.subheader("This is a line graph")
st.line_chart(df, x = "Date", y = "Temperature")
st.divider()
st.subheader("Full data table")
st.table(df)"""
