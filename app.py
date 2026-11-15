import streamlit as st
import math

st.set_page_config(page_title="Algoritmo PRO V3", page_icon="🏆")
st.title("🏆 ALGORITMO PRO V3")
st.write("Poisson + xG + Valor vs Casa de Apuestas")

equipos = {
    "Real Madrid": [1950, 1.25, 0.85],
    "Barcelona": [1940, 1.22, 0.88],
    "Man City": [1960, 1.30, 0.82],
    "Liverpool": [1920, 1.20, 0.90],
    "Arsenal": [1900, 1.15, 0.85],
    "Bayern": [1910, 1.28, 0.95],
    "PSG": [1890, 1.20, 0.92],
    "Inter": [1880, 1.10, 0.82],
    "Chelsea": [1870, 1.05, 0.92],
    "Argentina": [1920, 1.15, 0.85],
    "Brasil": [1880, 1.12, 0.90],
    "España": [1910, 1.18, 0.82],
    "Francia": [1900, 1.18, 0.88],
    "Inglaterra": [1890, 1.12, 0.88],
    "México": [1750, 0.95, 1.0],
    "USA": [1740, 0.92, 1.02],
    "Nueva Zelanda": [1580, 0.85, 1.10],
    "India": [1350, 0.60, 1.35],
    "Honduras": [1480, 0.75, 1.15],
    "Costa Rica": [1550, 0.82, 1.05],
    "Panamá": [1560, 0.85, 1.02],
    "Colombia": [1780, 1.0, 0.95],
    "Uruguay": [1800, 1.02, 0.90],
    "Japón": [1790, 1.05, 0.92],
}

def poisson(lam, k):
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)

col1, col2 = st.columns(2)
with col1:
    eq_local = st.selectbox("Equipo Local", list(equipos.keys()), index=0)
    forma_local = st.slider("Forma Local (0-15)", 0, 15, 10)
    bajas_local = st.slider("Bajas Local (0-5)", 0, 5, 0)
with col2:
    eq_visit = st.selectbox("Equipo Visitante", list(equipos.keys()), index=1)
    forma_visit = st.slider("Forma Visitante (0-15)", 0, 15, 10)
    bajas_visit = st.slider("Bajas Visitante (0-5)", 0, 5, 0)

st.subheader("Cuotas de la Casa")
c1, c2, c3 = st.columns(3)
with c1:
    cuota_local = st.number_input("Cuota Gana Local", 1.01, 20.0, 1.85)
with c2:
    cuota_empate = st.number_input("Cuota Empate", 1.01, 20.0, 3.40)
with c3:
    cuota_visit = st.number_input("Cuota Gana Visita", 1.01, 20.0, 4.20)

if st.button("ANALIZAR PARTIDO PRO"):
    elo_l, atq_l, def_l = equipos[eq_local]
    elo_v, atq_v, def_v = equipos[eq_visit]

    elo_l_adj = elo_l + 75 + (forma_local - 7.5) * 10 - (bajas_local * 25)
    elo_v_adj = elo_v + (forma_visit - 7.5) * 10 - (bajas_visit * 25)
    diff = elo_l_adj - elo_v_adj

    xg_local = max(0.15, 1.35 * atq_l * def_v * (1 + diff / 1200))
    xg_visit = max(0.15, 1.15 * atq_v * def_l * (1 - diff / 1200))

    prob_local = 0
    prob_empate = 0
    prob_visit = 0
    prob_over25 = 0
    prob_btts = 0
    marcadores = []

    for gL in range(0, 6):
        for gV in range(0, 6):
            p = poisson(xg_local, gL) * poisson(xg_visit, gV)
            marcadores.append((p, gL, gV))
            if gL > gV:
                prob_local += p
            elif gL == gV:
                prob_empate += p
            else:
                prob_visit += p
            if gL + gV > 2.5:
                prob_over25 += p
            if gL > 0 and gV > 0:
                prob_btts += p

    marcadores = sorted(marcadores, reverse=True)[:3]

    st.subheader(f"{eq_local} vs {eq_visit}")
    st.write(f"xG: {eq_local} {xg_local:.2f} - {xg_visit:.2f} {eq_visit}")

    m1, m2, m3 = st.columns(3)
    m1.metric("Gana Local", f"{prob_local*100:.1f}%")
    m2.metric("Empate", f"{prob_empate*100:.1f}%")
    m3.metric("Gana Visita", f"{prob_visit*100:.1f}%")

    st.write("Top 3 Marcadores Mas Probables")
    for p, gL, gV in marcadores:
        st.write(f"{gL} - {gV} : {p*100:.1f}%")

    st.write(f"Over 2.5 Goles: {prob_over25*100:.1f}%")
    st.write(f"Ambos Anotan: {prob_btts*100:.1f}%")

    st.write("Detector de VALOR")
    vL = (prob_local * cuota_local - 1) * 100
    vE = (prob_empate * cuota_empate - 1) * 100
    vV = (prob_visit * cuota_visit - 1) * 100

    st.write(f"Gana {eq_local}: {vL:.1f}% de valor")
    st.write(f"Empate: {vE:.1f}% de valor")
    st.write(f"Gana {eq_visit}: {vV:.1f}% de valor")

    if vL > 5:
        st.success(f"VALOR EN {eq_local} - Apostar!")
    if vE > 5:
        st.success("VALOR EN Empate - Apostar!")
    if vV > 5:
        st.success(f"VALOR EN {eq_visit} - Apostar!")

    if prob_over25 > 0.60:
        st.success("APUESTA: Over 2.5 Goles")
    elif prob_btts > 0.60:
        st.success("APUESTA: Ambos Anotan")
    else:
        st.warning("PARTIDO TRAMPA - Mejor Doble Oportunidad")
