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


def generate_flame_points(gravity_level: float, points: int = 2500, seed: int = 42):
    rng = np.random.default_rng(seed)

    if gravity_level <= 0.2:
        phi = rng.uniform(0, np.pi, points)
        theta = rng.uniform(0, 2 * np.pi, points)
        radius = np.clip(rng.normal(0.65, 0.18, points), 0.05, 1.0)
        x = radius * np.sin(phi) * np.cos(theta)
        y = radius * np.sin(phi) * np.sin(theta)
        z = radius * np.cos(phi)
    else:
        z = rng.uniform(-0.3, 1.8, points)
        radial_scale = np.clip(0.6 - (z + 0.3) * 0.22, 0.08, 0.6)
        radial_noise = np.abs(rng.normal(0.0, radial_scale, points))
        theta = rng.uniform(0, 2 * np.pi, points)
        x = radial_noise * np.cos(theta)
        y = radial_noise * np.sin(theta)

    intensity = np.clip(1.0 - np.sqrt(x**2 + y**2 + (z * 0.7) ** 2), 0, 1)
    return x, y, z, intensity


def build_flame_figure(gravity_level: float):
    x, y, z, intensity = generate_flame_points(gravity_level)

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="markers",
                marker=dict(
                    size=3,
                    color=intensity,
                    colorscale="Hot",
                    opacity=0.75,
                    colorbar=dict(title="Flame intensity"),
                ),
                name="Flame",
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            bgcolor="rgba(0,0,0,0)",
        ),
        title=(
            "Microgravity: Spherical Combustion"
            if gravity_level <= 0.2
            else "Earth Gravity: Elongated Flame"
        ),
    )
    return fig


def simulate_sensor_series(gravity_level: float, samples: int = 60):
    now = time.time()
    timeline = np.linspace(now - samples + 1, now, samples)

    gravity_base = gravity_level
    oxygen_base = 20.9 - 0.15 * gravity_level
    pressure_base = 101.3 + 1.4 * gravity_level

    oxygen = oxygen_base + 0.35 * np.sin(timeline / 4) + np.random.normal(0, 0.05, samples)
    pressure = pressure_base + 0.55 * np.cos(timeline / 7) + np.random.normal(0, 0.08, samples)
    gravity = gravity_base + 0.015 * np.sin(timeline / 6) + np.random.normal(0, 0.003, samples)

    readable_time = [datetime.fromtimestamp(t).strftime("%H:%M:%S") for t in timeline]
    return readable_time, oxygen, pressure, gravity


with st.sidebar:
    st.header("Simulation Controls")
    gravity_level = st.slider("Ambient gravity (g)", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    st.button("Refresh sensor simulation")

left_col, right_col = st.columns([1.2, 1])

with left_col:
    st.subheader("3D Flame Visualization")
    st.plotly_chart(build_flame_figure(gravity_level), use_container_width=True)

with right_col:
    st.subheader("Predictive Fire Safety Dashboard")
    timestamps, oxygen, pressure, gravity = simulate_sensor_series(gravity_level)

    latest_oxygen = float(oxygen[-1])
    latest_pressure = float(pressure[-1])
    latest_gravity = float(gravity[-1])

    c1, c2, c3 = st.columns(3)
    c1.metric("Oxygen (%)", f"{latest_oxygen:.2f}")
    c2.metric("Pressure (kPa)", f"{latest_pressure:.2f}")
    c3.metric("Gravity (g)", f"{latest_gravity:.3f}")

    st.line_chart(
        {
            "time": timestamps,
            "oxygen_%": oxygen,
            "pressure_kPa": pressure,
            "gravity_g": gravity,
        },
        x="time",
    )

    risk_score = (
        max(0.0, (20.6 - latest_oxygen) * 10)
        + max(0.0, abs(latest_pressure - 101.3) * 1.4)
        + max(0.0, abs(latest_gravity - gravity_level) * 100)
    )

    if risk_score < 5:
        st.success("Predicted risk: LOW")
    elif risk_score < 12:
        st.warning("Predicted risk: MODERATE")
    else:
        st.error("Predicted risk: HIGH")

st.info("Use the gravity slider to compare spherical microgravity flames and elongated Earth-gravity flames.")
