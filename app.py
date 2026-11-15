# !pip install streamlit
import streamlit as st
import math

st.set_page_config(page_title="Algoritmo Pro de Apuestas", page_icon="⚽", layout="wide")

st.title("⚽ ALGORITMO PRO DE APUESTAS - HONDUBET STYLE")
st.write("Versión Avanzada con Análisis de Mercados, Goles y Goleadores")

# Sidebar o pestañas para filtrar el tipo de análisis de mercado
st.sidebar.header("🎯 Configuración de Mercado")
mercado_seleccionado = st.sidebar.selectbox(
    "Selecciona el enfoque de análisis:",
    [
        "Todos los Mercados (General)",
        "Resultado y Doble Oportunidad (1X2)",
        "Goles y Totales (Over/Under y BTTS)",
        "Goleadores y Rendimiento Individual",
        "Hándicaps y Márgenes",
    ]
)

equipo_a = st.text_input("Equipo A (Local)", "Toluca Femenil")
equipo_b = st.text_input("Equipo B (Visitante)", "America Femenil")

col1, col2 = st.columns(2)
with col1:
    st.subheader(equipo_a)
    v_a = st.slider(f"Victorias {equipo_a}", 0, 10, 4)
    e_a = st.slider(f"Empates {equipo_a}", 0, 10, 2)
    gf_a = st.number_input(f"Goles a favor {equipo_a}", value=20)
    gc_a = st.number_input(f"Goles en contra {equipo_a}", value=21)
    motiv_a = st.slider(f"Motivacion {equipo_a}", -10, 15, 15)
    jugador_estrella_a = st.text_input(f"Delantero Clave de {equipo_a}", "Delantero Principal A")

with col2:
    st.subheader(equipo_b)
    v_b = st.slider(f"Victorias {equipo_b}", 0, 10, 8)
    e_b = st.slider(f"Empates {equipo_b}", 0, 10, 1)
    gf_b = st.number_input(f"Goles a favor {equipo_b}", value=32)
    gc_b = st.number_input(f"Goles en contra {equipo_b}", value=9)
    motiv_b = st.slider(f"Motivacion {equipo_b}", -10, 15, -5)
    jugador_estrella_b = st.text_input(f"Delantero Clave de {equipo_b}", "Delantero Principal B")

if st.button("CALCULAR APUESTA PROFESIONAL"):
    # Cálculo ponderado de goles esperados incluyendo motivación
    factor_motiv_a = motiv_a * 0.02
    factor_motiv_b = motiv_b * 0.02
    
    exp_a = max(0.2, ((gf_a/10 + gc_b/10)/2) + 0.35 + factor_motiv_a)
    exp_b = max(0.2, ((gf_b/10 + gc_a/10)/2) - 0.15 + factor_motiv_b)
    total_goles = exp_a + exp_b
    
    st.markdown("---")
    st.subheader("📊 Resultados del Análisis Estadístico")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.success(f"**Goles Esperados:**\n- {equipo_a}: **{round(exp_a,2)}**\n- {equipo_b}: **{round(exp_b,2)}**")
    with col_res2:
        st.success(f"**Total Goles Proyectados:** **{round(total_goles,2)}**")

    st.markdown("---")
    st.subheader("💡 Sugerencias de Apuesta por Categoría")

    # 1. MERCADOS DE RESULTADO Y 1X2
    if mercado_seleccionado in ["Todos los Mercados (General)", "Resultado y Doble Oportunidad (1X2)"]:
        st.markdown("### 🏟️ 1. Resultado y Doble Oportunidad")
        if exp_a > exp_b + 0.4:
            st.write(f"✅ **Ganador Principal / 1X2:** Gana **{equipo_a}** (Local)")
            st.write(f"✅ **Doble Oportunidad:** **1X** ({equipo_a} o Empate)")
        elif exp_b > exp_a + 0.4:
            st.write(f"✅ **Ganador Principal / 1X2:** Gana **{equipo_b}** (Visitante)")
            st.write(f"✅ **Doble Oportunidad:** **X2** ({equipo_b} o Empate)")
        else:
            st.write(f"✅ **Doble Oportunidad Recomendada:** **1X** o Partido muy reñido (Considerar *Apuesta sin Empate / DNB*)")

    # 2. GOLES Y TOTALES (OVER / UNDER Y BTTS)
    if mercado_seleccionado in ["Todos los Mercados (General)", "Goles y Totales (Over/Under y BTTS)"]:
        st.markdown("### ⚽ 2. Goles y Totales (Over/Under)")
        prob_over = round(min(total_goles/3.5*100, 90), 1)
        if total_goles > 2.5:
            st.write(f"✅ **Línea de Goles:** **OVER 2.5 GOLES** (Probabilidad estimada: {prob_over}%)")
        else:
            st.write(f"✅ **Línea de Goles:** **UNDER 2.5 GOLES**")
            
        if exp_a > 0.8 and exp_b > 0.8:
            st.write("✅ **Ambos Equipos Anotan (BTTS):** **SÍ (GG)** — Alta probabilidad de que ambos marquen.")
        else:
            st.write("✅ **Ambos Equipos Anotan (BTTS):** **NO (NG)** — Es probable que al menos un arco quede en cero.")

    # 3. GOLEADORES Y RENDIMIENTO INDIVIDUAL
    if mercado_seleccionado in ["Todos los Mercados (General)", "Goleadores y Rendimiento Individual"]:
        st.markdown("### 🎯 3. Mercados de Goleadores (Player Props)")
        if exp_a >= exp_b:
            st.write(f"✅ **Goleador en Cualquier Momento (Anytime):** **{jugador_estrella_a}** ({equipo_a}) por volumen ofensivo esperado.")
            st.write(f"✅ **Primer Goleador Probable:** **{jugador_estrella_a}** (Dado que se proyecta que {equipo_a} anote primero).")
        else:
            st.write(f"✅ **Goleador en Cualquier Momento (Anytime):** **{jugador_estrella_b}** ({equipo_b}).")
            st.write(f"✅ **Primer Goleador Probable:** **{jugador_estrella_b}**.")
        st.write("💡 *Consejo Hondubet:* Revisa cuotas de 'Doblete' si el delantero clave tiene alta motivación o rival directo débil.")

    # 4. HÁNDICAPS Y MÁRGENES
    if mercado_seleccionado in ["Todos los Mercados (General)", "Hándicaps y Márgenes"]:
        st.markdown("### ⚖️ 4. Hándicaps y Margen de Victoria")
        diferencia = abs(exp_a - exp_b)
        if diferencia > 1.0:
            equipo_favorito = equipo_a if exp_a > exp_b else equipo_b
            st.write(f"✅ **Hándicap Europeo / Asiático:** Considerar **{equipo_favorito} -1.0** debido a la superioridad proyectada.")
        else:
            st.write("✅ **Hándicap:** Partido parejo. Ideal utilizar **Hándicap Asiático +0.5** o evitar líneas amplias.")
            
        st.write(f"✅ **Margen de Victoria Estimado:** El equipo ganador podría imponerse por una diferencia de **{round(diferencia, 1)} a 2 goles**.")
