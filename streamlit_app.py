import pandas as pd
import re
import streamlit as st
from streamlit_lottie import st_lottie
from Entities.Chat import Chat

# Cargar el archivo de configuración personalizado
st.set_page_config(
    page_title="MiChat",
    page_icon=":rocket:",
    layout="centered",
)

def process():
    chat = Chat()

    # Crear una aplicación Streamlit
    st.title("MiChat Analyser")

    # URL de la imagen
    imagen_url = "assets//img//michi.jpg"

    # Muestra la imagen en la barra lateral izquierda
    st.sidebar.image(imagen_url, width=200)

    # Subir un archivo
    uploaded_file = st.file_uploader("Upload a WhatsApp chat file (.txt)", type=["txt"])
    chat_df = None

    if uploaded_file is not None:
        # Procesar el archivo
        chat_df = chat.process_data(uploaded_file)
        chat_df = chat.analyze_sentiments()  # Análisis de sentimientos

        # Mostrar una vista previa de los datos
        st.subheader("Previes")
        
        # Agregar un slider para seleccionar la fecha de inicio y fin en el sidebar
        st.sidebar.subheader("Filter by date")
        # Obtén los valores mínimo y máximo de la columna 'date' de tu DataFrame
        min_date = chat_df['date'].min()
        max_date = chat_df['date'].max()

        # Crea un sidebar para seleccionar la fecha de inicio
        start_date = st.sidebar.date_input("Start", min_value=min_date, max_value=max_date, value=min_date)

        # Crea un sidebar para seleccionar la fecha de fin
        end_date = st.sidebar.date_input("End", min_value=min_date, max_value=max_date, value=max_date)

        # Convertir start_date y end_date a objetos datetime
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filtrar los mensajes por fecha
        filtered_df = chat_df[(chat_df['date'] >= start_date) & (chat_df['date'] <= end_date)]

        # Mostrar los mensajes filtrados si las fechas se han actualizado
        if start_date != min_date or end_date != max_date:
            st.write(filtered_df)
        
        # Mostrar la vista previa original si las fechas no se han actualizado
        else:
            st.write(chat_df)

        st.subheader("Most used words")
    
        custom_excluded_words = [ "multimedia", "omitido","jajaja", "jajajaja","jajajajaja","jajajja",
                                "jaja","jajaj","jajajjaa","jajajajjaa", "jajajaj","jajajajaj","jajajjaja",
                                "si","así", "https", "com", "v", "vm", "c"
                                ]
        selected_words = st.sidebar.multiselect("Palabras personalizadas a excluir", custom_excluded_words, default=custom_excluded_words)
        word_df = chat.count_words_frequency(selected_words)
        st.write(word_df)

        # Agregar aquí tus análisis y visualizaciones
        # Después de cargar y procesar tus datos, puedes contar emojis

        emoji_counts = chat.count_emojis(chat_df['message'])
        st.subheader("Most used emojis:")
        for emoji_char, count in emoji_counts.items():
            st.write(f"{emoji_char}: {count} veces")


if __name__ == "__main__":
    process()



   