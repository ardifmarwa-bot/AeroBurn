import time
from datetime import datetime

import numpy as np
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(page_title="AeroBurn Engineering", layout="wide")
st.title("🚀 AeroBurn Engineering")
st.caption(
    "NASA Space Apps Challenge 2026 — Flame in Freefall: SI-Powered Fire Safety Insights "
    "from Microgravity Combustion Data"
)


def build_flame_surface(gravity_level: float) -> go.Figure:
    u = np.linspace(0, 2 * np.pi, 120)
    v = np.linspace(0, np.pi, 100)
    u_grid, v_grid = np.meshgrid(u, v)

    radius = 1.0
    x_sphere = radius * np.sin(v_grid) * np.cos(u_grid)
    y_sphere = radius * np.sin(v_grid) * np.sin(u_grid)
    z_sphere = radius * np.cos(v_grid)

    z_elong = 1.8 * np.cos(v_grid) + 0.65
    radial_shrink = np.clip(0.95 - 0.42 * (z_elong + 1) / 2.8, 0.2, 1.0)
    x_elong = radial_shrink * np.sin(v_grid) * np.cos(u_grid)
    y_elong = radial_shrink * np.sin(v_grid) * np.sin(u_grid)

    blend = np.clip(gravity_level, 0.0, 1.0)
    x = (1 - blend) * x_sphere + blend * x_elong
    y = (1 - blend) * y_sphere + blend * y_elong
    z = (1 - blend) * z_sphere + blend * z_elong

    intensity = np.sqrt(x**2 + y**2 + (z * 0.6) ** 2)
    colorscale = "Electric" if gravity_level <= 0.05 else "YlOrRd"
    title = (
        "Microgravity Flame Surface (Spherical, Blue/Electric)"
        if gravity_level <= 0.05
        else "Earth-Gravity Flame Surface (Elongated, Yellow/Red)"
    )

    fig = go.Figure(
        data=[
            go.Surface(
                x=x,
                y=y,
                z=z,
                surfacecolor=intensity,
                colorscale=colorscale,
                opacity=0.93,
                showscale=True,
                colorbar=dict(title="Heat field"),
            )
        ]
    )
    fig.update_layout(
        title=title,
        margin=dict(l=0, r=0, t=40, b=0),
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            bgcolor="rgba(0,0,0,0)",
            camera=dict(eye=dict(x=1.55, y=1.55, z=1.2)),
        ),
    )
    return fig


def simulate_sensor_series(
    oxygen_input: float,
    pressure_input: float,
    gravity_input: float,
    samples: int = 60,
):
    now = time.time()
    timeline = np.linspace(now - samples + 1, now, samples)

    oxygen = oxygen_input + 0.12 * np.sin(timeline / 4) + np.random.normal(0, 0.03, samples)
    pressure = pressure_input + 0.2 * np.cos(timeline / 6) + np.random.normal(0, 0.04, samples)
    gravity = gravity_input + 0.02 * np.sin(timeline / 7) + np.random.normal(0, 0.003, samples)

    readable_time = [datetime.fromtimestamp(t).strftime("%H:%M:%S") for t in timeline]
    return readable_time, oxygen, pressure, gravity


def calculate_fire_safety_index(oxygen_pct: float, pressure_kpa: float, gravity_g: float) -> float:
    oxygen_penalty = abs(oxygen_pct - 20.9) * 8
    low_oxygen_extra = max(0.0, 19.5 - oxygen_pct) * 12
    pressure_penalty = abs(pressure_kpa - 101.3) * 2.5
    gravity_penalty = gravity_g * 22

    return float(np.clip(oxygen_penalty + low_oxygen_extra + pressure_penalty + gravity_penalty, 0, 100))


with st.sidebar:
    st.header("Simulation Controls")
    gravity_level = st.slider("Gravity G", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    oxygen_level = st.slider("O2 %", min_value=16.0, max_value=23.0, value=20.9, step=0.1)
    pressure_level = st.slider("Pressure kPa", min_value=85.0, max_value=115.0, value=101.3, step=0.1)

left_col, right_col = st.columns([1.2, 1])

with left_col:
    st.subheader("3D Flame Surface Simulation")
    st.plotly_chart(build_flame_surface(gravity_level), use_container_width=True)

with right_col:
    st.subheader("Predictive Fire Safety Dashboard")
    timestamps, oxygen, pressure, gravity = simulate_sensor_series(oxygen_level, pressure_level, gravity_level)

    c1, c2, c3 = st.columns(3)
    c1.metric("Oxygen (%)", f"{oxygen_level:.1f}")
    c2.metric("Pressure (kPa)", f"{pressure_level:.1f}")
    c3.metric("Gravity (G)", f"{gravity_level:.2f}")

    st.line_chart(
        {
            "time": timestamps,
            "oxygen_%": oxygen,
            "pressure_kPa": pressure,
            "gravity_G": gravity,
        },
        x="time",
    )

    fire_safety_index = calculate_fire_safety_index(oxygen_level, pressure_level, gravity_level)
    st.metric("Predictive Fire Safety Index", f"{fire_safety_index:.1f}/100")

    if fire_safety_index < 35:
        st.success("Nominal: combustion environment remains within expected safety margins.")
    elif fire_safety_index < 70:
        st.warning("Warning: deviations detected; monitor oxygen/pressure/gravity trends closely.")
    else:
        st.error("Critical: high-risk fire behavior conditions detected; immediate mitigation recommended.")

st.markdown("---")
st.subheader("Terrestrial GIS Applications (Morocco GeoPortal)")
st.write(
    "AeroBurn uses microgravity combustion laws as a clean baseline to isolate oxygen, pressure, and "
    "flow-driven flame behavior before applying them to Earth wildfire contexts. "
    "In Morocco GeoPortal workflows, these laws help calibrate forest-fire spread layers by separating "
    "terrain/wind effects from intrinsic combustion dynamics, improving risk zoning and early-warning mapping."
)
st.markdown(
    "- Map likely acceleration zones where oxygen availability and pressure gradients amplify flame persistence.\n"
    "- Compare modeled fire intensity against regional terrain and vegetation layers for decision support.\n"
    "- Prioritize prevention corridors and emergency response staging using hazard overlays."
)
