

import openai
import speech_recognition as sr
from gtts import gTTS
import pygame
import os


# Configura tu clave de API de OpenAI
# openai.api_key = os.environ.get.OPENAI_API_KEY,

# Función para enviar la pregunta a GPT-4 y obtener una respuesta
def obtener_respuesta(pregunta):
    # Enviamos la pregunta al modelo GPT-4 (gpt-4o en este caso)
    response = openai.Completion.create(
      engine="gpt-3.5-turbo-0125",
      prompt=pregunta,
      max_tokens=150  # Limitamos el número de tokens para la respuesta
    )
    # Extraemos la respuesta del modelo y la limpiamos de espacios en blanco
    respuesta = response.choices[0].text.strip()
    return respuesta

# Función para capturar la voz del usuario usando el micrófono
def capturar_voz():
    recognizer = sr.Recognizer()  # Creamos una instancia del reconocedor de voz
    with sr.Microphone() as source:
        print("Escuchando...")
        # Capturamos el audio desde el micrófono
        audio = recognizer.listen(source)

    try:
        # Intentamos convertir el audio capturado a texto usando Google Speech Recognition
        texto = recognizer.recognize_google(audio, language="es-ES")
        print(f"Has dicho: {texto}")
        return texto
    except sr.UnknownValueError:
        # Si no se puede entender el audio
        print("No se pudo entender el audio")
        return ""
    except sr.RequestError:
        # Si ocurre un error en la comunicación con el servicio de reconocimiento de voz
        print("Error al comunicarse con el servicio de reconocimiento de voz")
        return ""

# Función para reproducir la respuesta del avatar usando gTTS para convertir texto a voz
def reproducir_respuesta(respuesta):
    tts = gTTS(text=respuesta, lang='es')  # Convertimos el texto a voz en español
    archivo = "respuesta.mp3"  # Guardamos el archivo de audio como 'respuesta.mp3'
    tts.save(archivo)  # Guardamos el archivo en el sistema
    os.system(f"mpg321 {archivo}")  # Ejecutamos el archivo de audio (Linux/macOS)
    # En Windows, podrías usar:
    # os.system(f"start {archivo}")

# Función principal que integra la captura de voz, el procesamiento con GPT-4 y la respuesta hablada
def main():
    while True:
        pregunta = capturar_voz()  # Capturamos lo que el usuario dice
        if pregunta:
            respuesta = obtener_respuesta(pregunta)  # Obtenemos la respuesta de GPT-4
            print(f"ChatGPT dice: {respuesta}")  # Mostramos la respuesta en la consola
            reproducir_respuesta(respuesta)  # Reproducimos la respuesta como audio

# Punto de entrada de la aplicación
if __name__ == "__main__":
    main()  # Ejecutamos la función principal para iniciar el programa
