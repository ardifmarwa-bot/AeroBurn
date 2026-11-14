# AeroBurn

AI-powered fire safety dashboard by AeroBurn Engineering for NASA Space Apps 2026.

## Streamlit dashboard
This repository contains a Streamlit app for the challenge:
**"Flame in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data"**.

The dashboard includes:
- A Plotly 3D flame model that appears **spherical in microgravity** and **elongated under Earth gravity**.
- A predictive fire safety panel with simulated real-time sensor data:
  - Oxygen level (%)
  - Atmospheric pressure (kPa)
  - Ambient gravity (g)

## Run locally
```bash
pip install -r requirements.txt
streamlit run /home/runner/work/AeroBurn/AeroBurn/streamlit_app.py
```
