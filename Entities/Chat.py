import pandas as pd
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords

class Chat:
    def __init__(self):
        self.df_chat =pd.DataFrame()

    def count_messages(self, messages):
        return len(messages)

    def count_multimedia(self, messages):
        # Expresion regular para multimedia
        multimedia_pattern = r'<[^>]+>'
        return len(re.findall(multimedia_pattern, messages))
        
    def count_links(self, messages):
        # Expresion regular para links
        link_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return len(re.findall(link_pattern, messages))
        
    # Leer el contenido del archivo
    def process_data(self, uploaded_file):
        messages = uploaded_file.read().decode("utf-8")

        # Expresión regular para extraer la fecha, hora, autor y mensaje
        pattern = r"(\d{1,2}/\d{1,2}/\d{4}, \d{1,2}:\d{2}) - ([^:]+): (.*)"
        
        # Dividir los mensajes en líneas
        message_lines = messages.split("\n")

        # Crear listas para almacenar los datos
        date_list = []
        time_list = []
        name_list = []
        message_list = []

        for line in message_lines:
            match = re.match(pattern, line)
            if match:
                datetime_str, author, content = match.groups()
                date, time = datetime_str.split(", ")
                date_list.append(pd.to_datetime(date, format='%d/%m/%Y', errors='coerce'))
                time_list.append(pd.to_datetime(time, format='%H:%M', errors='coerce').time())
                name_list.append(author)
                message_list.append(content)

        # Crear un DataFrame
        data = {
            "date": date_list,
            "time": time_list,
            "name": name_list,
            "message": message_list
        }
        self.df_chat = pd.DataFrame(data)
        
        return self.df_chat

    def set_df_chat(self, df):
        self.df_chat = df

    def count_words_frequency(self, omited_words):
        # Obtén el texto de todos los mensajes
        all_messages = " ".join(self.df_chat["message"])

        # Elimina signos de puntuación y convierte todo a minúsculas
        all_messages = re.sub(r'[^\w\s]', '', all_messages).lower()

        # Separa el texto en palabras
        words = self.delete_stopwords(all_messages.split(), omited_words)

        # Cuenta la frecuencia de cada palabra
        word_counts = Counter(words)

        # Convierte el conteo de palabras en un DataFrame
        word_df = pd.DataFrame(word_counts.items(), columns=["Palabra", "Frecuencia"])

        # Ordena el DataFrame por frecuencia en orden descendente
        word_df = word_df.sort_values(by="Frecuencia", ascending=False)

        return word_df

    def delete_stopwords(self, palabras, omited_words):
        # Define la ubicación de tu carpeta de recursos
        nltk_data_path = "..//Utils//stopwords"

        # Configura la ruta de datos de NLTK
        nltk.data.path.append(nltk_data_path)

        # Descarga las stopwords (esto se hará solo si no están ya descargadas en tu carpeta)
        nltk.download("stopwords", download_dir=nltk_data_path)

        # Obtén la lista de stopwords en español
        stopwords_es = set(stopwords.words("spanish"))

        palabras_filtradas = [palabra for palabra in palabras if palabra not in stopwords_es and palabra not in omited_words]
        return palabras_filtradas
        
