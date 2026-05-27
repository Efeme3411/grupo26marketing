"""
Presentación Streamlit — Trabajo 2 AEM Starbucks
Universidad de Concepción · 2026-1 · Prof. Juan Carlos Caro

Ejecutar:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="Starbucks América — Segmentación",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta Starbucks
GREEN_DARK   = "#1e3932" # Very deep forest green
GREEN_LIGHT  = "#006241" # Rich house green
GOLD         = "#cba258" # Warm accent gold
ACCENT_RED   = "#a6192e" # Crimson red for alerts/dormidos
NEUTRAL      = "#2d2926" # Off-black/Charcoal
BG_CREAM     = "#f9f8f6" # Fresh cream background

PALETA_RFM = {
    "Dormidos":          ACCENT_RED,
    "Regulares Activos": GOLD,
    "Leales Premium":    GREEN_LIGHT,
}
PALETA_SOCIO = [GREEN_DARK, GOLD, GREEN_LIGHT]

# =========================================================
# ESTILOS
# =========================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Typography and Contrast Control */
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Inter', sans-serif;
        color: {NEUTRAL};
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Playfair Display', serif;
        color: {GREEN_LIGHT} !important;
        font-weight: 800;
    }}
    
    h1 {{
        letter-spacing: -1px;
    }}
    
    /* Main container styling */
    .stApp {{
        background: {BG_CREAM};
    }}
    
    .block-container {{
        padding-top: 3rem;
        padding-bottom: 5rem;
        max-width: 1200px;
    }}
    
    /* Sidebar Styling (High contrast, light theme native layout) */
    section[data-testid="stSidebar"] {{
        box-shadow: 4px 0 15px rgba(0,0,0,0.05);
        border-right: 1px solid rgba(0, 0, 0, 0.08);
    }}
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {{
        font-family: 'Playfair Display', serif;
        color: {GREEN_LIGHT} !important;
        font-weight: 700;
    }}
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] li {{
        color: {NEUTRAL} !important;
    }}
    
    section[data-testid="stSidebar"] hr {{
        border-color: rgba(0, 0, 0, 0.1) !important;
    }}

    /* Modern Navigation Tabs inside Sidebar */
    section[data-testid="stSidebar"] .stButton button {{
        border-radius: 8px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: left;
        justify-content: flex-start;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        margin: 4px 0;
        width: 100%;
    }}
    
    /* Secondary (inactive) button in sidebar */
    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"] {{
        background-color: transparent;
        color: {NEUTRAL} !important;
        border: 1px solid rgba(0, 0, 0, 0.08);
    }}
    
    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"]:hover {{
        background-color: rgba(0, 98, 65, 0.08);
        color: {GREEN_LIGHT} !important;
        border-color: {GREEN_LIGHT};
        transform: translateX(4px);
    }}
    
    /* Primary (active) button in sidebar */
    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"] {{
        background-color: {GREEN_LIGHT};
        color: white !important;
        border: 1px solid {GREEN_LIGHT};
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0, 98, 65, 0.15);
    }}
    
    section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"]:hover {{
        background-color: #004d33;
        border-color: #004d33;
        transform: translateX(4px);
    }}
    
    .stButton button {{
        border-radius: 8px;
        font-weight: 500;
    }}
    
    .slide-counter {{
        color: {NEUTRAL};
        text-align: center;
        font-size: 0.9rem;
        font-weight: 500;
        opacity: 0.8;
        background: rgba(0, 0, 0, 0.03);
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }}
    
    /* Metrics & Cards Styling with Soft Shadows and Micro-animations */
    .metric-card {{
        background: white;
        padding: 1.6rem;
        border-radius: 16px;
        border-left: 5px solid {GREEN_LIGHT};
        margin: 0.8rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.06);
    }}
    
    .metric-value {{
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        font-weight: 900;
        color: {GREEN_LIGHT};
        line-height: 1;
    }}
    
    .metric-label {{
        color: {NEUTRAL};
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 0.4rem;
        opacity: 0.8;
    }}
    
    .meta-card {{
        background: white;
        padding: 2rem;
        border-radius: 20px;
        border-top: 6px solid {GREEN_LIGHT};
        margin: 1.2rem 0;
        box-shadow: 0 6px 24px rgba(0,0,0,0.03);
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }}
    
    .meta-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 35px rgba(0,0,0,0.07);
    }}
    
    .meta-card.reactivacion {{
        border-top-color: {ACCENT_RED};
    }}
    
    .meta-card.premium {{
        border-top-color: {GOLD};
    }}
    
    .meta-card h3 {{
        margin-top: 0;
        font-size: 1.5rem;
        font-weight: 800;
    }}
    
    .meta-card .badge {{
        display: inline-block;
        background: {GREEN_LIGHT};
        color: white !important;
        padding: 0.25rem 0.8rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }}
    
    .meta-card .badge.gold {{
        background: {GOLD};
        color: {GREEN_DARK} !important;
    }}
    
    .meta-card .badge.red {{
        background: {ACCENT_RED};
        color: white !important;
    }}
    
    .quote-block {{
        background: white;
        border-left: 6px solid {GOLD};
        padding: 1.6rem 2.2rem;
        margin: 1.8rem 0;
        font-style: italic;
        font-size: 1.1rem;
        color: {NEUTRAL};
        border-radius: 0 16px 16px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.02);
        border: 1px solid rgba(0,0,0,0.04);
        border-left-width: 6px;
    }}
    
    .footer-portada {{
        color: {NEUTRAL};
        opacity: 0.7;
        font-size: 0.9rem;
        line-height: 1.6;
    }}
    
    hr {{
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0));
        margin: 2rem 0;
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATOS (Carga dinámica de outputs con fallback hardcoded)
# =========================================================
clientes_path = Path("outputs/clientes_segmentados.csv")
afinidad_path = Path("outputs/tabla_afinidad.csv")

if clientes_path.exists() and afinidad_path.exists():
    # Carga dinámica desde los archivos exportados por el Notebook Trabajo2_Starbucks_FINAL_2.ipynb
    df_clientes = pd.read_csv(clientes_path)
    
    # Reconstrucción de perfiles RFM
    RFM_PROFILE = df_clientes.groupby(["Cluster_RFM_KM", "Nombre_RFM"]).agg(
        Recency=("Recency", "mean"),
        Frequency=("Frequency", "mean"),
        Monetary=("Monetary", "mean"),
        N_clientes=("customer_id", "count")
    ).reset_index().rename(columns={"Cluster_RFM_KM": "Cluster", "Nombre_RFM": "Nombre"})
    RFM_PROFILE["% mercado"] = (RFM_PROFILE["N_clientes"] / RFM_PROFILE["N_clientes"].sum() * 100).round(1)
    
    # Reconstrucción de perfiles sociodemográficos
    SOCIO_PROFILE = df_clientes.groupby(["Cluster_Socio_LCA", "Nombre_Socio"]).agg(
        N_clientes=("customer_id", "count")
    ).reset_index().rename(columns={"Cluster_Socio_LCA": "Cluster", "Nombre_Socio": "Nombre"})
    SOCIO_PROFILE["% mercado"] = (SOCIO_PROFILE["N_clientes"] / SOCIO_PROFILE["N_clientes"].sum() * 100).round(1)
    
    # Reconstrucción de la matriz cruzada
    MATRIZ = df_clientes.groupby(["Cluster_Socio_LCA", "Cluster_RFM_KM", "Segmento_Nombre"]).agg(
        N=("customer_id", "count"),
        Rec=("Recency", "mean"),
        Freq=("Frequency", "mean"),
        Mon=("Monetary", "mean")
    ).reset_index().rename(columns={"Cluster_Socio_LCA": "Socio", "Cluster_RFM_KM": "RFM", "Segmento_Nombre": "Nombre"})
    MATRIZ["Pct"] = (MATRIZ["N"] / MATRIZ["N"].sum() * 100).round(1)
    
    # Carga de tabla de afinidades
    df_af = pd.read_csv(afinidad_path)
    # Mapeo de códigos (por ejemplo, "1_2" o "Socio_1 · RFM_2") a nombres legibles
    code_to_name = dict(zip(
        df_clientes["Cluster_Socio_LCA"].astype(str) + "_" + df_clientes["Cluster_RFM_KM"].astype(str),
        df_clientes["Segmento_Nombre"]
    ))
    # También mapear formatos como "Socio_1 · RFM_2" si es que así viene en la tabla afinidad
    code_to_name_v2 = dict(zip(
        "Socio_" + df_clientes["Cluster_Socio_LCA"].astype(str) + " · RFM_" + df_clientes["Cluster_RFM_KM"].astype(str),
        df_clientes["Segmento_Nombre"]
    ))
    
    if "Segmento_Final" in df_af.columns:
        df_af = df_af.rename(columns={"Segmento_Final": "Segmento"})
    elif "Unnamed: 0" in df_af.columns:
        df_af = df_af.rename(columns={"Unnamed: 0": "Segmento"})
        
    df_af["Segmento"] = df_af["Segmento"].astype(str).map(lambda x: code_to_name.get(x, code_to_name_v2.get(x, x)))
    
    AFINIDAD = df_af.rename(columns={
        "customer_satisfaction": "satisfaccion",
        "num_customizations": "personalizaciones",
        "fulfillment_time_min": "fulfillment_time",
        "% mercado": "pct"
    })
else:
    # Fallback hardcoded con los nuevos nombres de cluster (FINAL_2)
    RFM_PROFILE = pd.DataFrame({
        "Cluster": [0, 1, 2],
        "Nombre":  ["Dormidos", "Leales Premium", "Regulares Activos"],
        "Recency": [296.92, 70.37, 76.03],
        "Frequency": [4.18, 9.40, 5.52],
        "Monetary": [61.22, 142.75, 80.27],
        "N_clientes": [2344, 5254, 7390],
    })
    RFM_PROFILE["% mercado"] = (RFM_PROFILE["N_clientes"] / RFM_PROFILE["N_clientes"].sum() * 100).round(1)

    SOCIO_PROFILE = pd.DataFrame({
        "Cluster": [0, 1, 2],
        "Nombre":  ["Adultos Drive-Thru", "Jóvenes Digitales", "Tradicionales Presenciales"],
        "N_clientes": [2677, 8951, 3360],
    })
    SOCIO_PROFILE["% mercado"] = (SOCIO_PROFILE["N_clientes"] / SOCIO_PROFILE["N_clientes"].sum() * 100).round(1)

    MATRIZ = pd.DataFrame([
        {"Socio": 1, "RFM": 2, "Nombre": "Jóvenes Digitales · Regulares Activos", "N": 4194, "Pct": 28.0, "Rec": 76.62, "Freq": 5.48, "Mon": 84.15},
        {"Socio": 1, "RFM": 1, "Nombre": "Jóvenes Digitales · Leales Premium",   "N": 3461, "Pct": 23.1, "Rec": 70.98, "Freq": 9.31, "Mon": 147.07},
        {"Socio": 2, "RFM": 2, "Nombre": "Tradicionales Presenciales · Regulares Activos", "N": 1832, "Pct": 12.2, "Rec": 74.72, "Freq": 5.60, "Mon": 74.38},
        {"Socio": 0, "RFM": 2, "Nombre": "Adultos Drive-Thru · Regulares Activos",         "N": 1364, "Pct": 9.1,  "Rec": 75.95, "Freq": 5.55, "Mon": 76.21},
        {"Socio": 1, "RFM": 0, "Nombre": "Jóvenes Digitales · Dormidos",          "N": 1296, "Pct": 8.6,  "Rec": 301.47, "Freq": 4.22, "Mon": 65.94},
        {"Socio": 2, "RFM": 1, "Nombre": "Tradicionales Presenciales · Leales Premium",            "N": 971,  "Pct": 6.5,  "Rec": 67.40, "Freq": 9.61, "Mon": 133.87},
        {"Socio": 0, "RFM": 1, "Nombre": "Adultos Drive-Thru · Leales Premium",            "N": 822,  "Pct": 5.5,  "Rec": 71.33, "Freq": 9.55, "Mon": 135.05},
        {"Socio": 2, "RFM": 0, "Nombre": "Tradicionales Presenciales · Dormidos",                  "N": 557,  "Pct": 3.7,  "Rec": 290.57, "Freq": 4.21, "Mon": 55.72},
        {"Socio": 0, "RFM": 0, "Nombre": "Adultos Drive-Thru · Dormidos",                  "N": 491,  "Pct": 3.3,  "Rec": 292.10, "Freq": 4.02, "Mon": 54.98},
    ])

    AFINIDAD = pd.DataFrame([
        {"Segmento": "Jóvenes Digitales · Regulares Activos", "cart_size": 101.1, "satisfaccion": 100.9, "personalizaciones": 108.8, "fulfillment_time": 101.8, "pct": 28.0},
        {"Segmento": "Jóvenes Digitales · Leales Premium",    "cart_size": 105.2, "satisfaccion": 100.7, "personalizaciones": 108.8, "fulfillment_time": 100.8, "pct": 23.1},
        {"Segmento": "Tradicionales Presenciales · Regulares Activos",          "cart_size": 93.3,  "satisfaccion": 98.9,  "personalizaciones": 83.8,  "fulfillment_time": 91.0,  "pct": 12.2},
        {"Segmento": "Adultos Drive-Thru · Regulares Activos",          "cart_size": 95.4,  "satisfaccion": 98.1,  "personalizaciones": 88.6,  "fulfillment_time": 105.4, "pct": 9.1},
        {"Segmento": "Jóvenes Digitales · Dormidos",           "cart_size": 103.3, "satisfaccion": 101.5, "personalizaciones": 111.4, "fulfillment_time": 103.0, "pct": 8.6},
        {"Segmento": "Tradicionales Presenciales · Leales Premium",             "cart_size": 98.5,  "satisfaccion": 99.2,  "personalizaciones": 86.4,  "fulfillment_time": 93.7,  "pct": 6.5},
        {"Segmento": "Adultos Drive-Thru · Leales Premium",            "cart_size": 98.5,  "satisfaccion": 98.3,  "personalizaciones": 91.2,  "fulfillment_time": 104.4, "pct": 5.5},
        {"Segmento": "Tradicionales Presenciales · Dormidos",                   "cart_size": 93.7,  "satisfaccion": 98.9,  "personalizaciones": 83.1,  "fulfillment_time": 89.1,  "pct": 3.7},
        {"Segmento": "Adultos Drive-Thru · Dormidos",                   "cart_size": 95.5,  "satisfaccion": 98.0,  "personalizaciones": 85.2,  "fulfillment_time": 106.7, "pct": 3.3},
    ])

COMPARACION = pd.DataFrame({
    "Modelo": ["Socio (K-Means)", "Socio (LCA)", "RFM (K-Means)", "RFM (LCA)"],
    "K": [3, 3, 3, 4],
    "Silhouette": [0.151, 0.082, 0.385, 0.337],
    "Davies-Bouldin": [2.364, 3.159, 0.887, 0.755],
    "Entropía": [None, 0.553, None, 0.666],
})


# =========================================================
# NAVEGACIÓN
# =========================================================
SLIDES = [
    "Portada",
    "Contexto del Mercado",
    "El Dataset",
    "Limpieza y Preparación",
    "Metodología — 4 Modelos en Paralelo",
    "Modelo RFM — K-Means",
    "Modelo Sociodemográfico — LCA",
    "Comparación Formal de Modelos",
    "Matriz de Segmentos Cruzados",
    "Caracterización por Afinidad",
    "Visualizaciones Complementarias",
    "Identificación de Mercados Meta",
    "Estrategia de Posicionamiento",
    "Conclusiones y Recomendaciones",
]

if "slide" not in st.session_state:
    st.session_state.slide = 0

def go_to(idx):
    st.session_state.slide = max(0, min(len(SLIDES) - 1, idx))

with st.sidebar:
    st.markdown("### ☕ Navegación")
    st.markdown("---")
    for i, titulo in enumerate(SLIDES):
        is_active = (i == st.session_state.slide)
        marker = "▶" if is_active else "○"
        type_btn = "primary" if is_active else "secondary"
        if st.button(f"{marker}  {i+1}. {titulo}", key=f"nav_{i}", use_container_width=True, type=type_btn):
            go_to(i)
            st.rerun()
    st.markdown("---")
    st.markdown("**AEM · 2026-1**")
    st.markdown("Prof. Juan Carlos Caro")

slide = st.session_state.slide

# =========================================================
# SLIDE 0 — PORTADA
# =========================================================
if slide == 0:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center; padding: 2rem;'>
        <p style='color:{GREEN_LIGHT}; font-weight: 700; letter-spacing: 4px; font-size: 0.95rem; margin-bottom: 0;'>
            MERCADO 2 · STARBUCKS AMÉRICA
        </p>
        <h1 style='font-size: 3.8rem; line-height: 1.1; margin: 1rem 0;'>
            Segmentación,<br>Mercados Meta<br>y Posicionamiento
        </h1>
        <p style='font-size: 1.15rem; color: {NEUTRAL}; max-width: 600px; margin: 1.5rem auto;'>
            Análisis estratégico de marketing para orientar la decisión de apertura
            de nuevas franquicias en Estados Unidos.
        </p>
        <br>
        <hr style='max-width: 200px; margin: 2rem auto;'>
        <p class='footer-portada'>
            Universidad de Concepción · Facultad de Ingeniería<br>
            Departamento de Ingeniería Industrial · 2026-1<br>
            Profesor: Juan Carlos Caro
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# SLIDE 1 — CONTEXTO
# =========================================================
elif slide == 1:
    st.title("Contexto del Mercado")
    st.markdown("&nbsp;")

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown("""
        ### El cliente

        Un **inversionista** evalúa abrir nuevas **franquicias de Starbucks** en
        distintos puntos de Estados Unidos. Necesita orientación basada en datos
        sobre tres preguntas:

        - ¿Quiénes son los clientes de Starbucks en EE.UU.?
        - ¿Cuáles segmentos representan la mejor oportunidad?
        - ¿Cómo debería posicionarse cada nueva franquicia?
        """)

        st.markdown(f"""
        <div class='quote-block'>
        "No basta con saber cuántas tiendas abrir. Necesitamos saber a quién apuntar
        y con qué propuesta de valor diferenciada."
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>~15K</div>
            <div class='metric-label'>Clientes únicos</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'>~150K</div>
            <div class='metric-label'>Órdenes transaccionales</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'>STP</div>
            <div class='metric-label'>Marco estratégico</div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# SLIDE 2 — DATASET
# =========================================================
elif slide == 2:
    st.title("El Dataset")
    st.markdown("Base transaccional consolidada a nivel cliente.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Variables sociodemográficas")
        st.markdown("""
        - `customer_age_group` — Grupo etario
        - `customer_gender` — Género
        - `region` — Región de EE.UU.
        - `store_location_type` — Urbano / Suburbano / Rural
        - `order_channel` — Canal modal (App / Drive / Store)
        - `is_rewards_member` — Membresía Rewards
        """)

    with col2:
        st.markdown("#### Variables de comportamiento (RFM)")
        st.markdown("""
        - `Recency` — Días desde la última compra
        - `Frequency` — N° de órdenes únicas
        - `Monetary` — Gasto total acumulado
        """)
        st.markdown("#### Variables de experiencia (perfilamiento ex-post)")
        st.markdown("""
        - `cart_size` · `customer_satisfaction`
        - `num_customizations` · `fulfillment_time_min`
        """)

    st.markdown("---")
    st.info(
        "**Decisión metodológica:** las variables de experiencia se reservan para "
        "**perfilar** los segmentos ex-post (índices de afinidad), no para definirlos. "
        "Esto evita confundir *quién es el cliente* con *qué experiencia tuvo*."
    )

# =========================================================
# SLIDE 3 — LIMPIEZA
# =========================================================
elif slide == 3:
    st.title("Limpieza y Preparación")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>150K → 15K</div>
            <div class='metric-label'>Agregación transacción → cliente</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>0%</div>
            <div class='metric-label'>Valores faltantes</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>11</div>
            <div class='metric-label'>Variables finales</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("&nbsp;")
    st.markdown("""
    ### Transformaciones aplicadas

    1. **Agregación por `customer_id`** — De ~150K registros transaccionales a ~15K clientes únicos.
    2. **Construcción de RFM** — Recency desde la última orden, Frequency y Monetary acumulados.
    3. **Canal modal por cliente** — `order_channel` se reduce a su moda individual.
    4. **Variables sociodemográficas estables** — Se toma el primer registro (no cambian dentro del cliente).
    5. **Estandarización para modelos** — `StandardScaler` para variables RFM (KMeans) y `LabelEncoder` para categóricas (LCA).
    """)

# =========================================================
# SLIDE 4 — METODOLOGÍA
# =========================================================
elif slide == 4:
    st.title("Metodología — 4 Modelos en Paralelo")
    st.markdown("Se aplican dos técnicas a dos dimensiones para elegir el mejor método en cada una.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class='meta-card'>
            <h3>Dimensión Sociodemográfica</h3>
            <p><strong>Variables:</strong> edad, género, región, tipo de tienda, canal, rewards (5 categóricas + 1 binaria)</p>
            <ul>
                <li><strong>K-Means</strong> sobre matriz one-hot</li>
                <li><strong>LCA (StepMix)</strong> nativo para categóricas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='meta-card premium'>
            <h3>Dimensión RFM</h3>
            <p><strong>Variables:</strong> Recency, Frequency, Monetary (3 continuas)</p>
            <ul>
                <li><strong>K-Means</strong> sobre datos estandarizados</li>
                <li><strong>LCA gaussian_unit</strong> con covarianza esférica</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("&nbsp;")
    st.markdown("""
    ### Criterios de selección de K

    - **K-Means:** Método del codo (inertia) + Silhouette Score
    - **LCA:** BIC mínimo + Entropía relativa cercana a 1
    - **Restricción de contexto:** mínimo K=3 (descartamos K=2 aunque sea óptimo por BIC) para preservar
      riqueza interpretativa al construir mercados meta.
    """)

# =========================================================
# SLIDE 5 — RFM K-MEANS
# =========================================================
elif slide == 5:
    st.title("Modelo RFM — K-Means (K=3)")

    col1, col2 = st.columns([1.2, 1])

    with col1:
        # Tabla con nombres
        tabla = RFM_PROFILE[["Nombre", "Recency", "Frequency", "Monetary", "N_clientes", "% mercado"]].copy()
        tabla.columns = ["Segmento", "Recency (días)", "Frequency", "Monetary ($)", "N clientes", "% mercado"]
        st.dataframe(tabla, hide_index=True, use_container_width=True)

        st.markdown("""
        - **Dormidos** — Casi un año sin comprar. Bajo riesgo de captura pero alto costo de reactivación.
        - **Regulares Activos** — El grueso del negocio. Frecuencia y ticket medios.
        - **Leales Premium** — Recientes, frecuentes, ticket 2× el promedio. El núcleo más valioso.
        """)

    with col2:
        # Donut de % mercado
        fig = px.pie(RFM_PROFILE, values="N_clientes", names="Nombre",
                     hole=0.55,
                     color="Nombre",
                     color_discrete_map=PALETA_RFM)
        fig.update_traces(textinfo="label+percent", textfont_size=12)
        fig.update_layout(
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif"),
            height=350,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Perfil RFM en coordenadas paralelas
    st.markdown("#### Perfil normalizado (coordenadas paralelas)")
    perfil = RFM_PROFILE.copy()
    perfil["Recency_inv"] = (perfil["Recency"].max() - perfil["Recency"]) / (perfil["Recency"].max() - perfil["Recency"].min())
    perfil["Freq_norm"] = (perfil["Frequency"] - perfil["Frequency"].min()) / (perfil["Frequency"].max() - perfil["Frequency"].min())
    perfil["Mon_norm"] = (perfil["Monetary"] - perfil["Monetary"].min()) / (perfil["Monetary"].max() - perfil["Monetary"].min())

    fig2 = go.Figure()
    for _, r in perfil.iterrows():
        fig2.add_trace(go.Scatter(
            x=["Recency (inv.)", "Frequency", "Monetary"],
            y=[r["Recency_inv"], r["Freq_norm"], r["Mon_norm"]],
            mode="lines+markers",
            name=r["Nombre"],
            line=dict(color=PALETA_RFM[r["Nombre"]], width=3),
            marker=dict(size=14),
        ))
    fig2.update_layout(
        yaxis=dict(
            title="Valor normalizado [0,1]", 
            range=[-0.05, 1.1],
            gridcolor="rgba(0,0,0,0.06)",
            zerolinecolor="rgba(0,0,0,0.1)"
        ),
        xaxis=dict(
            gridcolor="rgba(0,0,0,0.06)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        height=350,
        margin=dict(t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
    )
    st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# SLIDE 6 — LCA SOCIO
# =========================================================
elif slide == 6:
    st.title("Modelo Sociodemográfico — LCA (K=3)")
    st.markdown("Latent Class Analysis (StepMix) — método nativo para variables categóricas nominales.")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### Distribución de los clusters")
        tabla = SOCIO_PROFILE[["Nombre", "N_clientes", "% mercado"]].copy()
        tabla.columns = ["Segmento sociodemográfico", "N clientes", "% mercado"]
        st.dataframe(tabla, hide_index=True, use_container_width=True)

        st.markdown(f"""
        <div class='quote-block'>
        El cluster <strong>Jóvenes Digitales</strong> concentra el 60% del mercado.
        La diferenciación entre clientes valiosos y casuales <em>no está</em> en el perfil
        sociodemográfico sino en el patrón de consumo (RFM).
        </div>
        """, unsafe_allow_html=True)

    with col2:
        fig = px.bar(
            SOCIO_PROFILE,
            x="Nombre", y="N_clientes",
            color="Nombre",
            color_discrete_sequence=PALETA_SOCIO,
            text="% mercado",
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif"),
            yaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
            yaxis_title="N° clientes",
            xaxis_title="",
            height=400,
            margin=dict(t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown(f"""
    #### Justificación de la elección de método

    - **5 de 6 variables son categóricas nominales:** LCA es el método nativo, sin necesidad de one-hot.
    - **Entropía relativa = 0.553:** clasificación moderada-buena, refleja solapamiento real esperado en
      datos sociodemográficos de consumidores.
    - **ΔBIC entre K=2 y K=3 marginal:** se prefiere K=3 por riqueza interpretativa.
    """)

# =========================================================
# SLIDE 7 — COMPARACIÓN
# =========================================================
elif slide == 7:
    st.title("Comparación Formal de Modelos")

    st.markdown("Métricas de calidad para los 4 modelos. Se elige el mejor método **por dimensión**.")

    st.dataframe(
        COMPARACION.style.format({
            "Silhouette": "{:.3f}",
            "Davies-Bouldin": "{:.3f}",
            "Entropía": "{:.3f}",
        }, na_rep="—"),
        hide_index=True,
        use_container_width=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class='meta-card'>
            <span class='badge'>Sociodemográfico</span>
            <h3>✅ LCA (StepMix)</h3>
            <ul>
                <li>Nativo para categóricas nominales</li>
                <li>El Silhouette de K-Means se calcula en espacio dummy → comparación sesgada</li>
                <li>Entropía 0.553 indica clasificación realista</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='meta-card premium'>
            <span class='badge gold'>Comportamiento</span>
            <h3>✅ K-Means (RFM)</h3>
            <ul>
                <li>Espacio euclidiano apropiado para 3 variables continuas</li>
                <li>Silhouette 0.385 vs 0.337 (LCA): superior y comparación justa</li>
                <li>Davies-Bouldin 0.887 (&lt;1): buena separación absoluta</li>
                <li>Convergencia limpia, sin warnings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.success(
        "**Variable final sociodemográfica:** `Cluster_Socio_LCA` · "
        "**Variable final comportamental:** `Cluster_RFM_KM`. "
        "Su cruce genera la matriz de 9 segmentos."
    )

# =========================================================
# SLIDE 8 — MATRIZ CRUZADA
# =========================================================
elif slide == 8:
    st.title("Matriz de Segmentos Cruzados")
    st.markdown("3 perfiles sociodemográficos × 3 segmentos RFM = **9 segmentos finales**.")

    # Heatmap interactivo
    pivot = MATRIZ.pivot_table(
        index="Socio", columns="RFM", values="Pct", fill_value=0
    )
    nombres_socio_map = {0: "Adultos Drive-Thru", 1: "Jóvenes Digitales", 2: "Tradicionales Presenciales"}
    nombres_rfm_map   = {0: "Dormidos", 1: "Leales Premium", 2: "Regulares Activos"}
    pivot.index = [nombres_socio_map[i] for i in pivot.index]
    pivot.columns = [nombres_rfm_map[i] for i in pivot.columns]

    fig = px.imshow(
        pivot, text_auto=".1f", aspect="auto",
        color_continuous_scale=[[0, "#fff8e7"], [0.5, GOLD], [1, GREEN_DARK]],
        labels=dict(x="Comportamiento RFM", y="Perfil Sociodemográfico", color="% mercado"),
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        height=400,
        margin=dict(t=30, b=20),
        coloraxis_colorbar=dict(title="% mercado"),
    )
    fig.update_traces(texttemplate="%{z:.1f}%")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Ranking de los 9 segmentos por tamaño")
    fig2 = px.bar(
        MATRIZ.sort_values("Pct", ascending=True),
        x="Pct", y="Nombre", orientation="h",
        color="Pct", color_continuous_scale=[[0, GOLD], [1, GREEN_DARK]],
        text="Pct",
    )
    fig2.update_traces(texttemplate="%{text}%", textposition="outside")
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        xaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
        xaxis_title="% del mercado",
        yaxis_title="",
        height=450,
        margin=dict(t=20, b=20, l=20, r=80),
        showlegend=False,
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# SLIDE 9 — AFINIDADES
# =========================================================
elif slide == 9:
    st.title("Caracterización por Índices de Afinidad")
    st.markdown(
        "Cada celda mide el **índice base 100** del segmento vs el promedio poblacional. "
        "**>100** = comportamiento superior al promedio · **<100** = inferior."
    )

    # Heatmap de afinidades
    af = AFINIDAD.set_index("Segmento")[["cart_size", "satisfaccion", "personalizaciones", "fulfillment_time"]]

    fig = px.imshow(
        af, text_auto=".1f", aspect="auto",
        color_continuous_scale=[[0, ACCENT_RED], [0.5, "#fff8e7"], [1, GREEN_LIGHT]],
        color_continuous_midpoint=100,
        labels=dict(x="Variable de experiencia", y="Segmento", color="Índice (base 100)"),
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        height=500,
        margin=dict(t=30, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class='quote-block'>
    <strong>Hallazgo clave:</strong> las personalizaciones son el mejor proxy del valor del cliente.
    El segmento <em>Jóvenes Digitales · Leales Premium</em> alcanza afinidad 109 en
    <code>num_customizations</code>, sugiriendo que el menú customizable es un driver de retención
    más fuerte que el ticket promedio.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# SLIDE 10 — VISUALIZACIONES COMPLEMENTARIAS
# =========================================================
elif slide == 10:
    st.title("Visualizaciones Complementarias")
    st.markdown("Análisis visual avanzado de los clusters y perfiles (Parte 11 del notebook).")
    
    opcion = st.selectbox(
        "Seleccione una visualización avanzada:",
        [
            "1. Distribución Categórica por Cluster (LCA)",
            "2. Violin Plots — Distribución RFM por Cluster",
            "3. Radar Chart — Comparación Multidimensional",
            "4. Visualización 3D — Espacio de Clientes RFM"
        ]
    )
    
    data_path = Path("outputs/clientes_segmentados.csv")
    if not data_path.exists():
        st.warning("⚠️ Los archivos de datos complementarios no están generados en `/outputs`. Asegúrate de que el notebook se haya ejecutado por completo.")
    else:
        df_clientes = pd.read_csv(data_path)
        
        if "1. Distribución Categórica" in opcion:
            st.markdown("### Composición Categórica de los Clusters Sociodemográficos (LCA)")
            var_cat = st.selectbox(
                "Selecciona una variable sociodemográfica para ver su distribución:",
                ["customer_age_group", "customer_gender", "region", "store_location_type", "order_channel", "is_rewards_member"]
            )
            
            tabla = pd.crosstab(df_clientes['Nombre_Socio'], df_clientes[var_cat], normalize='index') * 100
            tabla = tabla.reset_index()
            tabla_melt = pd.melt(tabla, id_vars=['Nombre_Socio'], var_name=var_cat, value_name='Porcentaje')
            
            fig = px.bar(
                tabla_melt,
                y='Nombre_Socio',
                x='Porcentaje',
                color=var_cat,
                orientation='h',
                title=f'Distribución de {var_cat} por Cluster LCA',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                labels={'Nombre_Socio': 'Cluster Sociodemográfico', 'Porcentaje': '% dentro del cluster'}
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend_title_text=var_cat,
                height=350,
                xaxis=dict(range=[0, 100])
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("Esta visualización nos permite ver la distribución de cada categoría sociodemográfica en los tres clusters identificados por LCA.")
            
        elif "2. Violin Plots" in opcion:
            st.markdown("### Distribución Completa de las Variables RFM por Cluster (Violin Plots)")
            var_rfm = st.selectbox(
                "Selecciona una variable RFM:",
                ["Recency", "Frequency", "Monetary"]
            )
            
            fig = px.violin(
                df_clientes,
                x="Nombre_RFM",
                y=var_rfm,
                color="Nombre_RFM",
                box=True,
                points="outliers",
                title=f'Distribución de {var_rfm} por Cluster RFM',
                color_discrete_map=PALETA_RFM,
                labels={"Nombre_RFM": "Cluster RFM", var_rfm: f"Valor de {var_rfm}"}
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(gridcolor="rgba(0,0,0,0.06)"),
                showlegend=False,
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("A diferencia de los promedios simples, el gráfico de violín revela la distribución completa (cuartiles, densidad y valores atípicos) de cada segmento RFM.")
            
        elif "3. Radar Chart" in opcion:
            st.markdown("### Comparación Multidimensional (Radar de Afinidades)")
            
            vars_radar = ['Recency_inv', 'Frequency', 'Monetary', 'customer_satisfaction', 'cart_size']
            perfil = (df_clientes.groupby('Segmento_Nombre')
                      .agg(Recency=('Recency', 'mean'),
                           Frequency=('Frequency', 'mean'),
                           Monetary=('Monetary', 'mean'),
                           customer_satisfaction=('customer_satisfaction', 'mean'),
                           cart_size=('cart_size', 'mean'),
                           N=('customer_id', 'count'))
                      .copy())
            
            perfil['Recency_inv'] = perfil['Recency'].max() - perfil['Recency']
            
            perfil_norm = perfil[vars_radar].copy()
            for v in vars_radar:
                rng = perfil_norm[v].max() - perfil_norm[v].min()
                perfil_norm[v] = (perfil_norm[v] - perfil_norm[v].min()) / (rng if rng > 0 else 1)
                
            top_segs = perfil['N'].sort_values(ascending=False).head(4).index.tolist()
            
            fig = go.Figure()
            colores_radar = ['#006241', '#cba258', '#a6192e', '#1e3932']
            etiquetas_radar = ['Recency Invertida', 'Frequency', 'Monetary', 'Satisfacción', 'Cart size']
            
            for i, seg in enumerate(top_segs):
                valores = perfil_norm.loc[seg, vars_radar].tolist()
                valores += valores[:1]
                
                fig.add_trace(go.Scatterpolar(
                    r=valores,
                    theta=etiquetas_radar + [etiquetas_radar[0]],
                    fill='toself',
                    name=f'{seg} (n={perfil.loc[seg, "N"]:.0f})',
                    line=dict(color=colores_radar[i], width=2.5)
                ))
                
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1.05],
                        gridcolor="rgba(0,0,0,0.06)",
                    ),
                    angularaxis=dict(
                        gridcolor="rgba(0,0,0,0.06)"
                    )
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif"),
                height=500,
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("El radar compara los 4 segmentos cruzados más grandes de forma simultánea. Valores más cercanos al borde exterior indican un mejor comportamiento o afinidad en esa variable.")
            
        elif "4. Visualización 3D" in opcion:
            st.markdown("### Representación 3D del Espacio Conductual RFM")
            sample_3d = df_clientes.sample(min(5000, len(df_clientes)), random_state=42)
            
            fig = px.scatter_3d(
                sample_3d,
                x='Recency',
                y='Frequency',
                z='Monetary',
                color='Nombre_RFM',
                color_discrete_map=PALETA_RFM,
                opacity=0.5,
                title='Espacio 3D de Clientes Starbucks (Muestra de 5,000 clientes)',
                labels={'Nombre_RFM': 'Segmento RFM', 'Recency': 'Recency (días)', 'Frequency': 'Frequency (compras)', 'Monetary': 'Monetary ($)'}
            )
            
            fig.update_traces(marker=dict(size=4))
            
            # Centroides
            centroides = df_clientes.groupby('Nombre_RFM')[['Recency', 'Frequency', 'Monetary']].mean().reset_index()
            
            fig.add_trace(go.Scatter3d(
                x=centroides['Recency'],
                y=centroides['Frequency'],
                z=centroides['Monetary'],
                mode='markers+text',
                text=centroides['Nombre_RFM'],
                textposition="top center",
                marker=dict(
                    symbol='diamond',
                    size=12,
                    color=[PALETA_RFM[n] for n in centroides['Nombre_RFM']],
                    line=dict(color='black', width=3)
                ),
                name='Centroides'
            ))
            
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter, sans-serif"),
                height=600,
                scene=dict(
                    xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,0,0,0.06)"),
                    yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,0,0,0.06)"),
                    zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,0,0,0.06)"),
                ),
                margin=dict(l=0, r=0, b=0, t=30),
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("Este gráfico 3D interactivo le permite arrastrar, rotar y hacer zoom para explorar la distribución espacial tridimensional de los clientes en función de sus tres métricas de comportamiento (Recency, Frequency, Monetary). Los diamantes grandes representan los centros de gravedad de cada grupo.")

# =========================================================
# SLIDE 11 — MERCADOS META (ANTES SLIDE 10)
# =========================================================
elif slide == 11:
    st.title("Identificación de Mercados Meta")
    st.markdown("Aplicación de los **cuatro criterios STP** (Kotler) sobre los 9 segmentos.")

    # Tabla de criterios
    criterios = pd.DataFrame([
        ["Sustancialidad", "Tamaño suficiente para justificar inversión", "≥ 7% del mercado"],
        ["Accionabilidad", "Puede ser alcanzado con propuesta diferenciada", "Canal y mensaje identificables"],
        ["Diferenciabilidad", "Responde distinto a acciones de marketing", "Afinidades ≠ 100"],
        ["Rentabilidad", "Capacidad de gasto", "Monetary ≥ mediana poblacional"],
    ], columns=["Criterio", "Definición", "Operacionalización"])
    st.dataframe(criterios, hide_index=True, use_container_width=True)

    st.markdown("---")
    st.markdown("### Decisión final")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class='meta-card'>
            <span class='badge'>⭐ Meta Principal</span>
            <h3>Jóvenes Digitales · Regulares Activos</h3>
            <p style='font-size:0.9rem; color:{NEUTRAL};'>
            28% del mercado · 5.5 compras/cliente · $84 ticket medio
            </p>
            <p>El cliente más frecuente del mercado. Volumen sostén del negocio.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='meta-card premium'>
            <span class='badge gold'>⭐ Meta Principal</span>
            <h3>Jóvenes Digitales · Leales Premium</h3>
            <p style='font-size:0.9rem; color:{NEUTRAL};'>
            23% del mercado · 9.3 compras/cliente · $147 ticket medio
            </p>
            <p>Núcleo de valor. Frecuencia alta y personalización elevada.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='meta-card reactivacion'>
            <span class='badge red'>🔄 Reactivación</span>
            <h3>Jóvenes Digitales · Dormidos</h3>
            <p style='font-size:0.9rem; color:{NEUTRAL};'>
            9% del mercado · 301 días sin comprar · perfil idéntico al meta principal
            </p>
            <p>Oportunidad de reactivación a bajo costo. Win-back digital.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info(
        "**Cobertura total de los segmentos priorizados: ~60% del mercado.** "
        "Los 6 segmentos restantes se descartan por sustancialidad insuficiente (<7%) "
        "o por solapamiento con los mercados meta seleccionados."
    )

# =========================================================
# SLIDE 12 — POSICIONAMIENTO (ANTES SLIDE 11)
# =========================================================
elif slide == 12:
    st.title("Estrategia de Posicionamiento")
    st.markdown("Propuesta de valor diferenciada para cada mercado meta.")

    posic = [
        {
            "nombre": "Jóvenes Digitales · Regulares Activos",
            "clase": "",
            "badge": "",
            "insight": "Busca consistencia y rapidez. Starbucks es parte de su rutina, no un evento.",
            "propuesta": "Experiencia confiable + rapidez + programa de lealtad accesible.",
            "canal": "Tienda urbana/suburbana con foco en Mobile Order y Drive-Thru.",
            "tactica": "Rewards con beneficios de baja barrera (descuentos por frecuencia, refill gratis).",
        },
        {
            "nombre": "Jóvenes Digitales · Leales Premium",
            "clase": "premium",
            "badge": "gold",
            "insight": "Quiere personalización y reconocimiento. Paga por una experiencia adaptada.",
            "propuesta": "Menú customizable amplio + reconocimiento Rewards + opciones premium estacionales.",
            "canal": "Tienda flagship urbana con énfasis en personalización y Mobile App.",
            "tactica": "Rewards multi-tier con beneficios premium (early access, ediciones limitadas).",
        },
        {
            "nombre": "Jóvenes Digitales · Dormidos",
            "clase": "reactivacion",
            "badge": "red",
            "insight": "Conoce la marca y ya consumió antes. La barrera no es awareness sino re-enganche.",
            "propuesta": "Campaña 'te extrañamos' con incentivo bajo costo + comunicación personalizada.",
            "canal": "Email + Mobile App push + retargeting digital. Sin infraestructura nueva.",
            "tactica": "Campaña win-back de 60 días midiendo conversión a Regular Activo.",
        },
    ]

    for p in posic:
        st.markdown(f"""
        <div class='meta-card {p["clase"]}'>
            <span class='badge {p["badge"]}'>Mercado Meta</span>
            <h3>{p["nombre"]}</h3>
            <p><strong>💡 Insight central:</strong> {p["insight"]}</p>
            <p><strong>🎯 Propuesta de valor:</strong> {p["propuesta"]}</p>
            <p><strong>📍 Canal y formato:</strong> {p["canal"]}</p>
            <p><strong>⚙️ Acción táctica clave:</strong> {p["tactica"]}</p>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# SLIDE 13 — CONCLUSIONES (ANTES SLIDE 12)
# =========================================================
elif slide == 13:
    st.title("Conclusiones y Recomendaciones")

    st.markdown("### Hallazgos no triviales")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='meta-card'>
            <h3 style='font-size:1.1rem;'>1. Lealtad alta inusual</h3>
            <p>El 35% del mercado son Leales Premium — proporción inusualmente alta.
            La estrategia debe <strong>proteger ese núcleo</strong> antes que crecer en los márgenes.</p>
        </div>
        <div class='meta-card'>
            <h3 style='font-size:1.1rem;'>2. Demografía no diferencia valor</h3>
            <p>El segmento mayoritario de Jóvenes Digitales (60%) aparece en todos los niveles RFM.
            La diferenciación entre cliente valioso y casual está en el <strong>comportamiento</strong>,
            no en el perfil demográfico.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='meta-card premium'>
            <h3 style='font-size:1.1rem;'>3. Reactivación bajo costo</h3>
            <p>Los Jóvenes Digitales Dormidos (9%) comparten perfil con el segmento más grande
            pero llevan ~300 días sin comprar. <strong>Una campaña win-back digital</strong>
            puede convertirlos en regulares activos.</p>
        </div>
        <div class='meta-card premium'>
            <h3 style='font-size:1.1rem;'>4. Personalización = retención</h3>
            <p>Los Leales Premium muestran afinidad 109 en personalizaciones.
            El <strong>menú customizable</strong> es un driver de retención más fuerte
            que el ticket promedio.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 📊 Limitaciones del estudio
 
        - Datos sintéticos: validar con data real antes de invertir
        - Sin información de competencia ni precios inmobiliarios
        - Snapshot temporal fijo (no captura tendencias)
        - Variables limitadas (sin ingreso, ocupación)
        - No distingue cliente nuevo vs recurrente
        """)
    with col2:
        st.markdown("""
        ### 🔜 Próximos pasos al inversionista
 
        - Validar segmentación con piloto en 1-2 zonas
        - Análisis económico por ubicación (renta, foot traffic)
        - Estudio de canibalización vs tiendas existentes
        - Diseñar campaña win-back y medir lift real
        - Implementar tracking de conversión entre segmentos
        """)

    st.markdown("---")
    st.markdown(f"""
    <div style='text-align:center; padding:2rem;'>
        <h2 style='color:{GREEN_DARK};'>¿Preguntas?</h2>
        <p class='footer-portada'>Mercado 2 · Starbucks América · AEM 2026-1</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# CONTROLES INFERIORES
# =========================================================
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ Anterior", disabled=(slide == 0), use_container_width=True):
        go_to(slide - 1)
        st.rerun()
with col2:
    st.markdown(
        f"<p class='slide-counter'>Slide {slide + 1} de {len(SLIDES)} · {SLIDES[slide]}</p>",
        unsafe_allow_html=True,
    )
with col3:
    if st.button("Siguiente ➡️", disabled=(slide == len(SLIDES) - 1), use_container_width=True):
        go_to(slide + 1)
        st.rerun()
