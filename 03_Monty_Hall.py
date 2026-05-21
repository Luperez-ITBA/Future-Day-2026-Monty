import streamlit as st
import random
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Monty Hall - ITBA", layout="wide", initial_sidebar_state="collapsed")

# --- MEMORIA DEL JUEGO Y ESTADÍSTICAS ---
if 'etapa' not in st.session_state:
    st.session_state.etapa = 'inicio'
    st.session_state.puertas = [0, 0, 0] # 1 es Tesoro, 0 es Rabanito
    st.session_state.eleccion_usuario = None
    st.session_state.puerta_abierta_monty = None
    st.session_state.stats_quedarse = {'intentos': 0, 'exitos': 0}
    st.session_state.stats_cambiar = {'intentos': 0, 'exitos': 0}
    st.session_state.lanzar_festejo = False

# --- ESTILOS CSS UNIFICADOS ---
st.markdown("""
    <style>
    /* Fondo principal */
    .main { background-color: #f8fafc; }
    
    /* Clase para agrandar el texto de la explicación y darle estilo de caja destacada */
    .texto-grande {
        font-size: 22px !important;
        line-height: 1.6;
        color: #1e293b;
        background-color: #e2e8f0;
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #0074D9;
        margin-bottom: 25px;
    }
    
    /* Botón de navegación al Hub */
    .btn-nav {
        display: block;
        width: 100%;
        padding: 12px 0;
        background-color: #001f3f;
        color: #ffffff !important;
        text-align: center;
        border-radius: 10px;
        text-decoration: none !important;
        font-weight: 600;
        font-size: 16px;
        transition: background-color 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-top: 30px;
    }
    .btn-nav:hover, .btn-nav:visited, .btn-nav:active {
        text-decoration: none !important;
        color: white !important;
    }
    .btn-nav:hover {
        background-color: #0074D9;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA Y CONTROLES (Reemplaza a la antigua sidebar) ---
col_logo, col_titulo, col_reinicio = st.columns([1, 3, 1])

with col_logo:
    try:
        st.image('logo_itba.png', width=150)
    except:
        st.write("### ITBA")

with col_titulo:
    st.title("🎁 El Dilema de Monty Hall")

with col_reinicio:
    st.write("") # Espaciador para alinear
    if st.button("🔄 Reiniciar Juego Actual", use_container_width=True):
        st.session_state.etapa = 'inicio'
        st.session_state.lanzar_festejo = False
        st.rerun()

st.write("---")

# --- SISTEMA DE PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🚪 El Juego", "📊 Estadísticas", "🧠 Matemática"])

with tab1:
    # Explicación con el CSS aplicado y la corrección de redacción
    st.markdown("""
    <div class="texto-grande">
        Imaginá que estás en un programa de televisión. Tienes que elegir una de las tres puertas. 
        Detrás de una de ellas hay un auto 0KM (el Tesoro), y detrás de las otras dos hay cabras (o rabanitos).<br><br>
        Una vez que eliges, el presentador (Monty), que sabe qué hay detrás de cada puerta, abre una de las otras dos 
        que tiene una cabra. Luego te pregunta: <b>¿Quieres quedarte con tu opción original o quieres cambiar a la puerta restante?</b>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.etapa == 'inicio':
        if st.button("▶️ Iniciar Nuevo Juego", type="primary"):
            st.session_state.puertas = [0, 0, 0]
            st.session_state.puertas[random.randint(0, 2)] = 1
            st.session_state.etapa = 'eleccion'
            st.rerun()
            
    elif st.session_state.etapa == 'eleccion':
        st.subheader("Elige una puerta:")
        col1, col2, col3 = st.columns(3)
        
        for i, col in enumerate([col1, col2, col3]):
            with col:
                if st.button(f"🚪 Puerta {i+1}", use_container_width=True):
                    st.session_state.eleccion_usuario = i
                    
                    # Monty abre una puerta
                    opciones_monty = [j for j in range(3) if j != i and st.session_state.puertas[j] == 0]
                    st.session_state.puerta_abierta_monty = random.choice(opciones_monty)
                    
                    st.session_state.etapa = 'cambio'
                    st.rerun()
                    
    elif st.session_state.etapa == 'cambio':
        st.subheader(f"Elegiste la Puerta {st.session_state.eleccion_usuario + 1}.")
        st.info(f"Monty abre la Puerta {st.session_state.puerta_abierta_monty + 1} y revela un rabanito 🥕.")
        st.warning("¿Qué decides hacer?")
        
        puerta_restante = [j for j in range(3) if j != st.session_state.eleccion_usuario and j != st.session_state.puerta_abierta_monty][0]
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"✊ Quedarme con la Puerta {st.session_state.eleccion_usuario + 1}", use_container_width=True):
                st.session_state.stats_quedarse['intentos'] += 1
                if st.session_state.puertas[st.session_state.eleccion_usuario] == 1:
                    st.session_state.stats_quedarse['exitos'] += 1
                    st.session_state.lanzar_festejo = True
                st.session_state.etapa = 'resultado'
                st.session_state.eleccion_final = st.session_state.eleccion_usuario
                st.rerun()
        with col2:
            if st.button(f"🔄 Cambiar a la Puerta {puerta_restante + 1}", type="primary", use_container_width=True):
                st.session_state.stats_cambiar['intentos'] += 1
                if st.session_state.puertas[puerta_restante] == 1:
                    st.session_state.stats_cambiar['exitos'] += 1
                    st.session_state.lanzar_festejo = True
                st.session_state.etapa = 'resultado'
                st.session_state.eleccion_final = puerta_restante
                st.rerun()
                
    elif st.session_state.etapa == 'resultado':
        if st.session_state.lanzar_festejo:
            st.balloons()
            st.success(f"¡GANASTE! 🎉 El tesoro estaba en la Puerta {st.session_state.eleccion_final + 1}.")
        else:
            puerta_ganadora = [i for i, x in enumerate(st.session_state.puertas) if x == 1][0] + 1
            st.error(f"Perdiste. 🥕 El tesoro estaba en la Puerta {puerta_ganadora}.")
            
        if st.button("▶️ Jugar de Nuevo", type="primary"):
            st.session_state.etapa = 'inicio'
            st.session_state.lanzar_festejo = False
            st.rerun()

with tab2:
    st.subheader("Tus Estadísticas Históricas")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Estrategia: Quedarse")
        intentos = st.session_state.stats_quedarse['intentos']
        exitos = st.session_state.stats_quedarse['exitos']
        st.metric("Partidas Jugadas", intentos)
        st.metric("Victorias", exitos)
        if intentos > 0:
            st.metric("Efectividad", f"{(exitos/intentos)*100:.1f}%")
        else:
            st.metric("Efectividad", "0.0%")
            
    with col2:
        st.markdown("### Estrategia: Cambiar")
        intentos_c = st.session_state.stats_cambiar['intentos']
        exitos_c = st.session_state.stats_cambiar['exitos']
        st.metric("Partidas Jugadas", intentos_c)
        st.metric("Victorias", exitos_c)
        if intentos_c > 0:
            st.metric("Efectividad", f"{(exitos_c/intentos_c)*100:.1f}%")
        else:
            st.metric("Efectividad", "0.0%")

with tab3:
    st.subheader("La Matemática detrás del Juego")
    
    st.markdown("""
    ### La Información de Monty
    Hay que notar que la **información** que nos da Monty al abrir una puerta no es solamente que hay un rabanito tras ella. 
    La información real es que **Monty abrió esa puerta específica y NO abrió la otra**. 

    Para fijar ideas, supongamos que elegimos la **Puerta 1** ($1_T$) y Monty abrió la **Puerta 2** ($2_A$):
    * Si el tesoro hubiera estado detrás de la Puerta 2, Monty **NUNCA** la hubiera abierto. 
    * Esa es la información que sesga la probabilidad en favor del cambio.
    
    ### El Cálculo Matemático
    Usando el **Teorema de Bayes** y la **Ley de Probabilidad Total**, podemos calcular la probabilidad de que el tesoro esté en nuestra puerta original ($1_T$) dado que Monty abrió la 2 ($2_A$):
    """)

    st.latex(r"P(1_T | 2_A) = \frac{P(2_A | 1_T) P(1_T)}{P(2_A)}")
    
    st.markdown("Donde el denominador (Probabilidad Total) se expande como:")
    st.latex(r"P(2_A) = P(2_A|1_T)P(1_T) + P(2_A|2_T)P(2_T) + P(2_A|3_T)P(3_T)")
    st.markdown("Al resolverlo matemáticamente, obtenemos que $P(1_T | 2_A) = 1/3$, mientras que la probabilidad de ganar cambiando de puerta asciende a **2/3**. ¡Por eso siempre conviene cambiar!")

# --- BOTÓN DE RETORNO AL HUB ---
st.write("---")
col_vacia1, col_boton_regreso, col_vacia2 = st.columns([1, 1, 1])
with col_boton_regreso:
    st.markdown('<a href="https://future-day-2026-hub.streamlit.app/" target="_blank" class="btn-nav">🔙 Volver al Hub Principal</a>', unsafe_allow_html=True)
