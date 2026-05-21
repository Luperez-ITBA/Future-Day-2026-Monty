import streamlit as st
import random
from PIL import Image
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

# --- CABECERA Y CONTROLES ---
col_logo, col_titulo, col_reinicio = st.columns([1, 3, 2])

with col_logo:
    try:
        st.image('logo_itba.png', use_container_width=True)
    except:
        st.write("ITBA - Future Day")

with col_titulo:
    st.title("🚪 El Dilema de Monty Hall")

with col_reinicio:
    st.write("") # Espaciador para alinear con el título
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("🔄 Reiniciar Juego", use_container_width=True):
            st.session_state.etapa = 'inicio'
            st.session_state.lanzar_festejo = False
            st.rerun()
    with c_btn2:
        if st.button("🗑️ Borrar Stats", use_container_width=True):
            st.session_state.stats_quedarse = {'intentos': 0, 'exitos': 0}
            st.session_state.stats_cambiar = {'intentos': 0, 'exitos': 0}
            st.rerun()

st.write("---")

# Explicación con el texto original conservado, fuente aumentada y palabra cambiada
st.markdown("""
<div style="font-size: 22px; line-height: 1.6; background-color: #e2e8f0; padding: 25px; border-radius: 12px; border-left: 8px solid #0074D9; margin-bottom: 25px;">

* Detrás de una de las puertas se esconde un **tesoro**, detrás de las otras dos un **triste rabanito**.
* Te dejan elegir una de las tres puertas.
* Luego de tu elección, te muestran detrás de una de las otras dos, donde había un rabanito.
* Te dan a elegir: **quedarte con tu opción original o cambiar de puerta**.
* ¿Qué conviene? ¿Quedarnos con nuestra opción original? ¿Cambiar? ¿Da lo mismo?

</div>
""", unsafe_allow_html=True)
st.write("---")

tab1, tab2, tab3 = st.tabs(["🎮 ¡A Jugar!", "📊 Simulación y Estrategias", "🧠 Explicación Teórica"])

with tab1:
    if st.session_state.etapa == 'inicio':
        puertas = [0, 0, 0]
        puertas[random.randint(0, 2)] = 1 
        st.session_state.puertas = puertas
        st.session_state.lanzar_festejo = False
        st.subheader("Elegí una puerta. ¡Buscá el tesoro!")
    
    spacer_l, c1, c2, c3, spacer_r = st.columns([1, 2, 2, 2, 1])
    cols = [c1, c2, c3]

    for i in range(3):
        with cols[i]:
            st.write(f"### Puerta {i+1}")
            if st.session_state.etapa == 'inicio':
                st.image('puerta_cerrada.jpg', use_container_width=True)
                if st.button(f"Elegir Puerta {i+1}", key=f"btn_{i}"):
                    st.session_state.eleccion_usuario = i
                    opciones_monty = [j for j in range(3) if j != i and st.session_state.puertas[j] == 0]
                    st.session_state.puerta_abierta_monty = random.choice(opciones_monty)
                    st.session_state.etapa = 'decision'
                    st.rerun()
            elif st.session_state.etapa == 'decision':
                if i == st.session_state.puerta_abierta_monty:
                    st.image('premio_cabra.png', use_container_width=True)
                    st.caption("¡Acá había un rabanito!")
                elif i == st.session_state.eleccion_usuario:
                    st.image('puerta_cerrada.jpg', use_container_width=True)
                    st.info("Tu elección")
                else:
                    st.image('puerta_cerrada.jpg', use_container_width=True)
            elif st.session_state.etapa == 'resultado':
                if st.session_state.puertas[i] == 1:
                    st.image('premio_auto.png', use_container_width=True)
                else:
                    st.image('premio_cabra.png', use_container_width=True)

    if st.session_state.etapa == 'decision':
        st.write("---")
        st.subheader(f"Elegiste la Puerta {st.session_state.eleccion_usuario + 1}. Monty abrió la Puerta {st.session_state.puerta_abierta_monty + 1}.")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("Me quedo con la mía"):
                if st.session_state.puertas[st.session_state.eleccion_usuario] == 1:
                    st.session_state.lanzar_festejo = True
                st.session_state.etapa = 'resultado'
                st.rerun()
        with col_b2:
            if st.button("¡Sí, quiero cambiar!"):
                nueva = [j for j in range(3) if j != st.session_state.eleccion_usuario and j != st.session_state.puerta_abierta_monty][0]
                st.session_state.eleccion_usuario = nueva
                if st.session_state.puertas[st.session_state.eleccion_usuario] == 1:
                    st.session_state.lanzar_festejo = True
                st.session_state.etapa = 'resultado'
                st.rerun()

    if st.session_state.etapa == 'resultado':
        if st.session_state.lanzar_festejo:
            st.balloons()
            st.session_state.lanzar_festejo = False
        st.write("---")
        if st.session_state.puertas[st.session_state.eleccion_usuario] == 1:
            st.success("🎉 ¡Felicidades! Encontraste el Tesoro.")
        else:
            st.error("😢 ¡Mala suerte! Es solo un triste rabanito.")
        st.button("Jugar otra vez", on_click=lambda: st.session_state.update(etapa='inicio'))

with tab2:
    st.subheader("Simulación de Estrategias")
    st.write("Simulá juegos para ver cuál estrategia gana más veces en el largo plazo.")
    
    if st.button("🏃 Simular 10 juegos"):
        for _ in range(10):
            p_q, e_q = random.randint(0, 2), random.randint(0, 2)
            st.session_state.stats_quedarse['intentos'] += 1
            if p_q == e_q: st.session_state.stats_quedarse['exitos'] += 1
            
            p_c, e_c = random.randint(0, 2), random.randint(0, 2)
            st.session_state.stats_cambiar['intentos'] += 1
            if p_c != e_c: st.session_state.stats_cambiar['exitos'] += 1

    total_q = st.session_state.stats_quedarse['intentos']
    total_c = st.session_state.stats_cambiar['intentos']
    prop_q = st.session_state.stats_quedarse['exitos'] / total_q if total_q > 0 else 0
    prop_c = st.session_state.stats_cambiar['exitos'] / total_c if total_c > 0 else 0

    col_graf, _ = st.columns([0.6, 0.4])
    with col_graf:
        fig, ax = plt.subplots(figsize=(5, 3)) 
        ax.bar(['Quedarse', 'Cambiar'], [prop_q, prop_c], color=['#e74c3c', '#2ecc71'])
        ax.set_ylim(0, 1)
        ax.axhline(0.33, color='black', linestyle='--', alpha=0.3)
        ax.axhline(0.66, color='black', linestyle='--', alpha=0.3)
        ax.set_ylabel("Proporción de Éxito")
        st.pyplot(fig)
    
    st.info("""
    💡 **Análisis de la simulación:**
    * Una vez que abrieron la tercera puerta, sabemos que en una de las puertas cerradas está el tesoro y en la otra el rabanito.
    * Tenemos una probabilidad de ganar de 50% con cualquier elección...
    * Sin embargo, el gráfico nos muestra claramente por la experiencia que **conviene cambiar la elección**.
    * Esto se debe a que cambiar **duplica las probabilidades de ganar**. 
    * **¿Por qué pasa esto?** Podés encontrar la respuesta en la siguiente pestaña.
    """)

with tab3:
    st.subheader("🎓 El Veredicto de la Probabilidad Condicional")
    
    st.markdown("""
    El concepto clave para entender este resultado es la **Probabilidad Condicional**, que se define como:
    """)
    st.latex(r"P(A|B) = \frac{P(A \cap B)}{P(B)}")
    
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
    
    st.markdown("Sustituyendo los valores de nuestro caso:")
    st.latex(r"P(1_T | 2_A) = \frac{\frac{1}{2} \cdot \frac{1}{3}}{\frac{1}{2}\cdot\frac{1}{3} + 0\cdot\frac{1}{3} + 1\cdot\frac{1}{3}} = \frac{1/6}{3/6} = \frac{1}{3}")
    
    st.success("Esto demuestra que nuestra puerta inicial sigue teniendo **1/3** de probabilidad, por lo que la puerta restante necesariamente tiene **2/3**. ¡Siempre conviene cambiar!")
