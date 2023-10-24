import pandas as pd
import re
import streamlit as st
from streamlit_lottie import st_lottie
from Entities.Chat import Chat

chat = Chat()

# Crear una aplicación Streamlit
st.title("Analizador de Chat de WhatsApp")

# Subir un archivo
uploaded_file = st.file_uploader("Carga un archivo de chat de WhatsApp (.txt)", type=["txt"])
chat_df = None

if uploaded_file is not None:
    # Procesar el archivo
    chat_df = chat.process_data(uploaded_file)

    # Mostrar una vista previa de los datos
    st.subheader("Vista previa")
    
    # Agregar un slider para seleccionar la fecha de inicio y fin en el sidebar
    st.sidebar.subheader("Filtrar por Fecha")
    # Obtén los valores mínimo y máximo de la columna 'date' de tu DataFrame
    min_date = chat_df['date'].min()
    max_date = chat_df['date'].max()

    # Crea un sidebar para seleccionar la fecha de inicio
    start_date = st.sidebar.date_input("Fecha de Inicio", min_value=min_date, max_value=max_date, value=min_date)

    # Crea un sidebar para seleccionar la fecha de fin
    end_date = st.sidebar.date_input("Fecha de Fin", min_value=min_date, max_value=max_date, value=max_date)

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
        
    custom_excluded_words = [ "multimedia", "omitido","Jajaja", "Jajajaja","Jajajajaja","jajajja",
                             "jaja","jajaj","Jajajjaa","Jajajajjaa", "jajajaj","jajajajaj","Jajajjaja",
                             "si","así", "https", "com", "v", "vm", "c"
                            ]
    selected_words = st.sidebar.multiselect("Palabras personalizadas a excluir", custom_excluded_words, default=custom_excluded_words)
    word_df = chat.count_words_frequency(selected_words)
    st.write(word_df)

    # Agregar aquí tus análisis y visualizaciones

    




   