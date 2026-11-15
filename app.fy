import streamlit as st
import math

st.set_page_config(page_title="Algoritmo PRO V3", page_icon="🏆")
st.title("🏆 ALGORITMO PRO V3 - Nivel Profesional")
st.write("Poisson + xG + Valor vs Casa de Apuestas")

# Equipo: [Elo, Ataque, Defensa]
equipos = {
    "Real Madrid": [1950, 1.25, 0.85], "Barcelona": [1940, 1.22, 0.88],
    "Man City": [1960, 1.30, 0.82], "Liverpool": [1920, 1.20, 0.90],
    "Arsenal": [1900, 1.15, 0.85], "Bayern": [1910, 1.28, 0.95],
    "PSG": [1890, 1.20, 0.92], "Inter": [1880, 1.10, 0.82],
    "Chelsea": [1870, 1.05, 0.92], "Dortmund": [1840, 1.10, 1.0],
    "Juventus": [1830, 1.0, 0.85], "Milan": [1820, 1.02, 0.90],
    "Atlético Madrid": [1860, 0.98, 0.78], "Tottenham": [1830, 1.08, 1.02],
    "Argentina": [1920, 1.15, 0.85], "Brasil": [1880, 1.12, 0.90],
    "España": [1910, 1.18, 0.82], "Francia": [1900, 1.18, 0.88],
    "Inglaterra": [1890, 1.12, 0.88], "Alemania": [1870, 1.10, 0.95],
    "México": [1750, 0.95, 1.0], "USA": [1740, 0.92, 1.02],
    "Nueva Zelanda": [1580, 0.85, 1.10], "India": [1350, 0.60, 1.35],
    "Honduras": [1480, 0.75, 1.15], "Costa Rica": [1550, 0.82, 1.05],
    "Panamá": [1560, 0.85, 1.02], "Colombia": [1780, 1.0, 0.95],
    "Uruguay": [1800, 1.02, 0.90], "Japón": [1790, 1.05, 0.92],
}

def poisson(lam, k):
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)

col1, col2 = st.columns(2)
with col1:
    eq_local = st.selectbox("🏠 Equipo Local", list(equipos.keys()), index=0)
    forma_local = st.slider(f"Forma {eq_local} (0-15 pts)", 0, 15, 10)
    bajas_local = st.slider(f"Bajas importantes {eq_local} (0-5)", 0, 5, 0)
with col2:
    eq_visit = st.selectbox("✈️ Equipo Visitante", list(equipos.keys()), index=1)
    forma_visit = st.slider(f"Forma {eq_visit} (0-15 pts)", 0, 15, 10)
    bajas_visit = st.slider(f"Bajas importantes {eq_visit} (0-5)", 0, 5, 0)

st.subheader("🏦 Cuotas de la Casa de Apuestas (opcional)")
c1, c2, c3 = st.columns(3)
with c1: cuota_local = st.number_input("Cuota Gana Local", 1.01, 20.0, 1.85, 0.05)
with c2: cuota_empate = st.number_input("Cuota Empate", 1.01, 20.0, 3.40, 0.05)
with c3: cuota_visit = st.number_input("Cuota Gana Visita", 1.01, 20.0, 4.20, 0.05)

if st.button("🔥 ANALIZAR PARTIDO PRO", type="primary"):
    elo_l, atq_l, def_l = equipos[eq_local]
    elo_v, atq_v, def_v = equipos[eq_visit]

    # Ajustes PRO
    elo_l_adj = elo_l + 75 + (forma_local - 7.5) * 10 - (bajas_local * 25)
    elo_v_adj = elo_v + (forma_visit - 7.5) * 10 - (bajas_visit * 25)
    diff = elo_l_adj - elo_v_adj

    # xG con Ataque vs Defensa
    xg_local = max(0.15, 1.35 * atq_l * def_v * (1 + diff/1200) * (1 + (forma_local-7.5)/50))
    xg_visit = max(0.15, 1.15 * atq_v * def_l * (1 - diff/1200) * (1 + (forma_visit-7.5)/50))

    # Matriz Poisson 0-5 goles
    prob_local = prob_empate = prob_visit = 0
    prob_over25 = prob_btts = 0
    marcadores = []
    for gL in range(0, 6):
        for gV in range(0, 6):
            p = poisson(xg_local, gL) * poisson(xg_visit, gV)
            marcadores.append((p, gL, gV))
            if gL > gV: prob_local += p
            elif gL == gV: prob_empate += p
            else: prob_visit += p
            if gL + gV > 2.5: prob_over25 += p
            if gL > 0 and gV > 0: prob_btts += p

    marcadores = sorted(marcadores, reverse=True)[:3]

    st.subheader(f"{eq_local} vs {eq_visit}")
    st.write(f"**xG:** {eq_local} {xg_local:.2f} - {xg_visit:.2f} {eq_visit} | **Total xG:** {xg_local+xg_visit:.2f}")

    m1, m2, m3 = st.columns(3)
    m1.metric("Gana Local", f"{prob_local*100:.1f}%", f"Cuota justa {1/prob_local:.2f}")
    m2.metric("Empate", f"{prob_empate*100:.1f}%", f"Cuota justa {1/prob_empate:.2f}")
    m3.metric("Gana Visita", f"{prob_visit*100:.1f}%", f"Cuota justa {1/prob_visit:.2f}")

    st.write("### 🎯 Top 3 Marcadores Más Probables")
    for p, gL, gV in marcadores:
        st.write(f"**{gL} - {gV}** : {p*100:.1f}%")

    o1, o2 = st.columns(2)
    o1.metric("Over 2.5 Goles", f"{prob_over25*100:.1f}%")
    o2.metric("Ambos Anotan", f"{prob_btts*100:.1f}%")

    st.write("### 💰 Detector de VALOR")
    def valor(prob, cuota):
        v = (prob * cuota - 1) * 100
        return v
    vL = valor(prob_local, cuota_local)
    vE = valor(prob_empate, cuota_empate)
    vV = valor(prob_visit, cuota_visit)
    for nombre, v in [(f"Gana {eq_local}", vL), ("Empate", vE), (f"Gana {eq_visit}", vV)]:
        if v > 5:
            st.success(f"✅ VALOR ENCONTRADO: {nombre} -> +{v:.1f}% de valor ¡APOSTAR!")
        elif v > 0:
            st.info(f"➡️ Ligero valor: {nombre} -> +{v:.1f}%")
        else:
            st.write(f"❌ Sin valor: {nombre} -> {v:.1f}%")

    st.write("### 🧠 Recomendación PRO")
    mejor = max([(prob_local, f"Gana {eq_local}"), (prob_empate, "Empate"), (prob_visit, f"Gana {eq_visit}")])
    if mejor[0] > 0.60 and vL > 5 or vV > 5:
        st.success(f"🔥 APUESTA FUERTE: {mejor[1]} - Alta probabilidad + Valor")
    elif prob_over25 > 0.60:
        st.success("🔥 APUESTA: Over 2.5 Goles - Mucho gol esperado")
    elif prob_btts > 0.60:
        st.success("🔥 APUESTA: Ambos Anotan - Ambos atacan bien")
    else:
        st.warning("⚠️ PARTIDO TRAMPA - Mejor no apostar fuerte. Solo Doble Oportunidad.")
