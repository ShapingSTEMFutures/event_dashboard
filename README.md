# Shaping STEM Futures – Event Dashboard

Streamlit dashboard displaying workshop registration data for the Shaping STEM Futures program at Swinburne University of Technology.

## How to update data
Open `events_data.xlsx`, add a new row to the **Events** sheet (date, event name, registrations), and push to GitHub. The dashboard updates automatically.

## How to run locally
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## Stack
Python · Streamlit · Pandas · Plotly
