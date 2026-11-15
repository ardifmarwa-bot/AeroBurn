import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from gtts import gTTS
import os

# Configuration de la page de la salle de contrôle
st.set_page_config(page_title="AeroBurn Command Center", layout="wide", page_icon="🔥")


# Thème sombre pour les visualisations Plotly (sans modifier les données ni les calculs)
pio.templates.default = "plotly_dark"

# --- IDENTITÉ VISUELLE AEROBURN : DARK AEROSPACE COMMAND CENTER ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@500;600;700;800&display=swap');
    :root {
        --ab-blue: #19bfff; --ab-blue-soft: #68d5ff; --ab-red: #ff405b;
        --ab-text: #eaf4ff; --ab-muted: #91a8c2;
        --ab-border: rgba(39, 166, 255, 0.32);
    }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp {
        color: var(--ab-text);
        background:
            radial-gradient(ellipse at 12% 0%, rgba(0,126,255,.15), transparent 34%),
            radial-gradient(ellipse at 92% 18%, rgba(0,198,255,.09), transparent 28%),
            linear-gradient(145deg, #030812 0%, #071426 48%, #040a14 100%);
    }
    [data-testid="stHeader"] { background: rgba(3,9,19,.72); }
    .block-container { max-width: 1680px; padding-top: 2.1rem; padding-bottom: 3rem; }
    h1, h2, h3 { color: #f2f8ff !important; letter-spacing: -.025em; }
    h1 {
        font-family: 'Orbitron','Inter',sans-serif !important;
        font-size: clamp(1.8rem,3vw,2.7rem) !important;
        font-weight: 700 !important;
        text-shadow: 0 0 24px rgba(25,191,255,.25);
    }
    h2 {
        font-size: 1.35rem !important; border-left: 3px solid var(--ab-blue);
        padding-left: .7rem; margin-top: 1rem !important;
    }
    h3 { font-size: 1.05rem !important; color: var(--ab-blue-soft) !important; }
    p, label, [data-testid="stMarkdownContainer"] { color: #d4e3f5; }
    [data-testid="stCaptionContainer"], .stCaption { color: var(--ab-muted) !important; }
    hr {
        border: 0; height: 1px;
        background: linear-gradient(90deg,transparent,rgba(25,191,255,.65),rgba(25,191,255,.08),transparent);
        margin: 1.35rem 0;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg,rgba(13,35,61,.92),rgba(5,17,32,.92));
        border: 1px solid var(--ab-border); border-radius: 13px; padding: 15px 17px;
        box-shadow: 0 0 18px rgba(0,153,255,.07), inset 0 1px 0 rgba(255,255,255,.035);
        min-height: 112px;
    }
    [data-testid="stMetricLabel"] { color: #9eb8d3 !important; font-size: .82rem !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] { color: #f3f9ff !important; font-weight: 800 !important; text-shadow: 0 0 14px rgba(25,191,255,.18); }
    [data-testid="stMetricDelta"] { font-size: .78rem !important; }
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stMultiSelect"] > div > div,
    [data-testid="stTextInput"] > div > div {
        background: rgba(8,23,41,.92); border: 1px solid rgba(65,157,222,.42); border-radius: 10px;
    }
    [data-testid="stSelectbox"] label, [data-testid="stSlider"] label,
    [data-testid="stCheckbox"] label, [data-testid="stRadio"] label {
        color: #cfe4f8 !important; font-weight: 600;
    }
    [data-testid="stRadio"] div[role="radiogroup"] {
        gap: .55rem; background: rgba(7,22,40,.72); border: 1px solid var(--ab-border);
        border-radius: 13px; padding: 10px 14px;
    }
    [data-testid="stCheckbox"] {
        background: rgba(10,29,49,.65); border: 1px solid rgba(65,157,222,.22);
        border-radius: 9px; padding: 7px 10px;
    }
    .stButton > button {
        border: 1px solid rgba(25,191,255,.72); border-radius: 10px; color: #eaf8ff;
        background: linear-gradient(110deg,rgba(0,132,220,.28),rgba(0,65,116,.48));
        font-weight: 700; min-height: 2.8rem; box-shadow: 0 0 16px rgba(0,153,255,.12);
        transition: all .2s ease;
    }
    .stButton > button:hover {
        color: white; border-color: #7cddff;
        background: linear-gradient(110deg,rgba(0,164,255,.48),rgba(0,82,145,.62));
        box-shadow: 0 0 22px rgba(25,191,255,.28); transform: translateY(-1px);
    }
    .stButton > button[kind="primary"] {
        border-color: rgba(255,64,91,.8);
        background: linear-gradient(110deg,rgba(185,24,55,.78),rgba(91,13,38,.88));
        box-shadow: 0 0 18px rgba(255,64,91,.17);
    }
    [data-testid="stPlotlyChart"] {
        background: rgba(6,18,33,.78); border: 1px solid rgba(35,145,220,.25);
        border-radius: 14px; padding: 5px; box-shadow: inset 0 0 24px rgba(0,119,220,.045);
    }
    [data-testid="stAlert"] {
        border-radius: 12px; border: 1px solid rgba(65,157,222,.28);
        background: rgba(10,28,48,.84);
    }
    [data-testid="stIFrame"] {
        border: 1px solid rgba(25,191,255,.48); border-radius: 13px;
        overflow: hidden; box-shadow: 0 0 22px rgba(0,153,255,.13);
    }
    [data-testid="stAudio"] {
        border: 1px solid var(--ab-border); border-radius: 12px;
        background: rgba(7,22,40,.8); padding: 7px;
    }
    @media (max-width: 900px) {
        .block-container { padding: 1.2rem 1rem 2rem; }
        h1 { font-size: 1.65rem !important; }
        [data-testid="stMetric"] { padding: 11px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- CHARGEMENT DE LA BASE DE DONNÉES DYNAMIQUE ---
@st.cache_data
def load_nasa_data():
    if os.path.exists('nasa_data.csv'):
        df = pd.read_csv('nasa_data.csv', header=None)
        df = df.fillna(0.0)
        return df
    return None

df_nasa = load_nasa_data()

# --- INTERFACE ET NAVIGATION ---
st.markdown(
    """
    <div style="padding:1.25rem 1.5rem 1.15rem; margin:0 0 1.1rem 0;
        border:1px solid rgba(25,191,255,.38); border-radius:16px;
        background:linear-gradient(105deg,rgba(8,28,51,.96),rgba(5,14,29,.92) 58%,rgba(9,35,57,.82));
        box-shadow:0 0 28px rgba(0,153,255,.10),inset 0 1px 0 rgba(255,255,255,.04);">
        <div style="font-family:Inter,sans-serif;font-size:.72rem;letter-spacing:.22em;
            color:#54cfff;font-weight:800;margin-bottom:.45rem;">
            AEROSPACE • COMBUSTION INTELLIGENCE • GEOSPATIAL MONITORING
        </div>
        <div style="font-family:Orbitron,Inter,sans-serif;font-size:clamp(1.55rem,3vw,2.45rem);
            line-height:1.2;font-weight:800;color:#f2f8ff;text-shadow:0 0 22px rgba(25,191,255,.22);">
            AEROBURN <span style="color:#24bfff;">COMMAND CENTER</span>
        </div>
        <div style="margin-top:.55rem;color:#9eb8d3;font-size:.92rem;">
            Système d'Aide à la Décision Spatio-Terrestre — NASA PSI &amp; Esri SIG
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Sélection de l'environnement de crise par l'utilisateur
environnement = st.radio("Sélectionnez l'environnement opérationnel :", ["🌌 Espace (NASA PSI Telemetry)", "🌍 Terre (Morocco GeoPortal SIG)"], horizontal=True)

st.markdown("---")

# =========================================================================
# 🌌 CAS 1 : LES MISSIONS SPATIALES (NASA)
# =========================================================================
if environnement == "🌌 Espace (NASA PSI Telemetry)":
    st.header("Salle de Contrôle Orbitale - Analyse Microgravité")
    
    blend_options = {
        "C7 Heptane [ISS Space Experiment]": {"col_idx": 0, "gravity": 0.0},
        "C7 Heptane [Ground Control]": {"col_idx": 4, "gravity": 1.0},
        "C10 Decane [ISS Space Experiment]": {"col_idx": 8, "gravity": 0.0},
        "C10 Decane [Ground Control]": {"col_idx": 12, "gravity": 1.0},
        "C12 Dodecane [ISS Space Experiment]": {"col_idx": 16, "gravity": 0.0}
    }
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("🎛️ Panel de Contrôle")
        selected_blend = st.selectbox("Sélectionner l'expérience (Carburant / Gravité)", list(blend_options.keys()))
        
        cfg = blend_options[selected_blend]
        start_col = cfg["col_idx"]
        g_val = cfg["gravity"]
        
        frame = st.slider("Index Temporel de l'Expérience (Ligne)", min_value=0, max_value=5, value=0)
        
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
        
        # Algorithme prédictif d'évaluation du risque d'incendie
        risk_index = min(max(int((Do * 15) + (Dext_HF * 10) + (Dext_CF * 25)), 5), 100)
        st.metric(label="Indice Prescriptif de Risque Incendie", value=f"{risk_index} / 100")
        
        if risk_index < 45:
            status, status_color = "NOMINAL", "green"
        elif risk_index < 75:
            status, status_color = "ALERTE MODÉRÉE", "orange"
        else:
            status, status_color = "ALARME CRITIQUE", "red"

    with col_right:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Cœur de Goutte (Do)", f"{Do:.3f} mm")
        kpi2.metric("Zone Flamme Chaude (HF)", f"{Dext_HF:.3f} mm")
        kpi3.metric("Intensité Flamme Froide (CF)", f"{Dext_CF:.3f} mm")
        kpi4.markdown(f"<div style='background-color:{status_color};padding:10px;border-radius:5px;text-align:center;color:white;font-weight:bold;font-size:18px;'>STATUT : {status}</div>", unsafe_allow_html=True)
        
        graph_col, flame_col = st.columns(2)
        
        with graph_col:
            st.markdown("### 📈 Moniteur de Télémesure Temporelle")
            time_steps = list(range(6))
            fig_lines = go.Figure()
            fig_lines.add_trace(go.Scatter(x=time_steps, y=[3.91, 3.89, 3.61, 3.55, 3.48, 3.34], name="Taille Goutte", line=dict(color='green')))
            fig_lines.add_trace(go.Scatter(x=time_steps, y=[3.28, 3.41, 2.83, 2.79, 2.32, 2.10], name="Flamme Chaude", line=dict(color='red')))
            fig_lines.update_layout(height=280, xaxis_title="Nœud Chronologique", yaxis_title="Échelle (mm)", margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_lines, use_container_width=True)
            
        with flame_col:
            st.markdown("### 🔥 Flux du Capteur Visuel 3D")
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

    # --- SÉCURITÉ AUDIO SPATIALE ---
    st.markdown("---")
    st.subheader("🎙️ Interface Vocale de Crise (À la demande)")
    st.write("Cliquez sur le bouton ci-dessous pour interroger l'assistant de sécurité basé sur la physique de la NASA.")
    btn_vocal_space = st.button("🚨 Interroger le copilote d'urgence de l'ISS", type="primary")
    
    if btn_vocal_space:
        if Dext_CF > 0.01 and Dext_HF <= 0.01:
            msg_space = "Critical alert. Invisible cool flame combustion detected. Maintain module isolation, do not remove masks, and keep ventilation deactivated."
        elif status == "ALARME CRITIQUE":
            msg_space = "Emergency protocol engaged. Hot flame expansion is critical. Restrict local cabin oxygen immediately."
        else:
            msg_space = f"Telemetry nominal. Droplet core is stable at {Do:.2f} millimeters. No immediate fire hazards detected."
            
        st.markdown(f"**🤖 Dispatch Audio Spatial :** *\"{msg_space}\"*")
        tts = gTTS(text=msg_space, lang='en', slow=False)
        tts.save("space.mp3")
        st.audio("space.mp3", format="audio/mp3", autoplay=True)

# =========================================================================
# 🌍 CAS 2 : LA PARTIE TERRESTRE (MAROC)
# =========================================================================
else:
    st.header("🌍 Extension Terrestre : Gestion des Risques dans le Rif (Maroc)")
    
    col_map, col_ctrl = st.columns(2)
    
    with col_map:
        st.markdown("### 🗺️ Carte d'Intelligence Tactique SIG En Direct")
        st.write("Composant embarqué natif ArcGIS : Synchronisation automatique des anomalies de chaleur de la NASA.")
        
        # VOTRE CODE EMEDDED D'ORIGINE CONSERVÉ À 100%
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
        # LÉGENDE INTERACTIVE PLACÉE PROPREMENT JUSTE À CÔTÉ DE LA CARTE
        st.markdown("### 🔑 Légende Tactique du Système SIG")
        st.info("🟩 **Zones Vertes (Massifs Forestiers) :** Couverture végétale forestière dense du Rif marocain (Chefchaouen, Larache) constituant la biomasse inflammable de combustible.")
        st.error("🔴 **Points Rouges (Capteurs NASA) :** Anomalies thermiques détectées en temps réel par les satellites MODIS/VIIRS de la NASA, identifiant les départs de feux.")
        
        st.markdown("---")
        st.subheader("📋 Analyseurs de Vulnérabilité Environnementale")
        region = st.selectbox("Zone Forestière Ciblée (Rif)", ["Chefchaouen (Haut Risque)", "Larache (Zones Arides)", "Tétouan / Tanger"])
        vent_chergui = st.checkbox("Configuration Vent d'Est (Chergui) Actif", value=True)
        temp_sol = st.slider("Température Ambiante Mesurée au Sol (°C)", 25, 48, 42)
        
        fwi_base = (temp_sol * 1.8) + (20 if vent_chergui else 0)
        fwi_index = min(max(int(fwi_base), 10), 100)
        
        st.metric("Indice de Vitesse de Propagation Terrestre Calibré", f"{fwi_index} / 100")
        
        st.markdown("---")
        st.write("Cliquez sur le bouton ci-dessous pour interroger les recommandations de crise pour le territoire marocain.")
        btn_vocal_earth = st.button("🎙️ Interroger la Protection Civile du Maroc", type="secondary")
        
        if btn_vocal_earth:
            if fwi_index > 80:
                msg_earth = f"Alerte rouge pour la région de {region}. Risque de propagation extrême détecté sous configuration de vent Chergui. Déploiement immédiat des Canadairs recommandé."
            else:
                msg_earth = f"Conditions sous surveillance pour la province de {region}. Risque modéré. Maintenir les patrouilles forestières au sol."
                
            st.markdown(f"**🤖 Dispatch Radio Sécurité Civile :** *\"{msg_earth}\"*")
