import streamlit as st
import math

st.set_page_config(page_title="ALGORITMO V6", page_icon="🏆", layout="wide")
st.title("🏆 ALGORITMO V6 - TODO EN BLANCO")
st.write("Tú llenas todo. Aquí no hay nada predeterminado.")

def poisson(lam, k):
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)

st.header("1. TUS EQUIPOS - ESCRÍBELOS TÚ")

c1, c2 = st.columns(2)
with c1:
    eq_local = st.text_input("🏠 Nombre Equipo Local", value="", placeholder="Escribe aquí...")
    fuerza_local = st.number_input("Fuerza Local (1-100)", min_value=1, max_value=100, value=None, placeholder="Ej: 80")
    atq_local = st.number_input("Ataque Local (1-100)", min_value=1, max_value=100, value=None, placeholder="Ej: 70")
    def_local = st.number_input("Defensa Local (1-100)", min_value=1, max_value=100, value=None, placeholder="Ej: 75")
    forma_local = st.number_input("Forma Local (0-15 pts)", min_value=0, max_value=15, value=None, placeholder="Ej: 10")
    bajas_local = st.number_input("Bajas Local (0-5)", min_value=0, max_value=5, value=None, placeholder="Ej: 0")

with c2:
    eq_visit = st.text_input("✈️ Nombre Equipo Visitante", value="", placeholder="Escribe aquí...")
    fuerza_visit = st.number_input("Fuerza Visitante (1-100)", min_value=1, max_value=100, value=None, placeholder="Ej: 40")
    atq_visit = st.number_input("Ataque Visitante (1-100)", min_value=1, max_value=100, value=None, placeholder="Ej: 35")
    def_visit = st.number_input("Defensa Visitante (1-100)", min_value=1, max_value=100, value=None, placeholder="Ej: 30")
    forma_visit = st.number_input("Forma Visitante (0-15 pts)", min_value=0, max_value=15, value=None, placeholder="Ej: 8")
    bajas_visit = st.number_input("Bajas Visitante (0-5)", min_value=0, max_value=5, value=None, placeholder="Ej: 1")

st.header("2. CUOTAS DE TU CASA - ESCRÍBELAS TÚ")
cc1, cc2, cc3, cc4, cc5 = st.columns(5)
with cc1: cuota_local = st.number_input("Cuota Local", min_value=1.01, max_value=20.0, value=None, placeholder="Ej: 1.50")
with cc2: cuota_empate = st.number_input("Cuota Empate", min_value=1.01, max_value=20.0, value=None, placeholder="Ej: 3.80")
with cc3: cuota_visit = st.number_input("Cuota Visita", min_value=1.01, max_value=20.0, value=None, placeholder="Ej: 6.00")
with cc4: cuota_over25 = st.number_input("Cuota Over 2.5", min_value=1.01, max_value=20.0, value=None, placeholder="Ej: 1.90")
with cc5: cuota_btts = st.number_input("Cuota Ambos Anotan", min_value=1.01, max_value=20.0, value=None, placeholder="Ej: 1.80")

tu_banca = st.number_input("Tu Banca ($)", min_value=1, value=None, placeholder="Ej: 100")

if st.button("🔥 ANALIZAR TODO", type="primary"):
    faltan = []
    if not eq_local: faltan.append("Nombre Local")
    if not eq_visit: faltan.append("Nombre Visitante")
    if fuerza_local is None: faltan.append("Fuerza Local")
    if fuerza_visit is None: faltan.append("Fuerza Visitante")
    if atq_local is None: faltan.append("Ataque Local")
    if atq_visit is None: faltan.append("Ataque Visitante")
    if def_local is None: faltan.append("Defensa Local")
    if def_visit is None: faltan.append("Defensa Visitante")
    if forma_local is None: faltan.append("Forma Local")
    if forma_visit is None: faltan.append("Forma Visitante")
    if bajas_local is None: faltan.append("Bajas Local")
    if bajas_visit is None: faltan.append("Bajas Visitante")
    if cuota_local is None: faltan.append("Cuota Local")
    if cuota_empate is None: faltan.append("Cuota Empate")
    if cuota_visit is None: faltan.append("Cuota Visita")
    if cuota_over25 is None: faltan.append("Cuota Over 2.5")
    if cuota_btts is None: faltan.append("Cuota Ambos Anotan")
    if tu_banca is None: faltan.append("Tu Banca")

    if faltan:
        st.error(f"⚠️ Te falta llenar esto: {', '.join(faltan)}")
    else:
        elo_l = 1300 + fuerza_local * 7
        elo_v = 1300 + fuerza_visit * 7
        atq_l = atq_local / 50
        atq_v = atq_visit / 50
        def_l = (100 - def_local) / 50 + 0.5
        def_v = (100 - def_visit) / 50 + 0.5

        elo_l_adj = elo_l + 75 + (forma_local - 7.5) * 10 - (bajas_local * 25)
        elo_v_adj = elo_v + (forma_visit - 7.5) * 10 - (bajas_visit * 25)
        diff = elo_l_adj - elo_v_adj

        xg_local = max(0.15, 1.35 * atq_l * def_v * (1 + diff / 1200))
        xg_visit = max(0.15, 1.15 * atq_v * def_l * (1 - diff / 1200))

        pL = pE = pV = 0
        p_over15 = p_over25 = p_over35 = p_btts = 0
        p_under25 = 0
        marcadores = []
        for gL in range(0, 7):
            for gV in range(0, 7):
                p = poisson(xg_local, gL) * poisson(xg_visit, gV)
                marcadores.append((p, gL, gV))
                if gL > gV: pL += p
                elif gL == gV: pE += p
                else: pV += p
                total = gL + gV
                if total > 1.5: p_over15 += p
                if total > 2.5: p_over25 += p
                else: p_under25 += p
                if total > 3.5: p_over35 += p
                if gL > 0 and gV > 0: p_btts += p

        marcadores = sorted(marcadores, reverse=True)[:5]
        confianza = max(pL, pE, pV) * 100

        st.header(f"📊 {eq_local} vs {eq_visit}")
        st.write(f"xG Total: {xg_local + xg_visit:.2f}")

        st.subheader("RESULTADO 1X2")
        a, b, c = st.columns(3)
        a.metric(f"Gana {eq_local}", f"{pL*100:.1f}%", f"Justa {1/max(pL,0.01):.2f}")
        b.metric("Empate", f"{pE*100:.1f}%", f"Justa {1/max(pE,0.01):.2f}")
        c.metric(f"Gana {eq_visit}", f"{pV*100:.1f}%", f"Justa {1/max(pV,0.01):.2f}")

        st.subheader("GOLES ESPERADOS (xG)")
        st.write(f"**{eq_local}:** {xg_local:.2f} | **{eq_visit}:** {xg_visit:.2f}")

        st.subheader("TOP 5 MARCADORES EXACTOS")
        for p, gL, gV in marcadores:
            st.write(f"**{gL} - {gV}** -> {p*100:.1f}% | Cuota justa {1/max(p,0.01):.2f}")

        st.subheader("OVER / UNDER Y AMBOS ANOTAN")
        st.write(f"Over 1.5: {p_over15*100:.1f}% | Over 2.5: {p_over25*100:.1f}% | Under 2.5: {p_under25*100:.1f}% | Over 3.5: {p_over35*100:.1f}%")
        st.write(f"Ambos Anotan SI: {p_btts*100:.1f}% | NO: {(1-p_btts)*100:.1f}%")
        st.write(f"Doble 1X: {(pL+pE)*100:.1f}% | X2: {(pV+pE)*100:.1f}% | 12: {(pL+pV)*100:.1f}%")

        st.subheader("ESTADÍSTICAS ESTIMADAS")
        st.write(f"Tiros: {eq_local} {round(xg_local*7.5)} - {round(xg_visit*7.5)} {eq_visit}")
        st.write(f"Corners Total: {round(8+(xg_local+xg_visit)*2.5)}")

        st.subheader("💰 DETECTOR DE VALOR")
        vL = (pL * cuota_local - 1) * 100
        vE = (pE * cuota_empate - 1) * 100
        vV = (pV * cuota_visit - 1) * 100
        vO = (p_over25 * cuota_over25 - 1) * 100
        vB = (p_btts * cuota_btts - 1) * 100
        st.write(f"Valor Gana {eq_local}: {vL:.1f}% | Empate: {vE:.1f}% | Gana {eq_visit}: {vV:.1f}%")
        st.write(f"Valor Over 2.5: {vO:.1f}% | Valor Ambos Anotan: {vB:.1f}%")

        st.subheader("🎯 TUS 5 MEJORES APUESTAS")
        apuestas = sorted([(vL, f"Gana {eq_local} @ {cuota_local}"), (vE, f"Empate @ {cuota_empate}"), (vV, f"Gana {eq_visit} @ {cuota_visit}"), (vO, f"Over 2.5 @ {cuota_over25}"), (vB, f"Ambos Anotan @ {cuota_btts}")], reverse=True)
        for i, (val, nombre) in enumerate(apuestas, 1):
            emoji = "🟢" if val > 5 else ("🟡" if val > 0 else "🔴")
            st.write(f"{i}. {emoji} {nombre} - Valor {val:.1f}%")

        st.subheader("🧠 CONFIANZA Y CUÁNTO APOSTAR")
        st.write(f"Confianza: {confianza:.1f}%")
        if confianza > 60:
            st.success(f"ALTA - Apuesta 5%: ${tu_banca*0.05:.2f}")
        elif confianza > 45:
            st.warning(f"MEDIA - Apuesta 2%: ${tu_banca*0.02:.2f}")
        else:
            st.error(f"BAJA - PARTIDO TRAMPA - Solo 1% o no apuestes: ${tu_banca*0.01:.2f}")
