# !pip install streamlit
import streamlit as st
import math

st.set_page_config(page_title="Algoritmo Pro de Apuestas - Hondubet", page_icon="⚽", layout="wide")

st.title("⚽ ALGORITMO PRO DE APUESTAS & PROBABILIDADES")
st.write("Análisis basado en rendimiento de 10 partidos, métricas de mercado, córners, tarjetas y factores externos.")

# Sidebar de selección de mercado
st.sidebar.header("🎯 Enfoque de Análisis")
mercado_seleccionado = st.sidebar.selectbox(
    "Selecciona el mercado a evaluar:",
    [
        "Todos los Mercados (General)",
        "Resultado 1X2 y Doble Oportunidad",
        "Goles (Over/Under y BTTS)",
        "Córners y Tarjetas",
        "Goleadores y Rendimiento Individual"
    ]
)

# Configuración de Equipos
col_eq1, col_eq2 = st.columns(2)
with col_eq1:
    equipo_a = st.text_input("Equipo A (Local)", "Toluca Femenil")
with col_eq2:
    equipo_b = st.text_input("Equipo B (Visitante)", "America Femenil")

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📊 Estadísticas (Últimos 10 Partidos) - {equipo_a}")
    v_a = st.slider(f"Victorias de {equipo_a} (de 10)", 0, 10, 6)
    e_a = st.slider(f"Empates de {equipo_a} (de 10)", 0, 10, 2)
    d_a = 10 - (v_a + e_a)
    st.text(f"Derrotas calculadas: {d_a}")
    
    gf_a = st.number_input(f"Goles a favor totales (10 part) {equipo_a}", value=18)
    gc_a = st.number_input(f"Goles en contra totales (10 part) {equipo_a}", value=10)
    
    st.markdown("### 📐 Métricas Tácticas y Disciplinarias")
    corners_a = st.number_input(f"Promedio de córners a favor ({equipo_a})", value=5.5)
    amarillas_a = st.number_input(f"Promedio de tarjetas amarillas ({equipo_a})", value=2.1)
    rojas_a = st.number_input(f"Total tarjetas rojas recientes ({equipo_a})", value=0)
    
    st.markdown("### 🏥 Bajas y Entorno")
    lesiones_a = st.text_area(f"Lesiones / Suspendidos clave en {equipo_a}", "Delantero titular en duda por molestia muscular.")
    noticias_a = st.text_area(f"Noticias / Motivación ({equipo_a})", "Buen ambiente interno, racha positiva en casa.")
    jugador_estrella_a = st.text_input(f"Delantero Clave de {equipo_a}", "Delantero Principal A")

with col2:
    st.subheader(f"📊 Estadísticas (Últimos 10 Partidos) - {equipo_b}")
    v_b = st.slider(f"Victorias de {equipo_b} (de 10)", 0, 10, 5)
    e_b = st.slider(f"Empates de {equipo_b} (de 10)", 0, 10, 3)
    d_b = 10 - (v_b + e_b)
    st.text(f"Derrotas calculadas: {d_b}")
    
    gf_b = st.number_input(f"Goles a favor totales (10 part) {equipo_b}", value=15)
    gc_b = st.number_input(f"Goles en contra totales (10 part) {equipo_b}", value=12)
    
    st.markdown("### 📐 Métricas Tácticas y Disciplinarias")
    corners_b = st.number_input(f"Promedio de córners a favor ({equipo_b})", value=4.2)
    amarillas_b = st.number_input(f"Promedio de tarjetas amarillas ({equipo_b})", value=2.6)
    rojas_b = st.number_input(f"Total tarjetas rojas recientes ({equipo_b})", value=1)
    
    st.markdown("### 🏥 Bajas y Entorno")
    lesiones_b = st.text_area(f"Lesiones / Suspendidos clave en {equipo_b}", "Defensa central titular suspendido por acumulación.")
    noticias_b = st.text_area(f"Noticias / Motivación ({equipo_b})", "Presión externa por malos resultados fuera de casa.")
    jugador_estrella_b = st.text_input(f"Delantero Clave de {equipo_b}", "Delantero Principal B")

if st.button("🚀 CALCULAR PROBABILIDADES DE APUESTA"):
    
    # Ponderación basada en los últimos 10 partidos (Forma reciente = Puntos obtenidos / 30 * 100)
    puntos_a = (v_a * 3) + (e_a * 1)
    puntos_b = (v_b * 3) + (e_b * 1)
    
    # Ajuste por lesiones y noticias (penalización o bono simple de goles esperados)
    ajuste_a = 0.1 if "buen" in noticias_a.lower() or "racha" in noticias_a.lower() else 0.0
    ajuste_a -= 0.2 if "lesión" in lesiones_a.lower() or "duda" in lesiones_a.lower() else 0.0
    
    ajuste_b = 0.1 if "buen" in noticias_b.lower() else 0.0
    ajuste_b -= 0.2 if "lesión" in lesiones_b.lower() or "suspendido" in lesiones_b.lower() else 0.0

    # Cálculo de goles esperados con base en los últimos 10 partidos
    exp_a = max(0.3, ((gf_a / 10 + gc_b / 10) / 2) + 0.25 + ajuste_a)
    exp_b = max(0.3, ((gf_b / 10 + gc_a / 10) / 2) - 0.10 + ajuste_b)
    total_goles_est = exp_a + exp_b
    
    # Córners y Tarjetas estimadas
    total_corners_est = corners_a + corners_b
    total_amarillas_est = amarillas_a + amarillas_b + (rojas_a + rojas_b) * 0.5

    st.markdown("---")
    st.subheader("📈 Resultados del Modelo Predictivo")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.info(f"**Forma Reciente (Últimos 10):**\n- {equipo_a}: {puntos_a} pts\n- {equipo_b}: {puntos_b} pts")
    with col_res2:
        st.success(f"**Goles Proyectados:**\n- {equipo_a}: **{round(exp_a,2)}**\n- {equipo_b}: **{round(exp_b,2)}**\n- Total: **{round(total_goles_est,2)}**")
    with col_res3:
        st.warning(f"**Estadísticas del Juego:**\n- Córners Totales Est.: **{round(total_corners_est, 1)}**\n- Tarjetas Est.: **{round(total_amarillas_est, 1)}**")

    st.markdown("---")
    st.subheader("💡 Sugerencias de Apuestas Optimizadas para Hondubet")

    # 1. MERCADO 1X2 Y DOBLE OPORTUNIDAD
    if mercado_seleccionado in ["Todos los Mercados (General)", "Resultado 1X2 y Doble Oportunidad"]:
        st.markdown("### 🏟️ 1. Resultado 1X2 y Doble Oportunidad")
        if puntos_a > puntos_b + 3 and exp_a > exp_b:
            st.write(f"✅ **Apuesta sugerida:** Gana **{equipo_a}** (Cuota estimada valor local).")
            st.write(f"✅ **Doble Oportunidad segura:** **1X** ({equipo_a} o Empate).")
        elif puntos_b > puntos_a + 3 and exp_b > exp_a:
            st.write(f"✅ **Apuesta sugerida:** Gana **{equipo_b}** o **X2** (Visitante fuerte en últimos 10).")
        else:
            st.write(f"✅ **Apuesta sugerida:** Partido parejo. Considerar **Apuesta sin Empate (DNB)** o Doble Oportunidad **1X**.")

    # 2. MERCADO DE GOLES
    if mercado_seleccionado in ["Todos los Mercados (General)", "Goles (Over/Under y BTTS)"]:
        st.markdown("### ⚽ 2. Línea de Goles y Ambos Marcan")
        if total_goles_est > 2.6:
            st.write(f"✅ **Mercado Over/Under:** **Más de 2.5 Goles** (Proyección sólida de {round(total_goles_est,2)} tantos).")
        else:
            st.write(f"✅ **Mercado Over/Under:** **Menos de 2.5 Goles** (Tendencia de partidos cerrados).")
            
        if exp_a > 0.9 and exp_b > 0.9:
            st.write("✅ **Ambos Equipos Marcan (BTTS):** **SÍ (GG)** — Las defensas recientes conceden espacios.")
        else:
            st.write("✅ **Ambos Equipos Marcan (BTTS):** **NO (NG)** — Riesgo alto de arco en cero.")

    # 3. CÓRNERS Y TARJETAS
    if mercado_seleccionado in ["Todos los Mercados (General)", "Córners y Tarjetas"]:
        st.markdown("### 📐 3. Córners y Amonestaciones")
        if total_corners_est > 9.5:
            st.write(f"✅ **Tiros de Esquina:** **Más de 9.5 Córners** (Promedio combinado alto de {round(total_corners_est, 1)}).")
        else:
            st.write(f"✅ **Tiros de Esquina:** **Menos de 9.5 / 8.5 Córners**.")
            
        if total_amarillas_est > 4.5:
            st.write(f"✅ **Tarjetas:** Alta fricción esperada. Considerar **Más de 3.5 / 4.5 Tarjetas Amarillas**.")
        else:
            st.write(f"✅ **Tarjetas:** Partido de pierna moderada.")

    # 4. GOLEADORES
    if mercado_seleccionado in ["Todos los Mercados (General)", "Goleadores y Rendimiento Individual"]:
        st.markdown("### 🎯 4. Goleadores (Player Props)")
        if exp_a >= exp_b:
            st.write(f"✅ **Candidato a Goleador (Anytime):** **{jugador_estrella_a}** ({equipo_a}), respaldado por las bajas defensivas del rival y localía.")
        else:
            st.write(f"✅ **Candidato a Goleador (Anytime):** **{jugador_estrella_b}** ({equipo_b}).")
