# 🚀 Real-Time Data Pipeline & Dashboard

**HSBC Assessment Project** | Built with Google Cloud + Python + Streamlit

## 🏗️ Architecture

Simulated Data (IoT + Logs)
→ Publisher (Pub/Sub simulation)
→ Subscriber (Cloud Function simulation)
→ Google BigQuery (Data Warehouse)
→ Streamlit Dashboard (Live Visualization)

## ⚙️ Tech Stack

| Component | Technology |
|---|---|
| Data Ingestion | Pub/Sub (simulated via Python Queue) |
| Processing | Cloud Functions (simulated via Python) |
| Storage | Google BigQuery |
| Dashboard | Streamlit |
| Language | Python 3.11 |

## 📊 Features

- Simulates real-time IoT sensor data (temperature, humidity)
- Simulates server log data (INFO, WARNING, ERROR, CRITICAL)
- Anomaly detection — flags high temperature & critical errors
- Live dashboard with auto-refresh every 5 seconds
- Batch inserts to BigQuery

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/hsbc-realtime-pipeline.git
cd hsbc-realtime-pipeline
```

### 2. Install dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add GCP credentials
- Create a service account in GCP Console
- Download JSON key and save as `credentials.json` in project root
- Update `config.py` with your Project ID

### 4. Run the pipeline
```bash
# Terminal 1
python main.py

# Terminal 2
streamlit run dashboard.py
```

## 📁 Project Structure

hsbc-realtime-pipeline/
├── config.py              # GCP project config
├── publisher.py           # Simulates Pub/Sub publisher
├── subscriber.py          # Simulates Cloud Function trigger
├── bigquery_client.py     # BigQuery batch insert handler
├── main.py                # Pipeline entry point
├── dashboard.py           # Streamlit dashboard
└── requirements.txt       # Dependencies

## ⚠️ Note
`credentials.json` is excluded from this repo for security.
Add your own GCP service account key to run locally.