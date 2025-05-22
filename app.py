import streamlit as st
import random
from datetime import date


st.set_page_config(page_title="mySongList", page_icon=":)", layout="wide")

st.title("mySongList")
st.subheader("🎶 Elige la lista de canciones")

# Verificamos si la clave "canciones" no existe todavía en el estado de la sesión
# Esto asegura que la lista se cree solo una vez, no cada vez que se actualiza la página
if "canciones" not in st.session_state:
    st.session_state.canciones = []  # Creamos la lista vacía de canciones

# Entrada de usuario
cancion = st.text_input("Escribe el nombre de la canción")
# Cuando el usuario haga clic en el botón, se ejecuta este bloque
#Si el usuario hace clic en el botón "Guardar canción", se ejecuta este bloque
if st.button("Guardar canción"):
    # Eliminamos los espacios en blanco al principio y al final del texto ingresado
    # Esto evita que se guarden canciones vacías o con espacios accidentales
    cancion = cancion.strip()
    #Verificamos si el texto está vacío después de aplicar strip()
    # Esto ocurre si el usuario no escribió nada o solo puso espacios
    if cancion == "":
        # Mostramos un mensaje de advertencia al usuario
        st.warning("Por favor escribe un nombre antes de guardar.")
    else:
        # Vamos a verificar si la canción ya existe en la lista
        # Creamos una variable llamada 'ya_existe' para llevar el control
        ya_existe = False
        # Recorremos todas las canciones que ya están guardadas
        for c in st.session_state.canciones:
            # Comparamos la nueva canción con cada una, ignorando mayúsculas/minúsculas
            if cancion.lower() == c.lower():
                ya_existe = True  # Si encontramos una coincidencia, cambiamos la bandera
                break  # Ya no necesitamos seguir buscando, salimos del bucle
        # Si la canción ya existía, mostramos una advertencia
        if ya_existe:
            st.warning("Esta canción ya está en la lista.")
        else:
            # Si la canción no estaba, la agregamos a la lista
            st.session_state.canciones.append(cancion)
            # Mostramos un mensaje de éxito al usuario
            st.toast("🎶 Canción guardada con éxito!")


# Mostrar listado con opción de eliminar
st.subheader("🎼 Listado de canciones:")
for i, c in enumerate(st.session_state.canciones):
    col1, col2 = st.columns([6, 25])
    with col1:
        st.write(f"{i+1}. {c}")
    with col2:
        if st.button("🗑️", key=f"delete_{i}"):
            st.session_state.canciones.pop(i)
            st.rerun()

# -------------------------
# SECCIÓN DE SELECCIÓN DE CANCIONES
# -------------------------
st.subheader("🎲 Selección de canciones para hoy")

modo = st.radio("¿Cómo quieres seleccionar las canciones?", ["Manual", "Aleatoria"])

if st.session_state.canciones:
    if modo == "Manual":
        seleccion_manual = st.multiselect("Selecciona las canciones que quieres tocar:", st.session_state.canciones)
        if seleccion_manual:
            st.success("Lista de canciones seleccionadas manualmente:")
            st.write(seleccion_manual)
    else:  # Aleatoria
        cantidad = st.slider("¿Cuántas canciones quieres elegir al azar?", 1, len(st.session_state.canciones))
        if st.button("Generar lista aleatoria"):
            seleccion_aleatoria = random.sample(st.session_state.canciones, cantidad)
            st.success("Lista de canciones aleatorias:")
            st.write(seleccion_aleatoria)
else:
    st.info("Primero debes agregar canciones para poder seleccionarlas.")


# creando el historial
if "historial" not in st.session_state:
    st.session_state.historial = []

if st.button("Guardar historial"):
    if st.session_state.canciones:
        canciones_seleccionadas = seleccion_manual if seleccion_manual else seleccion_aleatoria
        if canciones_seleccionadas:
            st.session_state.historial.append({
                "fecha": date.today().isoformat(),
                "canciones": canciones_seleccionadas
            })
            st.success("Historial guardado correctamente.")


st.subheader("📜 Historial de canciones tocadas")

if st.session_state.historial:
    for registro in reversed(st.session_state.historial):
        st.markdown(f"### 📅 {registro['fecha']}")
        for cancion in registro["canciones"]:
            st.markdown(f"- 🎵 {cancion}")
else:
    st.info("Todavía no has guardado ninguna lista en el historial.")

import urllib.parse

if st.button("📤 Compartir por WhatsApp"):
    if st.session_state.historial:
        # Último registro del historial
        ultima = st.session_state.historial[-1]
        fecha = ultima["fecha"]
        canciones = ultima["canciones"]

        mensaje = f"📅 {fecha}\n"
        mensaje += "\n".join([f"🎵 {c}" for c in canciones])

        mensaje_codificado = urllib.parse.quote(mensaje)
        enlace_whatsapp = f"https://wa.me/?text={mensaje_codificado}"

        st.markdown(f"[Haz clic aquí para compartir por WhatsApp]({enlace_whatsapp})", unsafe_allow_html=True)
    else:
        st.warning("Primero guarda una lista en el historial.")
