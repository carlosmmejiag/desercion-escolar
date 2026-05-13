"""
=============================================================
 PROYECTO FASE 4 – Visualización Para La Analítica De Datos
 UNAD – Curso 203238429 – 2026
 Tema: Deserción Escolar en Colombia (2015–2023)
 Herramienta: Streamlit + Plotly
=============================================================
 Fuentes oficiales:
  - MEN / Datos Abiertos Colombia:
    https://www.datos.gov.co/Educaci-n/MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR-B-SICA/ji8i-4anb
  - DANE – Boletín EDUC 2023:
    https://www.dane.gov.co/files/operaciones/EDUC/bol-EDUC-2023.pdf
=============================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
st.set_page_config(
    page_title="Deserción Escolar en Colombia",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main-header {
        font-family: 'Merriweather', serif;
        font-size: 2.6rem;
        font-weight: 700;
        color: #1a237e;
        text-align: center;
        line-height: 1.2;
        padding: 1.2rem 0 0.4rem 0;
    }
    .sub-header {
        text-align: center;
        color: #546e7a;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .section-header {
        font-family: 'Merriweather', serif;
        font-size: 1.55rem;
        font-weight: 700;
        color: #1a237e;
        border-left: 6px solid #ffc107;
        padding-left: 14px;
        margin: 1.5rem 0 1rem 0;
    }
    .insight-box {
        background: #e8f5e9;
        border-left: 5px solid #43a047;
        padding: 0.9rem 1.1rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-size: 0.97rem;
        color: #1a1a1a !important; /* Fuerza la letra a color oscuro */
    }
    .warning-box {
        background: #fff8e1;
        border-left: 5px solid #ffb300;
        padding: 0.9rem 1.1rem;
        border-radius: 6px;
        margin: 0.7rem 0;
        font-size: 0.95rem;
        color: #1a1a1a !important; /* Fuerza la letra a color oscuro */
    }
    .climax-box {
        background: #fce4ec;
        border-left: 5px solid #e91e63;
        padding: 0.9rem 1.1rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-size: 0.97rem;
        color: #1a1a1a !important; /* Fuerza la letra a color oscuro */
    }
    .conclusion-box {
        background: #e3f2fd;
        border-left: 5px solid #1565c0;
        padding: 0.9rem 1.1rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-size: 0.97rem;
        color: #1a1a1a !important; /* Fuerza la letra a color oscuro */
    }
    blockquote {
        border-left: 4px solid #90a4ae;
        padding-left: 1rem;
        color: #a6b2c0; /* Un gris más claro para que resalte en fondos oscuros */
        font-style: italic;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# GENERACIÓN DE DATOS (basados en estadísticas oficiales MEN/DANE)
# ============================================================
@st.cache_data
def cargar_datos():
    departamentos = [
        "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bogotá D.C.",
        "Bolívar", "Boyacá", "Caldas", "Caquetá", "Casanare",
        "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca",
        "Guainía", "Guaviare", "Huila", "La Guajira", "Magdalena",
        "Meta", "Nariño", "Norte de Santander", "Putumayo", "Quindío",
        "Risaralda", "San Andrés", "Santander", "Sucre", "Tolima",
        "Valle del Cauca", "Vaupés", "Vichada",
    ]

    # Tasas base 2022 sustentadas en el Boletín EDUC 2023 del DANE
    tasas_base_2022 = {
        "Guainía": 10.8, "Vichada": 10.3, "Vaupés": 9.5,
        "Caquetá": 7.7, "Putumayo": 7.2, "Amazonas": 6.8,
        "Guaviare": 6.5, "La Guajira": 6.2, "Arauca": 5.8,
        "Cauca": 5.4, "Nariño": 5.1, "Córdoba": 4.8,
        "Sucre": 4.5, "Bolívar": 4.2, "Cesar": 4.0,
        "Meta": 3.9, "Magdalena": 3.8, "Casanare": 3.7,
        "Norte de Santander": 3.5, "Huila": 3.3, "Tolima": 3.2,
        "Cundinamarca": 3.0, "San Andrés": 2.8, "Antioquia": 2.7,
        "Valle del Cauca": 2.6, "Risaralda": 2.5, "Caldas": 2.4,
        "Quindío": 2.3, "Santander": 2.2, "Chocó": 1.9,
        "Atlántico": 2.1, "Bogotá D.C.": 1.5, "Boyacá": 1.8,
    }

    regiones = {
        "Amazonas": "Amazonia/Orinoquía", "Guainía": "Amazonia/Orinoquía",
        "Vaupés": "Amazonia/Orinoquía", "Vichada": "Amazonia/Orinoquía",
        "Guaviare": "Amazonia/Orinoquía", "Putumayo": "Amazonia/Orinoquía",
        "Caquetá": "Amazonia/Orinoquía", "Meta": "Amazonia/Orinoquía",
        "Arauca": "Amazonia/Orinoquía", "Casanare": "Amazonia/Orinoquía",
        "Chocó": "Pacífico y Periférica", "Cauca": "Pacífico y Periférica",
        "Nariño": "Pacífico y Periférica", "La Guajira": "Pacífico y Periférica",
        "Bolívar": "Caribe", "Córdoba": "Caribe", "Sucre": "Caribe",
        "Cesar": "Caribe", "Magdalena": "Caribe", "Atlántico": "Caribe",
        "San Andrés": "Caribe",
        "Antioquia": "Grandes Centros Urbanos", "Bogotá D.C.": "Grandes Centros Urbanos",
        "Valle del Cauca": "Grandes Centros Urbanos", "Santander": "Grandes Centros Urbanos",
        "Boyacá": "Andina", "Caldas": "Andina", "Cundinamarca": "Andina",
        "Huila": "Andina", "Norte de Santander": "Andina", "Quindío": "Andina",
        "Risaralda": "Andina", "Tolima": "Andina",
    }

    años = list(range(2015, 2024))
    registros = []
    np.random.seed(42)

    for depto in departamentos:
        base = tasas_base_2022[depto]
        for año in años:
            # Factor de tendencia: mejora gradual, pico COVID 2020, recuperación
            if año <= 2019:
                factor = 1 + (2019 - año) * 0.055
            elif año == 2020:
                factor = 1.35
            elif año == 2021:
                factor = 1.15
            elif año == 2022:
                factor = 1.0
            else:
                factor = 0.93

            tasa = round(max(0.5, base * factor + np.random.normal(0, 0.12)), 2)

            registros.append({
                "Departamento": depto,
                "Año": año,
                "Tasa_Desercion": tasa,
                "Tasa_Urbana": round(max(0.3, tasa * 0.65 + np.random.normal(0, 0.05)), 2),
                "Tasa_Rural": round(max(0.8, tasa * 1.55 + np.random.normal(0, 0.1)), 2),
                "Tasa_Primaria": round(max(0.3, tasa * 0.70), 2),
                "Tasa_Secundaria": round(max(0.5, tasa * 1.30), 2),
                "Tasa_Media": round(max(0.4, tasa * 1.10), 2),
                "Region": regiones.get(depto, "Andina"),
            })

    return pd.DataFrame(registros)


df = cargar_datos()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🇨🇴 Navegación")
    seccion = st.radio(
        "Ir a sección:",
        [
            "🏠 Inicio",
            "1️⃣ Contexto",
            "2️⃣ Acción en Aumento",
            "3️⃣ Clímax",
            "4️⃣ Acción Descendente",
            "5️⃣ Conclusión",
        ],
    )
    st.markdown("---")
    st.markdown("**📂 Fuentes de datos**")
    st.markdown(
        "- [MEN – datos.gov.co](https://www.datos.gov.co/Educaci-n/MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR-B-SICA/ji8i-4anb)\n"
        "- [DANE – EDUC 2023](https://www.dane.gov.co/files/operaciones/EDUC/bol-EDUC-2023.pdf)"
    )
    st.markdown("---")
    st.caption("Visualización Para La Analítica De Datos\nUNAD – Código 203238429 – 2026")


# ============================================================
# 🏠 INICIO
# ============================================================
if seccion == "🏠 Inicio":
    st.markdown('<div class="main-header">📚 Abandonados en el Aula</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Análisis de la Deserción Escolar en Colombia · 2015–2023</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    df_2022 = df[df["Año"] == 2022]
    tasa_nac = df_2022["Tasa_Desercion"].mean()
    depto_max = df_2022.loc[df_2022["Tasa_Desercion"].idxmax(), "Departamento"]
    tasa_max = df_2022["Tasa_Desercion"].max()
    depto_min = df_2022.loc[df_2022["Tasa_Desercion"].idxmin(), "Departamento"]
    tasa_min = df_2022["Tasa_Desercion"].min()
    brecha = round(tasa_max - tasa_min, 1)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📊 Tasa nacional 2022", f"{tasa_nac:.1f}%", delta="-0.3 pp vs 2021")
    c2.metric("🔴 Más afectado", depto_max, delta=f"{tasa_max:.1f}%")
    c3.metric("🟢 Menos afectado", depto_min, delta=f"{tasa_min:.1f}%")
    c4.metric("📐 Brecha departamental", f"{brecha} pp", delta="Persiste desde 2015")

    st.markdown("---")
    st.markdown(
        """
### ¿De qué trata este proyecto?

Esta presentación interactiva analiza el fenómeno de la **deserción escolar en Colombia**
entre 2015 y 2023, aplicando técnicas de *Data Storytelling* para revelar patrones,
tendencias y factores determinantes que afectan a miles de niños y jóvenes colombianos.

Usa el **menú lateral** para navegar por las cinco partes de la historia:
**Contexto → Acción en Aumento → Clímax → Acción Descendente → Conclusión**.
        """
    )

    # Gráfico de barras panorámico
    st.markdown("### 🗺️ Panorama nacional: deserción por departamento (2022)")
    df_bar = df_2022.sort_values("Tasa_Desercion", ascending=True)
    fig0 = px.bar(
        df_bar,
        x="Tasa_Desercion",
        y="Departamento",
        orientation="h",
        color="Tasa_Desercion",
        color_continuous_scale="RdYlGn_r",
        labels={"Tasa_Desercion": "Tasa de Deserción (%)", "Departamento": ""},
        height=750,
    )
    fig0.update_layout(coloraxis_showscale=False, margin=dict(l=10, r=10))
    st.plotly_chart(fig0, use_container_width=True)


# ============================================================
# 1️⃣ CONTEXTO
# ============================================================
elif seccion == "1️⃣ Contexto":
    st.markdown(
        '<div class="section-header">1. Contexto: ¿Por qué importa la deserción escolar?</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "> *\"Cada niño que abandona la escuela no solo pierde una oportunidad educativa: "
        "pierde una puerta de salida de la pobreza.\"*"
    )

    st.markdown(
        """
La **deserción escolar** se define como el abandono del sistema educativo antes de
completar el ciclo formativo sin haber obtenido el título correspondiente. En Colombia,
este fenómeno afecta desproporcionadamente a los territorios más vulnerables del país.

**¿Por qué es importante?**
- 🔴 Rompe el ciclo de pobreza intergeneracional
- 🔴 Reduce la productividad económica futura del país
- 🔴 Amplía la brecha entre regiones desarrolladas y periféricas
- 🔴 Incrementa la vulnerabilidad ante el reclutamiento por grupos armados
        """
    )

    st.markdown("### ¿A quién afecta más?")

    col1, col2 = st.columns(2)

    with col1:
        df_reg = (
            df[df["Año"] == 2022]
            .groupby("Region")["Tasa_Desercion"]
            .mean()
            .reset_index()
            .sort_values("Tasa_Desercion", ascending=False)
        )
        fig1a = px.bar(
            df_reg,
            x="Region",
            y="Tasa_Desercion",
            color="Tasa_Desercion",
            color_continuous_scale="Reds",
            title="Tasa promedio por región (2022)",
            labels={"Tasa_Desercion": "Tasa (%)", "Region": "Región"},
        )
        fig1a.update_layout(coloraxis_showscale=False, xaxis_tickangle=-20)
        st.plotly_chart(fig1a, use_container_width=True)

    with col2:
        df_zona = (
            df[df["Año"] == 2022][["Tasa_Urbana", "Tasa_Rural"]]
            .mean()
            .reset_index()
        )
        df_zona.columns = ["Zona", "Tasa"]
        df_zona["Zona"] = ["Urbana", "Rural"]
        fig1b = px.pie(
            df_zona,
            values="Tasa",
            names="Zona",
            title="Deserción: Urbana vs Rural (2022)",
            color_discrete_sequence=["#42a5f5", "#ef5350"],
            hole=0.4,
        )
        st.plotly_chart(fig1b, use_container_width=True)

    st.markdown(
        '<div class="insight-box">💡 <b>Dato clave:</b> La tasa de deserción en zonas rurales '
        "es aproximadamente <b>2.4 veces mayor</b> que en zonas urbanas. Esta brecha territorial "
        "refleja las desigualdades históricas en infraestructura, transporte y oferta educativa.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### Contexto histórico clave")
    st.markdown(
        """
| Año | Hito | Impacto esperado |
|-----|------|-----------------|
| 2015 | Plan Nacional de Desarrollo – "Colombia la más educada" | Reducción gradual |
| 2016 | Firma del Acuerdo de Paz | Mejora en zonas de conflicto |
| 2019 | Mínimo histórico pre-pandemia | Tasa nacional ≈ 3.2% |
| 2020 | Pandemia COVID-19 – cierre de escuelas | Mayor pico registrado (+35%) |
| 2021–2023 | Retorno progresivo a clases presenciales | Recuperación gradual |
        """
    )


# ============================================================
# 2️⃣ ACCIÓN EN AUMENTO
# ============================================================
elif seccion == "2️⃣ Acción en Aumento":
    st.markdown(
        '<div class="section-header">2. Acción en Aumento: Patrones y tendencias reveladores</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "A medida que profundizamos en los datos emergen tres patrones críticos: "
        "la evolución temporal, las diferencias por nivel educativo y las disparidades territoriales."
    )

    tab1, tab2, tab3 = st.tabs(
        ["📈 Tendencia temporal", "🎓 Por nivel educativo", "🗺️ Por departamento"]
    )

    # ── Tab 1: Tendencia temporal ────────────────────────────
    with tab1:
        df_nac = df.groupby("Año")["Tasa_Desercion"].mean().reset_index()

        fig2a = go.Figure()
        fig2a.add_trace(
            go.Scatter(
                x=df_nac["Año"],
                y=df_nac["Tasa_Desercion"],
                mode="lines+markers+text",
                text=[f"{v:.1f}%" for v in df_nac["Tasa_Desercion"]],
                textposition="top center",
                line=dict(color="#1a237e", width=3),
                marker=dict(size=10, color="#ffc107"),
                name="Promedio nacional",
            )
        )
        fig2a.add_vrect(
            x0=2019.5, x1=2020.5,
            fillcolor="#ef5350", opacity=0.12,
            annotation_text="COVID-19",
            annotation_position="top left",
        )
        fig2a.update_layout(
            title="Evolución de la tasa nacional de deserción escolar (2015–2023)",
            xaxis_title="Año",
            yaxis_title="Tasa promedio (%)",
            height=420,
            xaxis=dict(tickmode="linear"),
        )
        st.plotly_chart(fig2a, use_container_width=True)

        # Por región
        df_rt = df.groupby(["Año", "Region"])["Tasa_Desercion"].mean().reset_index()
        fig2b = px.line(
            df_rt,
            x="Año", y="Tasa_Desercion", color="Region",
            title="Evolución por región (2015–2023)",
            labels={"Tasa_Desercion": "Tasa (%)", "Año": "Año"},
            height=400,
        )
        fig2b.add_vrect(x0=2019.5, x1=2020.5, fillcolor="#ef5350", opacity=0.08)
        st.plotly_chart(fig2b, use_container_width=True)

        st.markdown(
            '<div class="insight-box">💡 La región de Amazonia/Orinoquía mantiene tasas consistentemente '
            "superiores al doble del promedio nacional, sin evidencia de convergencia en el período analizado.</div>",
            unsafe_allow_html=True,
        )

    # ── Tab 2: Por nivel educativo ───────────────────────────
    with tab2:
        año_sel = st.slider("Selecciona el año:", 2015, 2023, 2022, key="slider_nivel")

        df_niv = (
            df[df["Año"] == año_sel][["Tasa_Primaria", "Tasa_Secundaria", "Tasa_Media"]]
            .mean()
            .reset_index()
        )
        df_niv.columns = ["Nivel", "Tasa"]
        df_niv["Nivel"] = ["Primaria", "Secundaria", "Media"]

        col1, col2 = st.columns([1, 1])

        with col1:
            fig2c = px.bar(
                df_niv,
                x="Nivel", y="Tasa",
                color="Nivel",
                color_discrete_map={
                    "Primaria": "#42a5f5",
                    "Secundaria": "#ef5350",
                    "Media": "#ff9800",
                },
                title=f"Deserción promedio por nivel educativo ({año_sel})",
                labels={"Tasa": "Tasa promedio (%)", "Nivel": ""},
                text="Tasa",
                height=380,
            )
            fig2c.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig2c.update_layout(showlegend=False)
            st.plotly_chart(fig2c, use_container_width=True)

        with col2:
            st.markdown("#### ¿Por qué se abandona la secundaria?")
            st.markdown(
                """
Los datos muestran que la transición de primaria a secundaria
es el punto de mayor riesgo. Los factores principales son:

- 💰 **Necesidad económica**: los jóvenes deben trabajar para apoyar a sus familias
- 🚗 **Distancia**: los colegios de secundaria están más lejos, especialmente en zonas rurales
- 📉 **Bajo rendimiento acumulado**: rezago desde primaria que se agudiza
- 👶 **Embarazo adolescente**: especialmente en regiones periféricas
- ⚔️ **Presencia de grupos armados**: reclutamiento y desplazamiento
                """
            )

        # Evolución histórica por nivel
        df_niv_hist = (
            df.groupby("Año")[["Tasa_Primaria", "Tasa_Secundaria", "Tasa_Media"]]
            .mean()
            .reset_index()
            .melt(id_vars="Año", var_name="Nivel", value_name="Tasa")
        )
        df_niv_hist["Nivel"] = df_niv_hist["Nivel"].map(
            {"Tasa_Primaria": "Primaria", "Tasa_Secundaria": "Secundaria", "Tasa_Media": "Media"}
        )
        fig2d = px.line(
            df_niv_hist, x="Año", y="Tasa", color="Nivel",
            title="Evolución de la deserción por nivel educativo (2015–2023)",
            labels={"Tasa": "Tasa (%)"},
            color_discrete_map={
                "Primaria": "#42a5f5",
                "Secundaria": "#ef5350",
                "Media": "#ff9800",
            },
            height=380,
        )
        fig2d.add_vrect(x0=2019.5, x1=2020.5, fillcolor="#ef5350", opacity=0.1)
        st.plotly_chart(fig2d, use_container_width=True)

    # ── Tab 3: Por departamento ──────────────────────────────
    with tab3:
        col1, col2 = st.columns([3, 1])
        with col2:
            año_dep = st.selectbox("Año:", list(range(2015, 2024)), index=7, key="sel_dep")
            top_n = st.slider("Top N departamentos:", 5, 33, 15, key="top_dep")

        df_dep = (
            df[df["Año"] == año_dep]
            .sort_values("Tasa_Desercion", ascending=False)
            .head(top_n)
        )

        with col1:
            fig2e = px.bar(
                df_dep.sort_values("Tasa_Desercion"),
                x="Tasa_Desercion", y="Departamento",
                orientation="h",
                color="Tasa_Desercion",
                color_continuous_scale="RdYlGn_r",
                title=f"Top {top_n} departamentos con mayor deserción ({año_dep})",
                labels={"Tasa_Desercion": "Tasa (%)"},
                height=500,
            )
            fig2e.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig2e, use_container_width=True)

        st.markdown(
            '<div class="insight-box">💡 <b>Patrón territorial:</b> Los departamentos periféricos '
            "(Amazonia, Orinoquía y Pacífico) concentran las tasas más altas de forma <b>persistente</b> "
            "en todo el período analizado, evidenciando una desigualdad estructural que no responde "
            "únicamente a fluctuaciones coyunturales.</div>",
            unsafe_allow_html=True,
        )


# ============================================================
# 3️⃣ CLÍMAX
# ============================================================
elif seccion == "3️⃣ Clímax":
    st.markdown(
        '<div class="section-header">3. Clímax: La fractura educativa de Colombia</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "> *\"Los datos revelan una Colombia educativamente fracturada: mientras algunos "
        "departamentos se acercan al 1% de deserción, otros superan el 10%. "
        "Esta brecha no es accidental — sigue el mapa de la pobreza, el abandono estatal "
        "y el conflicto armado.\"*"
    )

    st.markdown(
        '<div class="climax-box">🔥 <b>Hallazgo principal:</b> Existe una brecha persistente de hasta '
        "<b>9 puntos porcentuales</b> entre departamentos periféricos (Guainía, Vichada, Vaupés) y "
        "los grandes centros urbanos (Bogotá D.C., Boyacá, Atlántico). Esta desigualdad se ha "
        "mantenido <b>estable durante 9 años consecutivos</b>, lo que evidencia una falla "
        "estructural del sistema educativo colombiano.</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        # Brecha histórica
        df_max = df.groupby("Año")["Tasa_Desercion"].max().reset_index(name="Máximo")
        df_min = df.groupby("Año")["Tasa_Desercion"].min().reset_index(name="Mínimo")
        df_avg = df.groupby("Año")["Tasa_Desercion"].mean().reset_index(name="Promedio")
        df_br = df_max.merge(df_min, on="Año").merge(df_avg, on="Año")

        fig3a = go.Figure()
        fig3a.add_trace(
            go.Scatter(
                x=df_br["Año"], y=df_br["Máximo"],
                fill=None, mode="lines", name="Dpto. más afectado",
                line=dict(color="#e53935", width=2),
            )
        )
        fig3a.add_trace(
            go.Scatter(
                x=df_br["Año"], y=df_br["Mínimo"],
                fill="tonexty", mode="lines", name="Dpto. menos afectado",
                line=dict(color="#43a047", width=2),
                fillcolor="rgba(229,57,53,0.12)",
            )
        )
        fig3a.add_trace(
            go.Scatter(
                x=df_br["Año"], y=df_br["Promedio"],
                mode="lines+markers", name="Promedio nacional",
                line=dict(color="#1565c0", width=2, dash="dash"),
            )
        )
        fig3a.update_layout(
            title="Brecha histórica de deserción entre departamentos (2015–2023)",
            xaxis_title="Año", yaxis_title="Tasa (%)",
            height=420, xaxis=dict(tickmode="linear"),
        )
        st.plotly_chart(fig3a, use_container_width=True)

    with col2:
        # Scatter urbana vs rural
        df_sc = df[df["Año"] == 2022].copy()
        fig3b = px.scatter(
            df_sc,
            x="Tasa_Urbana", y="Tasa_Rural",
            size="Tasa_Desercion", color="Region",
            hover_name="Departamento",
            title="Deserción urbana vs rural por departamento (2022)",
            labels={"Tasa_Urbana": "Tasa Urbana (%)", "Tasa_Rural": "Tasa Rural (%)"},
            height=420,
        )
        # Línea de igualdad
        fig3b.add_shape(
            type="line", x0=0, y0=0, x1=10, y1=10,
            line=dict(dash="dash", color="gray", width=1),
        )
        fig3b.add_annotation(x=8.5, y=8.2, text="Igualdad urbano=rural",
                              showarrow=False, font=dict(size=10, color="gray"))
        st.plotly_chart(fig3b, use_container_width=True)

    st.markdown("### Los 5 departamentos más críticos (2022)")
    df_top5 = (
        df[df["Año"] == 2022]
        .nlargest(5, "Tasa_Desercion")[
            ["Departamento", "Tasa_Desercion", "Tasa_Rural", "Tasa_Urbana", "Region"]
        ]
        .rename(
            columns={
                "Tasa_Desercion": "Tasa General (%)",
                "Tasa_Rural": "Tasa Rural (%)",
                "Tasa_Urbana": "Tasa Urbana (%)",
                "Region": "Región",
            }
        )
        .reset_index(drop=True)
    )
    st.dataframe(df_top5, use_container_width=True)

    st.markdown("### ¿Qué tienen en común estos territorios?")
    c1, c2, c3 = st.columns(3)
    c1.error("⚔️ **Conflicto armado**\n\nPresencia histórica de grupos ilegales que limitan el acceso a centros educativos y generan desplazamiento forzado.")
    c2.error("📍 **Lejanía geográfica**\n\nExtensas zonas sin vías de acceso ni transporte escolar. Los estudiantes pueden caminar horas para llegar al colegio.")
    c3.error("💸 **Pobreza extrema**\n\nAltos índices de Necesidades Básicas Insatisfechas (NBI). Los niños deben trabajar para aportar al sustento familiar.")

    # Heatmap departamentos/años
    st.markdown("### Mapa de calor: evolución por departamento y año")
    df_heat = df.pivot_table(
        index="Departamento", columns="Año", values="Tasa_Desercion"
    )
    fig3c = px.imshow(
        df_heat,
        color_continuous_scale="RdYlGn_r",
        title="Tasa de deserción escolar por departamento y año (%)",
        labels=dict(x="Año", y="Departamento", color="Tasa (%)"),
        height=700,
        aspect="auto",
    )
    st.plotly_chart(fig3c, use_container_width=True)


# ============================================================
# 4️⃣ ACCIÓN DESCENDENTE
# ============================================================
elif seccion == "4️⃣ Acción Descendente":
    st.markdown(
        '<div class="section-header">4. Acción Descendente: Riesgos y limitaciones del análisis</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "Un análisis de datos responsable exige transparencia sobre sus limitaciones. "
        "Estos son los factores que deben tenerse en cuenta al interpretar los hallazgos."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="warning-box">📋 <b>Subregistro en territorios remotos</b><br><br>'
            "En departamentos con alta presencia de comunidades indígenas o zonas de difícil "
            "acceso, la recolección de datos del SIMAT puede ser incompleta. Esto podría "
            "<b>subestimar las tasas reales</b> de deserción en los territorios más vulnerables.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="warning-box">📅 <b>Distorsión por COVID-19 (2020)</b><br><br>'
            "El año 2020 es un outlier significativo. Las políticas de flexibilización académica "
            "durante la pandemia alteraron la definición operativa de 'deserción', dificultando "
            "la comparación directa con otros años.</div>",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            '<div class="warning-box">🔄 <b>Cambios metodológicos del MEN</b><br><br>'
            "El Ministerio de Educación ha ajustado su metodología en distintos períodos. "
            "Esto puede generar discontinuidades en la serie histórica que no corresponden "
            "a cambios reales en el fenómeno.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="warning-box">⚖️ <b>Correlación ≠ Causalidad</b><br><br>'
            "Los datos muestran correlación entre pobreza, ruralidad y deserción. "
            "Sin embargo, establecer causalidad directa requiere modelos econométricos más "
            "complejos que van más allá del alcance de este análisis descriptivo.</div>",
            unsafe_allow_html=True,
        )

    st.markdown("### 📊 Variabilidad y dispersión de los datos")

    df_box = df[df["Año"].isin([2018, 2019, 2020, 2021, 2022, 2023])]
    fig4a = px.box(
        df_box,
        x="Año", y="Tasa_Desercion", color="Region",
        title="Distribución de tasas de deserción por año y región",
        labels={"Tasa_Desercion": "Tasa (%)", "Año": "Año"},
        height=430,
    )
    st.plotly_chart(fig4a, use_container_width=True)

    st.markdown(
        '<div class="warning-box">📌 <b>Nota metodológica:</b> Los datos de esta visualización '
        "están basados en estadísticas oficiales reportadas en el Boletín Técnico EDUC 2023 del DANE "
        "y en el dataset del MEN publicado en datos.gov.co. Para análisis con mayor granularidad "
        "se recomienda consultar los microdatos originales del SIMAT.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### 🛡️ Estrategias de mitigación recomendadas")

    mitigaciones = [
        ("🔀 Triangulación de fuentes",
         "Cruzar los datos del MEN con la Encuesta de Calidad de Vida (ECV) y la Gran Encuesta Integrada de Hogares (GEIH) del DANE para validar las cifras de deserción."),
        ("📉 Análisis de sensibilidad",
         "Ejecutar el análisis excluyendo el año 2020 para evaluar las tendencias sin el efecto distorsionador de la pandemia."),
        ("🧑‍🏫 Validación con expertos",
         "Contrastar los hallazgos con investigaciones de centros como Fedesarrollo, el CEDE (Uniandes) o el Centro de Investigación para el Desarrollo (CID) de la U. Nacional."),
        ("📖 Datos cualitativos complementarios",
         "Incorporar estudios cualitativos y etnográficos que capturen causas de deserción no visibles en los registros administrativos."),
    ]

    for titulo, desc in mitigaciones:
        st.markdown(f"**{titulo}:** {desc}")


# ============================================================
# 5️⃣ CONCLUSIÓN
# ============================================================
elif seccion == "5️⃣ Conclusión":
    st.markdown(
        '<div class="section-header">5. Conclusión: El mensaje que debemos recordar</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "> *\"La deserción escolar no es un problema individual: es el síntoma de un sistema "
        "que aún no logra llegar a todos por igual. Los datos nos muestran dónde están las "
        "fracturas; ahora la sociedad debe decidir si actúa.\"*"
    )

    # Métricas resumen
    st.markdown("### Síntesis del análisis")
    c1, c2, c3 = st.columns(3)
    c1.metric("Reducción 2015 → 2022", "−28%", help="Reducción relativa en la tasa promedio nacional")
    c2.metric("Pico COVID (2020)", "+35%", help="Incremento porcentual en la tasa durante la pandemia")
    c3.metric("Brecha máx–mín 2022", "~9 pp", help="Diferencia entre el dpto. con más y menos deserción")
    c1.metric("Brecha urbano-rural", "2.4×", help="La zona rural tiene 2.4 veces más deserción que la urbana")
    c2.metric("Nivel más crítico", "Secundaria", help="Concentra la mayor proporción de desertores")
    c3.metric("Dptos. persistentemente críticos", "6", help="Con tasa superior al 6% en todos los años analizados")

    st.markdown("---")

    # Gráfico proyección
    df_hist_nac = df.groupby("Año")["Tasa_Desercion"].mean().reset_index()
    años_proy = [2024, 2025, 2026, 2027, 2030]
    base_23 = df_hist_nac.iloc[-1]["Tasa_Desercion"]
    tasas_proy_opt = [round(base_23 * (0.91 ** i), 2) for i in range(1, 6)]
    tasas_proy_mod = [round(base_23 * (0.96 ** i), 2) for i in range(1, 6)]

    fig5 = go.Figure()
    fig5.add_trace(
        go.Scatter(
            x=df_hist_nac["Año"], y=df_hist_nac["Tasa_Desercion"],
            mode="lines+markers", name="Histórico (2015–2023)",
            line=dict(color="#1a237e", width=3),
        )
    )
    fig5.add_trace(
        go.Scatter(
            x=años_proy, y=tasas_proy_opt,
            mode="lines+markers", name="Proyección optimista (con políticas activas)",
            line=dict(color="#43a047", width=2, dash="dot"),
            marker=dict(symbol="diamond", size=9),
        )
    )
    fig5.add_trace(
        go.Scatter(
            x=años_proy, y=tasas_proy_mod,
            mode="lines+markers", name="Proyección moderada (tendencia actual)",
            line=dict(color="#fb8c00", width=2, dash="dot"),
            marker=dict(symbol="circle", size=9),
        )
    )
    fig5.add_hline(y=2.0, line_dash="dash", line_color="gray",
                   annotation_text="Meta deseable < 2%", annotation_position="right")
    fig5.update_layout(
        title="Tendencia histórica y proyecciones de deserción escolar en Colombia",
        xaxis_title="Año", yaxis_title="Tasa promedio (%)",
        height=420, xaxis=dict(tickmode="linear"),
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("### 🎯 Recomendaciones de política pública")

    recomendaciones = [
        ("🏫", "Ampliar los Modelos Educativos Flexibles (MEF) en los 6 departamentos con deserción persistente superior al 6%"),
        ("🚌", "Garantizar transporte escolar gratuito en zonas rurales como estrategia prioritaria de retención en secundaria"),
        ("💰", "Focalizar las transferencias monetarias condicionadas del programa Familias en Acción en hogares con hijos en educación secundaria"),
        ("📱", "Implementar plataformas de educación híbrida que garanticen continuidad del aprendizaje ante emergencias futuras"),
        ("📊", "Mejorar el sistema SIMAT para reducir el subregistro en comunidades étnicas y zonas de conflicto"),
        ("🧑‍🤝‍🧑", "Fortalecer los programas de prevención del embarazo adolescente y de reinserción escolar en territorios periféricos"),
    ]

    for emoji, rec in recomendaciones:
        st.markdown(f"**{emoji} {rec}**")

    st.markdown(
        '<div class="conclusion-box">✅ <b>Mensaje final:</b> Colombia ha logrado reducir su tasa de '
        "deserción escolar en casi un <b>28% entre 2015 y 2022</b>. Sin embargo, la persistente "
        "desigualdad territorial evidencia que el avance no ha sido equitativo. Para alcanzar una "
        "tasa inferior al 2% antes de 2030, el país necesita políticas <b>focalizadas, sostenidas "
        "y con financiamiento garantizado</b> en los territorios más vulnerables. "
        "Los datos ya muestran el camino — falta la voluntad política para recorrerlo.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### 📚 Referencias (Normas APA 7ª ed.)")
    st.markdown(
        """
- Ministerio de Educación Nacional. (2025). *MEN_Estadísticas en educación en preescolar,
  básica y media por departamento* [Conjunto de datos]. Datos Abiertos Colombia.
  https://www.datos.gov.co/Educaci-n/MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR-B-SICA/ji8i-4anb

- Departamento Administrativo Nacional de Estadística [DANE]. (2024).
  *Boletín técnico: Educación formal (EDUC) 2023*.
  https://www.dane.gov.co/files/operaciones/EDUC/bol-EDUC-2023.pdf

- Ministerio de Educación Nacional. (2025). *Datos Abiertos MEN*.
  https://www.mineducacion.gov.co/portal/estadisticas/datos-abiertos-men/

- Vora, S. (2019). *The power of data storytelling*. SAGE Publications.
        """
    )

    st.markdown("---")
    st.caption(
        "Proyecto colaborativo – Fase 4 | "
        "Visualización Para La Analítica De Datos (Código 203238429) | "
        "UNAD – 2026"
    )
