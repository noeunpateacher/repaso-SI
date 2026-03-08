import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# Configuración de la página
st.set_page_config(page_title="Física en Movimiento", layout="wide")

# CSS personalizado (opcional, mejora la apariencia)
st.markdown("""
<style>
    .card {
        background: rgba(255,255,255,0.75);
        backdrop-filter: blur(4px);
        padding: 25px 20px;
        border-radius: 36px;
        box-shadow: 0 10px 20px -5px rgba(26, 59, 85, 0.2);
        border: 1px solid white;
        margin-bottom: 20px;
    }
    .card h3 {
        color: #113855;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 15px;
        border-bottom: 4px solid #3b8fc2;
        display: inline-block;
        padding-right: 20px;
    }
    .badge-ejemplo {
        background: #d4e3f0;
        border-radius: 50px;
        padding: 10px 18px;
        font-family: monospace;
        font-weight: 500;
        margin: 8px 0;
        display: inline-block;
    }
    .sub-item {
        background: #1e4e6f;
        color: white;
        padding: 10px 18px;
        border-radius: 40px;
        font-weight: 600;
        font-size: 1.1rem;
        display: inline-block;
        margin-right: 10px;
        margin-bottom: 10px;
    }
    .conv-card {
        background: white;
        border-radius: 40px;
        padding: 30px;
        box-shadow: inset 0 1px 4px #ffffff, 0 20px 30px -12px #1f3d5466;
    }
    .pasos {
        background: #f8fbfe;
        border-radius: 28px;
        padding: 25px;
        margin-top: 30px;
        font-size: 1.25rem;
        border-left: 14px solid #3b8fc2;
    }
    .footer {
        margin-top: 40px;
        text-align: center;
        color: #1d3e58;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 style='font-size: 2.4rem; color: #0b2b44; border-left: 12px solid #3b8fc2; padding-left: 15px;'>⚛️ Física en Movimiento – Repaso de Unidades y Vectores</h1>", unsafe_allow_html=True)

# Crear pestañas
tab1, tab2, tab3, tab4 = st.tabs(["📘 Teoría", "🔁 Conversor", "🧪 Laboratorio vectores", "📝 Evaluación"])

# ------------------------------------------------------------------
# Pestaña 1: Teoría
# ------------------------------------------------------------------
with tab1:
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        <div class="card">
            <h3>📏 Unidades y magnitudes</h3>
            <p><strong>Magnitud fundamental:</strong> longitud (m), masa (kg), tiempo (s).<br>
            <strong>Derivadas:</strong> velocidad (m/s), densidad (kg/m³).</p>
            <p><span class="badge-ejemplo">🚗 1228.0 km/h → m/s (factor 3.6)</span></p>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
        <div class="card">
            <h3>🔟 Prefijos (submúltiplos)</h3>
            <div>
                <span class="sub-item">milli (m) 10⁻³</span>
                <span class="sub-item">centi (c) 10⁻²</span>
                <span class="sub-item">micro (µ) 10⁻⁶</span>
                <span class="sub-item">nano (n) 10⁻⁹</span>
                <span class="sub-item">pico (p) 10⁻¹²</span>
            </div>
            <p>Ej: 1 cm = 0.01 m, 1 mg = 10⁻³ g, 1 ns = 10⁻⁹ s</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown("""
        <div class="card">
            <h3>➡️ Vectores</h3>
            <p>Componentes: A = (Ax, Ay).<br>Módulo: √(Ax²+Ay²).<br>Suma: R = (Ax+Bx , Ay+By)</p>
            <p><strong>Cifras significativas:</strong> en este laboratorio usamos 3 decimales.</p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------
# Pestaña 2: Conversor de unidades (corregido)
# ------------------------------------------------------------------
with tab2:
    st.markdown('<div class="conv-card">', unsafe_allow_html=True)

    # Inicializar valores en session_state
    if 'valor_conv' not in st.session_state:
        st.session_state.valor_conv = 1228.0
    if 'unidad_origen' not in st.session_state:
        st.session_state.unidad_origen = "km/h"
    if 'unidad_destino' not in st.session_state:
        st.session_state.unidad_destino = "m/s"
    if 'resultado_conv' not in st.session_state:
        st.session_state.resultado_conv = 0.0
        st.session_state.pasos_conv = "Presiona Convertir para ver los pasos."

    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        valor = st.number_input("Valor", value=st.session_state.valor_conv, step=0.1, format="%.4f", key="input_valor")
        st.session_state.valor_conv = valor
        unidad_origen = st.selectbox("Unidad origen", ["km/h", "m/s", "g/cm³", "kg/m³"], key="origen")
        st.session_state.unidad_origen = unidad_origen
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 3rem;'>→</h1>", unsafe_allow_html=True)
    with col3:
        unidad_destino = st.selectbox("Unidad destino", ["m/s", "km/h", "kg/m³", "g/cm³"], key="destino")
        st.session_state.unidad_destino = unidad_destino

    # Función de conversión robusta
    def convertir(val, from_u, to_u):
        # Velocidad: km/h <-> m/s (factor 3.6)
        if from_u == "km/h" and to_u == "m/s":
            res = val / 3.6
            pasos = f"{val} km/h * (1000 m/1 km) * (1 h/3600 s) = {res:.3f} m/s"
        elif from_u == "m/s" and to_u == "km/h":
            res = val * 3.6
            pasos = f"{val} m/s * (1 km/1000 m) * (3600 s/1 h) = {res:.3f} km/h"
        # Densidad: g/cm³ <-> kg/m³ (factor 1000)
        elif from_u == "g/cm³" and to_u == "kg/m³":
            res = val * 1000
            pasos = f"{val} g/cm³ * (1 kg/1000 g) * (100 cm/m)³ = {res:.3f} kg/m³"
        elif from_u == "kg/m³" and to_u == "g/cm³":
            res = val / 1000
            pasos = f"{val} kg/m³ * (1000 g/1 kg) * (1 m/100 cm)³ = {res:.3f} g/cm³"
        elif from_u == to_u:
            res = val
            pasos = f"{val} {from_u} = {res:.3f} (misma unidad)"
        else:
            res = None
            pasos = "❌ Conversión no soportada entre estas unidades."
        return res, pasos

    if st.button("Convertir", key="btn_convertir"):
        res, pasos = convertir(st.session_state.valor_conv, st.session_state.unidad_origen, st.session_state.unidad_destino)
        if res is not None:
            st.session_state.resultado_conv = res
            st.session_state.pasos_conv = pasos
        else:
            st.session_state.resultado_conv = 0.0
            st.session_state.pasos_conv = pasos
            st.warning(pasos)

    # Mostrar resultados
    st.markdown(f"### Resultado: {st.session_state.resultado_conv:.3f} {st.session_state.unidad_destino}")
    st.markdown(f'<div class="pasos"><strong>⚡ Pasos de conversión:</strong><br>{st.session_state.pasos_conv}</div>', unsafe_allow_html=True)
    st.markdown("✏️ Ejemplos: km/h → m/s (÷3.6); g/cm³ → kg/m³ (×1000).")
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------
# Pestaña 3: Laboratorio de vectores (simplificado y funcional)
# ------------------------------------------------------------------
with tab3:
    # Inicializar estado
    if 'Ax' not in st.session_state:
        st.session_state.Ax = 3.0
        st.session_state.Ay = 4.0
        st.session_state.Bx = 1.5
        st.session_state.By = 2.5

    col_izq, col_der = st.columns([1, 1.2])

    with col_izq:
        st.markdown("### Vector A")
        Ax = st.number_input("Ax", value=st.session_state.Ax, step=0.1, format="%.2f", key="Ax_input")
        Ay = st.number_input("Ay", value=st.session_state.Ay, step=0.1, format="%.2f", key="Ay_input")
        st.session_state.Ax = Ax
        st.session_state.Ay = Ay
        modA = math.hypot(Ax, Ay)
        angA = math.degrees(math.atan2(Ay, Ax))
        st.metric("Módulo |A|", f"{modA:.3f}")
        st.metric("Ángulo θ°", f"{angA:.3f}")

        st.markdown("### Vector B")
        Bx = st.number_input("Bx", value=st.session_state.Bx, step=0.1, format="%.2f", key="Bx_input")
        By = st.number_input("By", value=st.session_state.By, step=0.1, format="%.2f", key="By_input")
        st.session_state.Bx = Bx
        st.session_state.By = By
        modB = math.hypot(Bx, By)
        angB = math.degrees(math.atan2(By, Bx))
        st.metric("Módulo |B|", f"{modB:.3f}")
        st.metric("Ángulo θ°", f"{angB:.3f}")

        Rx = Ax + Bx
        Ry = Ay + By
        Rmod = math.hypot(Rx, Ry)
        st.markdown(f"### Resultado suma: R = ({Rx:.3f}, {Ry:.3f})   |R| = {Rmod:.3f}")

    with col_der:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.axvline(0, color='gray', linewidth=0.5)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_aspect('equal')
        ax.arrow(0, 0, Ax, Ay, head_width=0.3, head_length=0.3, fc='#1e72b0', ec='#1e72b0', label='A')
        ax.arrow(0, 0, Bx, By, head_width=0.3, head_length=0.3, fc='#c05a2a', ec='#c05a2a', label='B')
        ax.arrow(0, 0, Rx, Ry, head_width=0.3, head_length=0.3, fc='#2b7a4e', ec='#2b7a4e', linestyle='dashed', label='R')
        ax.legend()
        st.pyplot(fig)

# ------------------------------------------------------------------
# Pestaña 4: Evaluación (15 preguntas)
# ------------------------------------------------------------------
with tab4:
    st.markdown("## Cuestionario de 15 preguntas")
    preguntas = [
        {"q": "¿Cuál es el resultado de convertir 1228.0 km/h a m/s? (3 cifras)", "opts": ["341.111", "4420.8", "341.111 m/s", " ninguna"], "correct": 2},
        {"q": "Un submúltiplo 'centi' representa:", "opts": ["10⁻²", "10⁻³", "10⁻⁶", "10²"], "correct": 0},
        {"q": "La densidad del agua 1 g/cm³ en kg/m³ es:", "opts": ["1000", "0.001", "100", "10"], "correct": 0},
        {"q": "Si A = (3,4) y B = (1,2), la suma A+B es:", "opts": ["(4,6)", "(5,5)", "(4,5)", "(3,6)"], "correct": 0},
        {"q": "El módulo del vector (3,4) es:", "opts": ["5", "7", "25", "1"], "correct": 0},
        {"q": "¿Cuántos m/s son 100 km/h?", "opts": ["27.7778", "360", "27.7778 m/s", "0.1"], "correct": 0},
        {"q": "1 micrómetro (µm) equivale a:", "opts": ["10⁻⁶ m", "10⁻³ m", "10⁻⁹ m", "10⁻¹² m"], "correct": 0},
        {"q": "Si un vector tiene Ax= -2, Ay= 2, su ángulo es:", "opts": ["135°", "45°", "-45°", "315°"], "correct": 0},
        {"q": "Al sumar (2, -1) + (-2, 1) se obtiene:", "opts": ["(0,0)", "(4,-2)", "(-4,2)", "(0,2)"], "correct": 0},
        {"q": "La operación g/cm³ → kg/m³ multiplica por:", "opts": ["1000", "0.001", "10", "1/1000"], "correct": 0},
        {"q": "¿Cuál prefijo es 10⁻⁹?", "opts": ["nano", "micro", "pico", "milli"], "correct": 0},
        {"q": "Si |A| = 5 y θ=53°, Ax ≈", "opts": ["3", "4", "5", "2.5"], "correct": 0},
        {"q": "La suma de vectores es conmutativa?", "opts": ["sí", "no", "solo en algunos casos", "depende"], "correct": 0},
        {"q": "Cifras significativas de 1228.0 son:", "opts": ["5", "4", "3", " ambiguo"], "correct": 0},
        {"q": "Un vector nulo (0,0) es:", "opts": ["vector cero", "no existe", "escalar", "unitario"], "correct": 0},
    ]

    if 'respuestas' not in st.session_state:
        st.session_state.respuestas = [None] * len(preguntas)

    for i, p in enumerate(preguntas):
        st.markdown(f"**{i+1}. {p['q']}**")
        opciones = p['opts']
        # Determinar índice por defecto
        default_idx = st.session_state.respuestas[i] if st.session_state.respuestas[i] is not None else 0
        respuesta = st.radio(
            "Selecciona una opción:",
            opciones,
            index=default_idx,
            key=f"q{i}",
            label_visibility="collapsed"
        )
        st.session_state.respuestas[i] = opciones.index(respuesta)

    if st.button("Revisar respuestas"):
        correctas = 0
        for i, p in enumerate(preguntas):
            if st.session_state.respuestas[i] == p['correct']:
                st.success(f"{i+1}. Correcto")
                correctas += 1
            else:
                st.error(f"{i+1}. Incorrecto. Respuesta correcta: {p['opts'][p['correct']]}")
        st.markdown(f"## 📊 {correctas}/15 correctas")

# Pie de página
st.markdown('<div class="footer">🧪 Física en movimiento — conversiones, vectores y precisión</div>', unsafe_allow_html=True)

