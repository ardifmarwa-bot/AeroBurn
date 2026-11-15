import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from gtts import gTTS
import json
import os

# Control room page configuration
st.set_page_config(page_title="Airoburn Engineering Command Center", layout="wide", page_icon="🔥")
pio.templates.default = "plotly_dark"

# --- VISUAL IDENTITY: AIROBURN ENGINEERING / AEROSPACE COMMAND CENTER ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@500;600;700;800&display=swap');
    :root {
        --cyan: #37e0ff; --cyan-soft: #9bdfff; --orange: #ff9a3d;
        --text: #dbe8ff; --muted: #8fa6c6;
        --border: rgba(110,190,255,.28);
    }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp {
        color: var(--text);
        background:
            radial-gradient(ellipse at 10% 18%, rgba(255,154,61,.12), transparent 25%),
            radial-gradient(ellipse at 80% 0%, rgba(55,224,255,.14), transparent 34%),
            linear-gradient(145deg, #02040a 0%, #061126 52%, #02040a 100%);
    }
    .stApp::before {
        content: ""; position: fixed; inset: 0; pointer-events: none; opacity: .25;
        background-image: linear-gradient(rgba(55,224,255,.035) 1px, transparent 1px),
            linear-gradient(90deg, rgba(55,224,255,.035) 1px, transparent 1px);
        background-size: 46px 46px;
    }
    [data-testid="stHeader"] { background: rgba(2,4,10,.72); }
    .block-container { max-width: 1680px; padding-top: 2rem; padding-bottom: 3rem; }
    h1, h2, h3 { color: #f2f8ff !important; }
    h1 {
        font-family: 'Orbitron','Inter',sans-serif !important;
        letter-spacing: .16em; font-weight: 500 !important;
        text-shadow: 0 0 28px rgba(55,224,255,.42);
    }
    h2 { border-left: 2px solid var(--cyan); padding-left: .7rem; }
    h3 { color: var(--cyan-soft) !important; letter-spacing: .04em; }
    p, label, [data-testid="stMarkdownContainer"] { color: var(--text); }
    [data-testid="stCaptionContainer"], .stCaption { color: var(--muted) !important; }
    hr {
        border: 0; height: 1px;
        background: linear-gradient(90deg, transparent, var(--cyan), transparent);
        opacity: .55; margin: 1.25rem 0;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(8,24,48,.88), rgba(3,10,24,.92));
        border: 1px solid var(--border); border-radius: 3px; padding: 14px 16px;
        box-shadow: 0 0 22px rgba(55,224,255,.07), inset 0 1px 0 rgba(255,255,255,.04);
        min-height: 105px;
    }
    [data-testid="stMetricLabel"] { color: var(--muted) !important; }
    [data-testid="stMetricValue"] { color: #f2f8ff !important; text-shadow: 0 0 14px rgba(55,224,255,.3); }
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stRadio"] div[role="radiogroup"] {
        background: rgba(4,10,24,.78); border: 1px solid var(--border); border-radius: 3px;
    }
    [data-testid="stRadio"] div[role="radiogroup"] { padding: 8px 12px; gap: .5rem; }
    [data-testid="stCheckbox"] {
        background: rgba(4,10,24,.65); border: 1px solid var(--border);
        border-radius: 3px; padding: 6px 10px;
    }
    .stButton > button {
        border: 1px solid rgba(55,224,255,.7); border-radius: 3px;
        color: #eaf8ff; background: rgba(55,224,255,.08);
        font-weight: 700; min-height: 2.7rem; transition: .25s;
    }
    .stButton > button:hover {
        border-color: var(--orange); color: white;
        background: rgba(255,154,61,.14); box-shadow: 0 0 20px rgba(255,154,61,.2);
    }
    .stButton > button[kind="primary"] {
        border-color: rgba(255,154,61,.8); background: rgba(255,96,40,.18);
    }
    [data-testid="stPlotlyChart"] {
        background: rgba(3,10,24,.72); border: 1px solid var(--border);
        border-radius: 3px; padding: 5px; box-shadow: inset 0 0 24px rgba(55,224,255,.05);
    }
    [data-testid="stAlert"], [data-testid="stIFrame"], [data-testid="stAudio"] {
        border-radius: 3px; border: 1px solid var(--border);
        background: rgba(4,10,24,.78);
    }
    .sf-landing {
        position: relative; min-height: 48vh; margin: 3vh auto 1.5rem; padding: 8vh 2rem 5vh;
        overflow: hidden; text-align: center; border: 1px solid rgba(110,190,255,.25);
        background: radial-gradient(circle at 50% 55%, rgba(55,224,255,.12), transparent 34%),
            linear-gradient(160deg, rgba(4,14,32,.88), rgba(2,4,10,.96));
        box-shadow: inset 0 0 80px rgba(55,224,255,.06), 0 0 35px rgba(55,224,255,.08);
    }
    .sf-landing:before, .sf-landing:after {
        content: ""; position: absolute; left: 8%; right: 8%; height: 1px;
        background: linear-gradient(90deg, transparent, var(--cyan), transparent); opacity: .7;
    }
    .sf-landing:before { top: 18%; } .sf-landing:after { bottom: 18%; }
    .landing-kicker { color: var(--cyan); font-size: .72rem; letter-spacing: .3em; font-weight: 700; }
    .sf-landing h1 {
        position: relative; margin: 3rem 0 .4rem; font-size: clamp(2.5rem, 8vw, 6.5rem) !important;
        letter-spacing: .3em !important; font-weight: 400 !important;
    }
    .sf-landing h1 span { color: var(--cyan); }
    .sf-landing p { color: var(--cyan); letter-spacing: .45em; font-size: .85rem; }
    .landing-scan {
        position: absolute; left: 15%; right: 15%; top: 52%; height: 2px;
        background: linear-gradient(90deg, transparent, var(--orange), transparent);
        box-shadow: 0 0 18px var(--orange); opacity: .65;
    }
    .landing-intro { margin: 1.25rem 0 .8rem; color: var(--muted); text-align: center; letter-spacing: .12em; }
    .mode-ribbon {
        padding: .8rem 1rem; color: var(--cyan); border-left: 2px solid var(--cyan);
        background: rgba(4,10,24,.7); letter-spacing: .14em; font-size: .8rem;
    }
    @media (max-width: 700px) {
        .sf-landing { min-height: 40vh; padding-top: 5vh; }
        .sf-landing h1 { letter-spacing: .15em !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- DYNAMIC DATABASE LOADING ---
@st.cache_data
def load_nasa_data():
    if os.path.exists('nasa_data.csv'):
        df = pd.read_csv('nasa_data.csv', header=None)
        df = df.fillna(0.0)
        return df
    return None

df_nasa = load_nasa_data()


def build_airoburn_simulation(do: float, hot_flame: float, cool_flame: float, gravity: float, risk: int, status: str) -> str:
    """Render the interactive Airoburn Engineering command interface in a Streamlit iframe."""
    payload = json.dumps({
        "do": round(do, 3),
        "hot": round(hot_flame, 3),
        "cool": round(cool_flame, 3),
        "gravity": gravity,
        "risk": risk,
        "status": status,
    })
    return f"""
    <style>
      * {{ box-sizing: border-box; }}
      html, body {{ margin: 0; height: 100%; overflow: hidden; background: #02040a; }}
      body {{ color: #dbe8ff; font: 13px/1.45 Segoe UI, system-ui, sans-serif; }}
      button, input {{ font: inherit; color: inherit; }}
      .sf {{ position: relative; height: 700px; overflow: hidden; background: #02040a; }}
      #space {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
      .sf:after {{ content: ""; position: absolute; inset: 0; pointer-events: none;
        background: radial-gradient(ellipse at 16% 48%, #ff9a3d30, transparent 30%),
          linear-gradient(90deg, #02040a88, transparent 35%, transparent 70%, #02040a99); }}
      .brand {{ position: absolute; z-index: 2; top: 28px; left: 178px; pointer-events: none; }}
      .brand h1 {{ margin: 0; font: 500 clamp(24px, 4vw, 48px) Orbitron, Segoe UI, sans-serif;
        letter-spacing: .24em; text-shadow: 0 0 30px #37e0ff88; }}
      .brand p {{ margin: 6px 0; color: #37e0ff; letter-spacing: .3em; }}
      .rail {{ position: absolute; z-index: 3; left: 0; top: 0; bottom: 0; width: 150px;
        display: flex; flex-direction: column; justify-content: center; gap: 5px; padding: 10px; }}
      .rail button {{ text-align: left; border: 0; border-left: 2px solid transparent; border-radius: 0;
        padding: 10px; background: #040a1870; cursor: pointer; }}
      .rail button:hover, .rail button.on {{ border-left-color: #37e0ff; background: #37e0ff18; }}
      .panel {{ position: absolute; z-index: 3; right: 14px; top: 18px; width: 270px; padding: 14px;
        background: #040a18c9; border-left: 1px solid #6ebeff55; backdrop-filter: blur(12px); }}
      .panel h3 {{ margin: 0 0 10px; color: #37e0ff; font-weight: 500; letter-spacing: .12em; }}
      .row {{ display: flex; justify-content: space-between; padding: 7px 3px;
        border-bottom: 1px solid #6ebeff1c; }}
      .value {{ color: #ffb875; font-weight: 700; }}
      .alert {{ position: absolute; z-index: 3; left: 170px; bottom: 132px; width: min(390px, 42vw);
        padding: 12px 15px; background: #1e060acc; border-left: 3px solid #ff3b30;
        backdrop-filter: blur(10px); }}
      .alert h3 {{ margin: 0 0 4px; color: #ffb0a7; }}
      .alert p {{ margin: 3px 0; color: #b7c8df; }}
      .assist {{ position: absolute; z-index: 3; left: 170px; right: 300px; bottom: 15px; }}
      .reply {{ margin-bottom: 7px; padding: 9px 12px; background: #040a18cc; border-left: 2px solid #37e0ff; }}
      .assist form {{ display: flex; gap: 7px; }}
      .assist input {{ flex: 1; min-width: 0; padding: 9px 11px; border: 1px solid #6ebeff55;
        border-radius: 2px; background: #050c1ccc; outline: none; }}
      .assist button {{ padding: 8px 14px; border: 1px solid #37e0ff99; background: #37e0ff18;
        cursor: pointer; border-radius: 2px; }}
      .assist button:hover {{ border-color: #ff9a3d; }}
      .tag {{ color: #8fa6c6; font-size: 11px; }}
      @media (max-width: 760px) {{
        .rail {{ width: 94px; }} .brand {{ left: 108px; }} .panel {{ width: 205px; }}
        .alert {{ left: 108px; bottom: 155px; width: 55vw; }} .assist {{ left: 108px; right: 220px; }}
      }}
    </style>
    <div class="sf">
      <canvas id="space"></canvas>
      <div class="brand"><h1>AIROBURN ENGINEERING</h1><p>EXPLORE · PREDICT · PROTECT</p></div>
      <aside class="panel">
        <h3 id="panel-title">LIVE TELEMETRY</h3>
        <div class="row"><span>Droplet core</span><span class="value" id="do">--</span></div>
        <div class="row"><span>Hot flame zone</span><span class="value" id="hot">--</span></div>
        <div class="row"><span>Cool flame signal</span><span class="value" id="cool">--</span></div>
        <div class="row"><span>Gravity field</span><span class="value" id="gravity">--</span></div>
        <div class="row"><span>Risk index</span><span class="value" id="risk">--</span></div>
        <p class="tag" id="source">NASA PSI / local simulation</p>
      </aside>
      <div class="alert"><h3 id="alert-title">COMBUSTION MONITOR</h3>
        <p id="alert-copy">Interactive visualisation active. Click a control channel to inspect the mission.</p></div>
    </div>
    <script>
      const DATA = {payload};
      const canvas = document.getElementById("space"), ctx = canvas.getContext("2d");
      const state = {{time: 0, view: "mission", particles: []}};
      const el = id => document.getElementById(id);
      el("do").textContent = DATA.do.toFixed(3) + " mm";
      el("hot").textContent = DATA.hot.toFixed(3) + " mm";
      el("cool").textContent = DATA.cool.toFixed(3) + " mm";
      el("gravity").textContent = DATA.gravity.toFixed(2) + " G";
      el("risk").textContent = DATA.risk + " / 100";
      el("alert-title").textContent = DATA.status === "NOMINAL" ? "NOMINAL COMBUSTION" : DATA.status;
      el("alert-copy").textContent = DATA.cool > .01 && DATA.hot <= .01
        ? "Cool flame detected. Maintain module isolation and ventilation discipline."
        : "Visual sensor online. Flame response is being monitored continuously.";
      function resize() {{
        const dpr = Math.min(devicePixelRatio || 1, 2), r = canvas.getBoundingClientRect();
        canvas.width = r.width * dpr; canvas.height = r.height * dpr; ctx.setTransform(dpr,0,0,dpr,0,0);
      }}
      function seed() {{
        state.particles = Array.from({{length: 145}}, () => ({{x: Math.random(), y: Math.random(),
          s: Math.random() * 1.8 + .25, a: Math.random() * .75 + .15}}));
      }}
      function flame(x, y, scale, hot, t) {{
        ctx.save(); ctx.translate(x, y); ctx.globalCompositeOperation = "lighter";
        const pulse = 1 + Math.sin(t * 3.2) * .045 + Math.sin(t * 7.1) * .025;
        const outer = ctx.createRadialGradient(0, 0, 4, 0, 0, scale * pulse);
        outer.addColorStop(0, hot ? "#ffedb0cc" : "#b9d8ffbb");
        outer.addColorStop(.28, hot ? "#ff9a3dcc" : "#6b9dff88");
        outer.addColorStop(1, hot ? "#ff3b3000" : "#37e0ff00");
        ctx.fillStyle = outer; ctx.beginPath(); ctx.arc(0, 0, scale * pulse, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = hot ? "#ff9a3d" : "#72b7ff"; ctx.shadowBlur = 28; ctx.shadowColor = ctx.fillStyle;
        ctx.beginPath(); ctx.ellipse(0, 0, scale * .25, scale * .62, Math.sin(t) * .12, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
      }}
      function draw() {{
        const w = canvas.clientWidth, h = canvas.clientHeight; state.time += .016;
        ctx.clearRect(0, 0, w, h); ctx.fillStyle = "#02040a"; ctx.fillRect(0, 0, w, h);
        for (const p of state.particles) {{
          p.y += .00025 * p.s; if (p.y > 1) p.y = 0;
          ctx.fillStyle = `rgba(150,205,255,${{p.a}})`; ctx.fillRect(p.x*w, p.y*h, p.s, p.s);
        }}
        const cx = w * .49, cy = h * .42, size = Math.max(50, Math.min(115, DATA.do * 18));
        ctx.strokeStyle = "#37e0ff22"; ctx.lineWidth = 1;
        for (let r = size * 1.6; r < size * 3.2; r += 24) {{
          ctx.beginPath(); ctx.arc(cx, cy, r + Math.sin(state.time + r) * 2, 0, Math.PI * 2); ctx.stroke();
        }}
        flame(cx, cy, size * 1.45, false, state.time);
        flame(cx, cy + (DATA.gravity ? size * .15 : 0), size * .78, DATA.hot > .01, state.time + 1);
        if (DATA.cool > .01) flame(cx, cy - size * .28, size * .56, false, state.time + 2);
        ctx.fillStyle = "#8fa6c6"; ctx.font = "11px Segoe UI"; ctx.fillText("LIVE VISUAL SENSOR", cx - 60, cy + size * 2.2);
        requestAnimationFrame(draw);
      }}
      window.addEventListener("resize", resize); seed(); resize(); draw();
    </script>
    """

# --- AIROBURN ENGINEERING HOME AND MODE NAVIGATION ---
if "mode" not in st.session_state:
    st.session_state.mode = None

if st.session_state.mode is None:
    st.markdown(
        """
        <div class="sf-landing">
            <div class="landing-kicker">AEROSPACE COMBUSTION INTELLIGENCE</div>
            <h1>AIROBURN <span>ENGINEERING</span></h1>
            <p>EXPLORE · PREDICT · PROTECT</p>
            <div class="landing-scan"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='landing-intro'>Select your operational environment</div>",
        unsafe_allow_html=True,
    )
    mode_space, mode_earth = st.columns(2)
    with mode_space:
        if st.button("🌌  ASTRONAUT MODE", use_container_width=True, type="primary"):
            st.session_state.mode = "space"
            st.rerun()
        st.caption("Onboard intelligent companion · NASA PSI · microgravity combustion")
    with mode_earth:
        if st.button("🌍  EARTH MODE", use_container_width=True):
            st.session_state.mode = "earth"
            st.rerun()
        st.caption("Territorial monitoring · Morocco GIS · wildfire spread")
    st.stop()

mode_space, mode_earth = st.columns([1, 5])
with mode_space:
    if st.button("← Home", use_container_width=True):
        st.session_state.mode = None
        st.rerun()
with mode_earth:
    st.markdown(
        f"<div class='mode-ribbon'>{'🌌 AIROBURN ENGINEERING · ASTRONAUT MODE' if st.session_state.mode == 'space' else '🌍 AIROBURN ENGINEERING · EARTH MODE'}</div>",
        unsafe_allow_html=True,
    )

environment = (
    "🌌 Space (NASA PSI Telemetry)"
    if st.session_state.mode == "space"
    else "🌍 Earth (Morocco GeoPortal GIS)"
)
st.markdown("---")

# =========================================================================
# 🌌 CASE 1: SPACE MISSIONS (NASA)
# =========================================================================
if environment == "🌌 Space (NASA PSI Telemetry)":
    st.header("Orbital Control Room - Microgravity Analysis")
    
    blend_options = {
        "C7 Heptane [ISS Space Experiment]": {"col_idx": 0, "gravity": 0.0},
        "C7 Heptane [Ground Control]": {"col_idx": 4, "gravity": 1.0},
        "C10 Decane [ISS Space Experiment]": {"col_idx": 8, "gravity": 0.0},
        "C10 Decane [Ground Control]": {"col_idx": 12, "gravity": 1.0},
        "C12 Dodecane [ISS Space Experiment]": {"col_idx": 16, "gravity": 0.0}
    }
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("🎛️ Control Panel")
        selected_blend = st.selectbox("Select experiment (Fuel / Gravity)", list(blend_options.keys()))
        
        cfg = blend_options[selected_blend]
        start_col = cfg["col_idx"]
        g_val = cfg["gravity"]
        
        frame = st.slider("Experiment Time Index (Row)", min_value=0, max_value=5, value=0)
        
        Do, Dext_HF, Dext_CF = 4.0, 3.0, 0.0
        if df_nasa is not None:
            try:
                val_do = df_nasa.iloc[frame + 2, start_col + 2]
                val_hf = df_nasa.iloc[frame + 2, start_col + 3]
                val_cf = df_nasa.iloc[frame + 2, start_col + 4]
                
                Do = float(val_do) if pd.notnull(val_do) and str(val_do).strip() != "" else 4.0
                Dext_HF = float(val_hf) if pd.notnull(val_hf) and str(val_hf).strip() != "" else 0.0
                Dext_CF = float(val_cf) if pd.notnull(val_cf) and str(val_cf).strip() != "" else 0.0
            except:
                pass
        
        # Predictive fire risk assessment algorithm
        risk_index = min(max(int((Do * 15) + (Dext_HF * 10) + (Dext_CF * 25)), 5), 100)
        st.metric(label="Prescriptive Fire Risk Index", value=f"{risk_index} / 100")
        
        if risk_index < 45:
            status, status_color = "NOMINAL", "green"
        elif risk_index < 75:
            status, status_color = "MODERATE ALERT", "orange"
        else:
            status, status_color = "CRITICAL ALARM", "red"

    with col_right:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Droplet Core (Do)", f"{Do:.3f} mm")
        kpi2.metric("Hot Flame Zone (HF)", f"{Dext_HF:.3f} mm")
        kpi3.metric("Cool Flame Intensity (CF)", f"{Dext_CF:.3f} mm")
        kpi4.markdown(f"<div style='background-color:{status_color};padding:10px;border-radius:5px;text-align:center;color:white;font-weight:bold;font-size:18px;'>STATUS: {status}</div>", unsafe_allow_html=True)
        
        graph_col, flame_col = st.columns(2)
        
        with graph_col:
            st.markdown("### 📈 Time-Series Telemetry Monitor")
            time_steps = list(range(6))
            fig_lines = go.Figure()
            fig_lines.add_trace(go.Scatter(x=time_steps, y=[3.91, 3.89, 3.61, 3.55, 3.48, 3.34], name="Droplet Size", line=dict(color='green')))
            fig_lines.add_trace(go.Scatter(x=time_steps, y=[3.28, 3.41, 2.83, 2.79, 2.32, 2.10], name="Hot Flame", line=dict(color='red')))
            fig_lines.update_layout(height=280, xaxis_title="Time Node", yaxis_title="Scale (mm)", margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_lines, use_container_width=True)
            
        with flame_col:
            st.markdown("### 🔥 3D Visual Sensor Flux")
            u, v = np.linspace(0, 2 * np.pi, 20), np.linspace(0, np.pi, 20)
            etirement = 1.0 + (g_val * 2.5)
            render_size = Do if Do > 0.1 else 0.5
            x_mesh = render_size * np.outer(np.cos(u), np.sin(v))
            y_mesh = render_size * np.outer(np.sin(u), np.sin(v))
            z_mesh = render_size * np.outer(np.ones(np.size(u)), np.cos(v)) * etirement
            if g_val > 0: z_mesh += (g_val * render_size)
            
            palette = 'Electric' if g_val == 0 else 'YlOrRd'
            fig_3d = go.Figure(data=[go.Surface(x=x_mesh, y=y_mesh, z=z_mesh, colorscale=palette, showscale=False)])
            fig_3d.update_layout(scene=dict(xaxis=dict(range=[-6,6]), yaxis=dict(range=[-6,6]), zaxis=dict(range=[-4,12])), height=280, margin=dict(l=0,r=0,b=0,t=0))
            st.plotly_chart(fig_3d, use_container_width=True)

    st.components.v1.html(
        build_airoburn_simulation(Do, Dext_HF, Dext_CF, g_val, risk_index, status),
        height=700,
        scrolling=False,
    )

    # --- SPACE AUDIO SAFETY ---
    st.markdown("---")
    st.subheader("🎙️ Crisis Voice Interface (On Demand)")
    st.write("Click the button below to query the NASA physics-based safety assistant.")
    btn_vocal_space = st.button("🚨 Query the ISS Emergency Copilot", type="primary")
    
    if btn_vocal_space:
        if Dext_CF > 0.01 and Dext_HF <= 0.01:
            msg_space = "Critical alert. Invisible cool flame combustion detected. Maintain module isolation, do not remove masks, and keep ventilation deactivated."
        elif status == "CRITICAL ALARM":
            msg_space = "Emergency protocol engaged. Hot flame expansion is critical. Restrict local cabin oxygen immediately."
        else:
            msg_space = f"Telemetry nominal. Droplet core is stable at {Do:.2f} millimeters. No immediate fire hazards detected."
            
        st.markdown(f"**🤖 Space Audio Dispatch:** *\"{msg_space}\"*")
        tts = gTTS(text=msg_space, lang='en', slow=False)
        tts.save("space.mp3")
        st.audio("space.mp3", format="audio/mp3", autoplay=True)

# =========================================================================
# 🌍 CASE 2: EARTH OPERATIONS (MOROCCO)
# =========================================================================
else:
    st.markdown(
        """
        <div class="sf-landing" style="min-height:auto;text-align:left;padding:1.5rem 1.7rem;margin:0 0 1.2rem;">
            <div class="landing-kicker">GEOSPATIAL FIRE INTELLIGENCE · MOROCCO</div>
            <h2 style="margin:.55rem 0 .25rem;border:0;padding:0;">EARTH OPERATIONS CENTER</h2>
            <p style="margin:0;color:#8fa6c6;letter-spacing:.08em;">
                Rif monitoring, NASA thermal anomalies, and decision support for Civil Protection.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    col_map, col_ctrl = st.columns(2)
    
    with col_map:
        st.markdown("### 🗺️ Live GIS Tactical Intelligence Map")
        st.write("Native ArcGIS embedded component: automatic synchronization of NASA heat anomalies.")
        
        # ORIGINAL EMBEDDED CODE PRESERVED 100%
        esri_html_component = """
        <script type="module" src="https://js.arcgis.com/5.2/embeddable-components/"></script>
        <arcgis-embedded-map 
            style="height:550px; width:100%; max-width:100%; border-radius:8px;" 
            item-id="56d4c16cf5b84203be3d88b557657538" 
            theme="light" 
            time-bar-enabled 
            center="-9.724048956590583,29.476239100014613" 
            scale="18489297.737236" 
            portal-url="https://africageoportal.maps.arcgis.com">
        </arcgis-embedded-map>
        """
        st.components.v1.html(esri_html_component, height=580, scrolling=False)
        
    with col_ctrl:
        # INTERACTIVE LEGEND DISPLAYED BESIDE THE MAP
        st.markdown("### 🔑 GIS Tactical System Legend")
        st.info("🟩 **Green Zones (Forest Areas):** Dense forest vegetation cover in the Moroccan Rif (Chefchaouen, Larache), providing flammable biomass.")
        st.error("🔴 **Red Points (NASA Sensors):** Real-time thermal anomalies detected by NASA MODIS/VIIRS satellites, identifying fire ignition points.")
        
        st.markdown("---")
        st.subheader("📋 Environmental Vulnerability Analysis")
        region = st.selectbox("Target Forest Area (Rif)", ["Chefchaouen (High Risk)", "Larache (Arid Zones)", "Tetouan / Tangier"])
        vent_chergui = st.checkbox("Active Easterly Wind Configuration (Chergui)", value=True)
        temp_sol = st.slider("Measured Ground Ambient Temperature (°C)", 25, 48, 42)
        
        fwi_base = (temp_sol * 1.8) + (20 if vent_chergui else 0)
        fwi_index = min(max(int(fwi_base), 10), 100)
        
        st.metric("Calibrated Land Spread Rate Index", f"{fwi_index} / 100")
        
        st.markdown("---")
        st.write("Click the button below to query crisis recommendations for Moroccan territory.")
        btn_vocal_earth = st.button("🎙️ Query Morocco Civil Protection", type="secondary")
        
        if btn_vocal_earth:
            if fwi_index > 80:
                msg_earth = f"Red alert for the {region} region. Extreme spread risk detected under Chergui wind conditions. Immediate deployment of water bombers recommended."
            else:
                msg_earth = f"Conditions under monitoring for the {region} province. Moderate risk. Keep ground forest patrols active."
                
            st.markdown(f"**🤖 Civil Protection Radio Dispatch:** *\"{msg_earth}\"*")