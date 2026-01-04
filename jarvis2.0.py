# -*- coding: utf-8 -*-
"""
Created on Sat Jan  3 18:13:01 2026

@author: kenne
"""

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import time
import unicodedata

# =========================
# CONFIGURACIÓN
# =========================
WAKE_WORD = "jarvis"
IDIOMA = "es-ES"

# =========================
# TEXTO A VOZ
# =========================
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def hablar(texto):
    print("Jarvis:", texto)
    engine.say(texto)
    engine.runAndWait()

# =========================
# RECONOCIMIENTO DE VOZ
# =========================
r = sr.Recognizer()
r.dynamic_energy_threshold = True
r.pause_threshold = 0.6
r.non_speaking_duration = 0.3

def normalizar(texto):
    texto = texto.lower()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto

def escuchar():
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=6, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            return ""

    try:
        texto = r.recognize_google(audio, language=IDIOMA)
        texto = normalizar(texto)
        print("Tú:", texto)
        return texto
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        hablar("Problema de conexión.")
        return ""

# =========================
# COMANDOS
# =========================
def procesar_comando(cmd):
    if "hora" in cmd:
        hablar("Son las " + datetime.datetime.now().strftime("%H:%M"))
        return True

    if "abre" in cmd and "google" in cmd:
        hablar("Abriendo Google")
        webbrowser.open("https://www.google.com")
        return True

    if "abre" in cmd and "youtube" in cmd:
        hablar("Abriendo YouTube")
        webbrowser.open("https://www.youtube.com")
        return True

    if "como estas" in cmd:
        hablar("Funcionando correctamente.")
        return True

    if "apaga" in cmd or "salir" in cmd:
        hablar("Hasta luego.")
        return False

    hablar("No entiendo el comando.")
    return True

# =========================
# PROGRAMA PRINCIPAL
# =========================
def main():
    hablar("Sistema iniciado. Di Jarvis para activarme.")

    # Calibración UNA sola vez
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)

    activo = True
    while activo:
        texto = escuchar()

        if not texto.startswith(WAKE_WORD):
            continue

        hablar("Te escucho")
        comando = escuchar()

        if not comando:
            hablar("No te he entendido.")
            continue

        activo = procesar_comando(comando)
        time.sleep(0.3)

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    main()
