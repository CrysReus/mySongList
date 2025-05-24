import streamlit as st
import random
from datetime import date
import urllib.parse

st.set_page_config(page_title="mySongList", page_icon=":)", layout="wide")

st.title("mySongList")
st.subheader("\U0001F3B6 Elige la lista de canciones")

# --- Cargar canciones desde archivo externo ---
def cargar_canciones():
    try:
        with open("canciones.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

# --- Guardar canción en archivo externo ---
def guardar_cancion_en_archivo(cancion):
    with open("canciones.txt", "a", encoding="utf-8") as f:
        f.write(cancion + "\n")

# --- Inicializar estados ---
if "canciones" not in st.session_state:
    st.session_state.canciones = cargar_canciones()

if "historial" not in st.session_state:
    st.session_state.historial = []

# Entrada de usuario
cancion = st.text_input("Escribe el nombre de la canción")
if st.button("Guardar canción"):
    cancion = cancion.strip()
    if cancion == "":
        st.warning("Por favor escribe un nombre antes de guardar.")
    else:
        ya_existe = any(cancion.lower() == c.lower() for c in st.session_state.canciones)
        if ya_existe:
            st.warning("Esta canción ya está en la lista.")
        else:
            st.session_state.canciones.append(cancion)
            guardar_cancion_en_archivo(cancion)
            st.toast("\U0001F3B6 Canción guardada con éxito!")

# Mostrar listado dentro de un expander para evitar scroll largo
with st.expander("\U0001F3BC Listado de canciones (haz clic para ver/desplegar)"):
    for i, c in enumerate(st.session_state.canciones):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.write(f"{i+1}. {c}")
        with col2:
            if st.button("🗑️", key=f"delete_{i}"):
                st.session_state.canciones.pop(i)
                # Actualizar archivo externo
                with open("canciones.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join(st.session_state.canciones))
                st.rerun()

# SECCIÓN DE SELECCIÓN DE CANCIONES
st.subheader("\U0001F3B2 Selección de canciones para hoy")
modo = st.radio("¿Cómo quieres seleccionar las canciones?", ["Manual", "Aleatoria"])

seleccion_manual = []
seleccion_aleatoria = []

if st.session_state.canciones:
    if modo == "Manual":
        seleccion_manual = st.multiselect("Selecciona las canciones que quieres tocar:", st.session_state.canciones)
        if seleccion_manual:
            st.success("Lista de canciones seleccionadas manualmente:")
            st.write(seleccion_manual)
    else:
        cantidad = st.slider("¿Cuántas canciones quieres elegir al azar?", 1, len(st.session_state.canciones))
        if st.button("Generar lista aleatoria"):
            seleccion_aleatoria = random.sample(st.session_state.canciones, cantidad)
            st.success("Lista de canciones aleatorias:")
            st.write(seleccion_aleatoria)
else:
    st.info("Primero debes agregar canciones para poder seleccionarlas.")

# Guardar historial
if st.button("Guardar historial"):
    if st.session_state.canciones:
        canciones_seleccionadas = seleccion_manual if seleccion_manual else seleccion_aleatoria
        if canciones_seleccionadas:
            st.session_state.historial.append({
                "fecha": date.today().isoformat(),
                "canciones": canciones_seleccionadas
            })
            st.success("Historial guardado correctamente.")

# Mostrar historial
st.subheader("\U0001F4DC Historial de canciones tocadas")
if st.session_state.historial:
    for registro in reversed(st.session_state.historial):
        st.markdown(f"### \U0001F4C5 {registro['fecha']}")
        for cancion in registro["canciones"]:
            st.markdown(f"- \U0001F3B5 {cancion}")
else:
    st.info("Todavía no has guardado ninguna lista en el historial.")

# Compartir por WhatsApp
if st.button("\U0001F4E4 Compartir por WhatsApp"):
    if st.session_state.historial:
        ultima = st.session_state.historial[-1]
        fecha = ultima["fecha"]
        canciones = ultima["canciones"]

        mensaje = f"\U0001F4C5 {fecha}\n" + "\n".join([f"\U0001F3B5 {c}" for c in canciones])
        mensaje_codificado = urllib.parse.quote(mensaje)
        enlace_whatsapp = f"https://wa.me/?text={mensaje_codificado}"

        st.markdown(f"[Haz clic aquí para compartir por WhatsApp]({enlace_whatsapp})", unsafe_allow_html=True)
    else:
        st.warning("Primero guarda una lista en el historial.")

st.subheader("CARGAR CANCIONES CON LETRAS Y ACORDES")
st.subheader("Aqui estrán todas las canciones con letras y acordes... ")
st.text("Se esta trabajando en ello, agradecemos tu paciencia.....")