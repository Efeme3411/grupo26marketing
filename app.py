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
GREEN_DARK   = "#006241"
GREEN_LIGHT  = "#1e3932"
GOLD         = "#cba258"
ACCENT_RED   = "#d62828"
NEUTRAL      = "#3d3935"
BG_CREAM     = "#f5f1e8"

PALETA_RFM = {
    "Dormidos":          ACCENT_RED,
    "Regulares Activos": GOLD,
    "Leales Premium":    GREEN_DARK,
}
PALETA_SOCIO = [GREEN_DARK, GOLD, GREEN_LIGHT]

# =========================================================
# ESTILOS
# =========================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    h1, h2, h3 {{
        font-family: 'Playfair Display', serif;
        color: {GREEN_DARK};
    }}
    h1 {{
        font-weight: 900;
        letter-spacing: -1px;
    }}
    .stApp {{
        background: {BG_CREAM};
    }}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1200px;
    }}
    section[data-testid="stSidebar"] {{
        background: {GREEN_DARK};
    }}
    section[data-testid="stSidebar"] * {{
        color: white !important;
    }}
    section[data-testid="stSidebar"] .stButton button {{
        background: transparent;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2);
        text-align: left;
        font-weight: 400;
        border-radius: 4px;
        margin: 2px 0;
    }}
    section[data-testid="stSidebar"] .stButton button:hover {{
        background: rgba(203, 162, 88, 0.2);
        border-color: {GOLD};
    }}
    .slide-counter {{
        color: {NEUTRAL};
        text-align: center;
        font-size: 0.85rem;
        font-style: italic;
        opacity: 0.7;
    }}
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid {GREEN_DARK};
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .metric-value {{
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: {GREEN_DARK};
        line-height: 1;
    }}
    .metric-label {{
        color: {NEUTRAL};
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.3rem;
    }}
    .meta-card {{
        background: white;
        padding: 1.8rem;
        border-radius: 12px;
        border-top: 5px solid {GREEN_DARK};
        margin: 1rem 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }}
    .meta-card.reactivacion {{
        border-top-color: {ACCENT_RED};
    }}
    .meta-card.premium {{
        border-top-color: {GOLD};
    }}
    .meta-card h3 {{
        margin-top: 0;
        font-size: 1.4rem;
    }}
    .meta-card .badge {{
        display: inline-block;
        background: {GREEN_DARK};
        color: white;
        padding: 0.2rem 0.7rem;
        border-radius: 4px;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
    }}
    .meta-card .badge.gold {{
        background: {GOLD};
    }}
    .meta-card .badge.red {{
        background: {ACCENT_RED};
    }}
    .quote-block {{
        background: white;
        border-left: 5px solid {GOLD};
        padding: 1.5rem 2rem;
        margin: 1.5rem 0;
        font-style: italic;
        font-size: 1.05rem;
        color: {NEUTRAL};
        border-radius: 0 6px 6px 0;
    }}
    .footer-portada {{
        color: {NEUTRAL};
        opacity: 0.6;
        font-size: 0.85rem;
    }}
    hr {{
        border-color: {GOLD};
        opacity: 0.3;
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATOS (hardcoded desde los outputs reales del notebook)
# =========================================================
# RFM perfiles (de la celda 8 del notebook)
RFM_PROFILE = pd.DataFrame({
    "Cluster": [0, 1, 2],
    "Nombre":  ["Dormidos", "Leales Premium", "Regulares Activos"],
    "Recency": [296.92, 70.37, 76.03],
    "Frequency": [4.18, 9.40, 5.52],
    "Monetary": [61.22, 142.75, 80.27],
    "N_clientes": [2344, 5254, 7390],
})
RFM_PROFILE["% mercado"] = (RFM_PROFILE["N_clientes"] / RFM_PROFILE["N_clientes"].sum() * 100).round(1)

# Sociodemográfico LCA (de la celda 6)
SOCIO_PROFILE = pd.DataFrame({
    "Cluster": [0, 1, 2],
    "Nombre":  ["Perfil Nicho A", "Mainstream Mayoritario", "Perfil Nicho B"],
    "N_clientes": [2677, 8951, 3360],
})
SOCIO_PROFILE["% mercado"] = (SOCIO_PROFILE["N_clientes"] / SOCIO_PROFILE["N_clientes"].sum() * 100).round(1)

# Matriz cruzada (de la celda 16)
MATRIZ = pd.DataFrame([
    {"Socio": 1, "RFM": 2, "Nombre": "Mainstream Mayoritario · Regulares Activos", "N": 4194, "Pct": 28.0, "Rec": 76.62, "Freq": 5.48, "Mon": 84.15},
    {"Socio": 1, "RFM": 1, "Nombre": "Mainstream Mayoritario · Leales Premium",   "N": 3461, "Pct": 23.1, "Rec": 70.98, "Freq": 9.31, "Mon": 147.07},
    {"Socio": 2, "RFM": 2, "Nombre": "Perfil Nicho B · Regulares Activos",         "N": 1832, "Pct": 12.2, "Rec": 74.72, "Freq": 5.60, "Mon": 74.38},
    {"Socio": 0, "RFM": 2, "Nombre": "Perfil Nicho A · Regulares Activos",         "N": 1364, "Pct": 9.1,  "Rec": 75.95, "Freq": 5.55, "Mon": 76.21},
    {"Socio": 1, "RFM": 0, "Nombre": "Mainstream Mayoritario · Dormidos",          "N": 1296, "Pct": 8.6,  "Rec": 301.47, "Freq": 4.22, "Mon": 65.94},
    {"Socio": 2, "RFM": 1, "Nombre": "Perfil Nicho B · Leales Premium",            "N": 971,  "Pct": 6.5,  "Rec": 67.40, "Freq": 9.61, "Mon": 133.87},
    {"Socio": 0, "RFM": 1, "Nombre": "Perfil Nicho A · Leales Premium",            "N": 822,  "Pct": 5.5,  "Rec": 71.33, "Freq": 9.55, "Mon": 135.05},
    {"Socio": 2, "RFM": 0, "Nombre": "Perfil Nicho B · Dormidos",                  "N": 557,  "Pct": 3.7,  "Rec": 290.57, "Freq": 4.21, "Mon": 55.72},
    {"Socio": 0, "RFM": 0, "Nombre": "Perfil Nicho A · Dormidos",                  "N": 491,  "Pct": 3.3,  "Rec": 292.10, "Freq": 4.02, "Mon": 54.98},
])

# Afinidades (de la celda 18)
AFINIDAD = pd.DataFrame([
    {"Segmento": "Mainstream Mayoritario · Regulares Activos", "cart_size": 101.1, "satisfaccion": 100.9, "personalizaciones": 108.8, "fulfillment_time": 101.8, "pct": 28.0},
    {"Segmento": "Mainstream Mayoritario · Leales Premium",    "cart_size": 105.2, "satisfaccion": 100.7, "personalizaciones": 108.8, "fulfillment_time": 100.8, "pct": 23.1},
    {"Segmento": "Perfil Nicho B · Regulares Activos",          "cart_size": 93.3,  "satisfaccion": 98.9,  "personalizaciones": 83.8,  "fulfillment_time": 91.0,  "pct": 12.2},
    {"Segmento": "Perfil Nicho A · Regulares Activos",          "cart_size": 95.4,  "satisfaccion": 98.1,  "personalizaciones": 88.6,  "fulfillment_time": 105.4, "pct": 9.1},
    {"Segmento": "Mainstream Mayoritario · Dormidos",           "cart_size": 103.3, "satisfaccion": 101.5, "personalizaciones": 111.4, "fulfillment_time": 103.0, "pct": 8.6},
    {"Segmento": "Perfil Nicho B · Leales Premium",             "cart_size": 98.5,  "satisfaccion": 99.2,  "personalizaciones": 86.4,  "fulfillment_time": 93.7,  "pct": 6.5},
    {"Segmento": "Perfil Nicho A · Leales Premium",             "cart_size": 98.5,  "satisfaccion": 98.3,  "personalizaciones": 91.2,  "fulfillment_time": 104.4, "pct": 5.5},
    {"Segmento": "Perfil Nicho B · Dormidos",                   "cart_size": 93.7,  "satisfaccion": 98.9,  "personalizaciones": 83.1,  "fulfillment_time": 89.1,  "pct": 3.7},
    {"Segmento": "Perfil Nicho A · Dormidos",                   "cart_size": 95.5,  "satisfaccion": 98.0,  "personalizaciones": 85.2,  "fulfillment_time": 106.7, "pct": 3.3},
])

# Comparación de modelos
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
        marker = "▶" if i == st.session_state.slide else "○"
        if st.button(f"{marker}  {i+1}. {titulo}", key=f"nav_{i}", use_container_width=True):
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
        <p style='color:{GOLD}; letter-spacing: 4px; font-size: 0.9rem; margin-bottom: 0;'>
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
            paper_bgcolor=BG_CREAM,
            plot_bgcolor=BG_CREAM,
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
        yaxis=dict(title="Valor normalizado [0,1]", range=[-0.05, 1.1]),
        paper_bgcolor=BG_CREAM,
        plot_bgcolor="white",
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
        El cluster <strong>Mainstream Mayoritario</strong> concentra el 60% del mercado.
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
            paper_bgcolor=BG_CREAM,
            plot_bgcolor="white",
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
    nombres_socio_map = {0: "Nicho A", 1: "Mainstream", 2: "Nicho B"}
    nombres_rfm_map   = {0: "Dormidos", 1: "Leales Premium", 2: "Regulares Activos"}
    pivot.index = [nombres_socio_map[i] for i in pivot.index]
    pivot.columns = [nombres_rfm_map[i] for i in pivot.columns]

    fig = px.imshow(
        pivot, text_auto=".1f", aspect="auto",
        color_continuous_scale=[[0, "#fff8e7"], [0.5, GOLD], [1, GREEN_DARK]],
        labels=dict(x="Comportamiento RFM", y="Perfil Sociodemográfico", color="% mercado"),
    )
    fig.update_layout(
        paper_bgcolor=BG_CREAM,
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
        paper_bgcolor=BG_CREAM,
        plot_bgcolor="white",
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
        color_continuous_scale=[[0, ACCENT_RED], [0.5, "#fff8e7"], [1, GREEN_DARK]],
        color_continuous_midpoint=100,
        labels=dict(x="Variable de experiencia", y="Segmento", color="Índice (base 100)"),
    )
    fig.update_layout(
        paper_bgcolor=BG_CREAM,
        height=500,
        margin=dict(t=30, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class='quote-block'>
    <strong>Hallazgo clave:</strong> las personalizaciones son el mejor proxy del valor del cliente.
    El segmento <em>Mainstream Mayoritario · Leales Premium</em> alcanza afinidad 109 en
    <code>num_customizations</code>, sugiriendo que el menú customizable es un driver de retención
    más fuerte que el ticket promedio.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# SLIDE 10 — MERCADOS META
# =========================================================
elif slide == 10:
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
            <h3>Mainstream Regular</h3>
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
            <h3>Mainstream Premium</h3>
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
            <h3>Mainstream Dormido</h3>
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
# SLIDE 11 — POSICIONAMIENTO
# =========================================================
elif slide == 11:
    st.title("Estrategia de Posicionamiento")
    st.markdown("Propuesta de valor diferenciada para cada mercado meta.")

    posic = [
        {
            "nombre": "Mainstream Regular",
            "clase": "",
            "badge": "",
            "insight": "Busca consistencia y rapidez. Starbucks es parte de su rutina, no un evento.",
            "propuesta": "Experiencia confiable + rapidez + programa de lealtad accesible.",
            "canal": "Tienda urbana/suburbana con foco en Mobile Order y Drive-Thru.",
            "tactica": "Rewards con beneficios de baja barrera (descuentos por frecuencia, refill gratis).",
        },
        {
            "nombre": "Mainstream Premium",
            "clase": "premium",
            "badge": "gold",
            "insight": "Quiere personalización y reconocimiento. Paga por una experiencia adaptada.",
            "propuesta": "Menú customizable amplio + reconocimiento Rewards + opciones premium estacionales.",
            "canal": "Tienda flagship urbana con énfasis en personalización y Mobile App.",
            "tactica": "Rewards multi-tier con beneficios premium (early access, ediciones limitadas).",
        },
        {
            "nombre": "Mainstream Dormido",
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
# SLIDE 12 — CONCLUSIONES
# =========================================================
elif slide == 12:
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
            <p>El segmento mayoritario (60%) aparece en todos los niveles RFM.
            La diferenciación entre cliente valioso y casual está en el <strong>comportamiento</strong>,
            no en el perfil demográfico.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='meta-card premium'>
            <h3 style='font-size:1.1rem;'>3. Reactivación bajo costo</h3>
            <p>Los Mainstream Dormidos (9%) comparten perfil con el segmento más grande
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
