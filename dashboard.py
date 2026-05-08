import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from config import PROJECT_ID, DATASET_ID, TABLE_ID, CREDENTIALS_PATH
import time

st.set_page_config(page_title="Real-Time Data Pipeline Dashboard", layout="wide", page_icon="🚀")
st.title("🚀 Real-Time Data Pipeline Dashboard")
st.caption("HSBC Project | Pub/Sub simulation + BigQuery + Streamlit")

credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
client = bigquery.Client(project=PROJECT_ID, credentials=credentials)

@st.cache_data(ttl=5)
@st.cache_data(ttl=5)
def fetch_data():
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 10 MINUTE)
        ORDER BY timestamp ASC
    """
    return client.query(query).to_dataframe()

placeholder = st.empty()

while True:
    df = fetch_data()
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    iot_df = df[df['data_type'] == 'iot'].copy().sort_values('timestamp')
    log_df = df[df['data_type'] == 'log'].copy().sort_values('timestamp')

    with placeholder.container():

        # --- Metrics Row ---
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📦 Total Records", len(df))
        col2.metric("🌡️ IoT Readings", len(iot_df))
        col3.metric("📋 Log Entries", len(log_df))
        errors = len(log_df[log_df['log_level'].isin(['ERROR', 'CRITICAL'])])
        col4.metric("🔴 Errors / Critical", errors)

        st.divider()

        # --- Temperature Chart ---
        st.subheader("🌡️ Temperature Over Time")
        if not iot_df.empty:
            temp_chart = iot_df.set_index('timestamp')[['temperature']].dropna()
            st.line_chart(temp_chart)
        else:
            st.info("No IoT data yet...")

        # --- Humidity Chart ---
        st.subheader("💧 Humidity Over Time")
        if not iot_df.empty:
            humidity_chart = iot_df.set_index('timestamp')[['humidity']].dropna()
            st.line_chart(humidity_chart)
        else:
            st.info("No IoT data yet...")

        # --- Response Time Chart ---
        st.subheader("⚡ Server Response Time (ms)")
        if not log_df.empty:
            resp_chart = log_df.set_index('timestamp')[['response_time_ms']].dropna()
            st.line_chart(resp_chart)
        else:
            st.info("No log data yet...")

        # --- Log Level Distribution ---
        st.subheader("📊 Log Level Breakdown")
        if not log_df.empty:
            level_counts = log_df['log_level'].value_counts().reset_index()
            level_counts.columns = ['log_level', 'count']
            st.bar_chart(level_counts.set_index('log_level'))

        st.divider()

        # --- Anomalies ---
        st.subheader("⚠️ Anomalies Detected")
        anomalies = df[
            (df['temperature'] > 40) |
            (df['log_level'].isin(['ERROR', 'CRITICAL']))
        ][['timestamp', 'device_id', 'data_type', 'temperature', 'humidity', 'log_level']].copy()

        if not anomalies.empty:
            st.dataframe(anomalies, use_container_width=True)
        else:
            st.success("No anomalies detected!")

        # --- Latest Records (no message column) ---
        st.subheader("📋 Latest Records")
        display_cols = ['timestamp', 'device_id', 'data_type', 'temperature', 'humidity', 'log_level', 'response_time_ms']
        st.dataframe(df[display_cols].head(20), use_container_width=True)

    time.sleep(5)
    st.cache_data.clear()