# AeroBurn

AI-powered fire safety dashboard by AeroBurn Engineering for NASA Space Apps 2026.

## Streamlit dashboard
This repository contains a Streamlit app for the challenge:
**"Flame in Freefall: SI-Powered Fire Safety Insights from Microgravity Combustion Data"**.

The dashboard includes:
- A full **3D Plotly flame surface simulation**:
  - **Microgravity (Gravity = 0):** spherical flame with blue/electric visual profile
  - **Earth gravity (Gravity = 1):** elongated flame with yellow/red visual profile
- A predictive fire safety panel with direct input sliders:
  - O2 %
  - Pressure (kPa)
  - Gravity (G)
- A **Predictive Fire Safety Index** with visual alert states:
  - Nominal
  - Warning
  - Critical
- A dedicated section for **Terrestrial GIS Applications (Morocco GeoPortal)** linking isolated microgravity combustion laws to forest-fire hazard mapping in Morocco.

## Run locally
```bash
pip install -r requirements.txt
streamlit run /home/runner/work/AeroBurn/AeroBurn/streamlit_app.py
```
