# -*- coding: utf-8 -*-
import speech_recognition as sr
import datetime
import webbrowser
import time
import unicodedata
import win32com.client as wincl
import os

# =========================
# CONFIGURACIÓN
# =========================
WAKE_WORDS = ["jarvis","oye jarvis", "jarbis", "harvis", "yarvis", "charvis","jarvi"]

IDIOMA = "es-ES"

# =========================
# VOZ (SAPI - Windows)
# =========================
voz = wincl.Dispatch("SAPI.SpVoice")
voz.Volume = 100   # 0-100
voz.Rate = 0       # -10 a 10

def hablar(texto: str):
    print("Jarvis:", texto)
    voz.Speak(texto)

# =========================
# RECONOCIMIENTO DE VOZ
# =========================
r = sr.Recognizer()
r.dynamic_energy_threshold = True
r.pause_threshold = 0.6
r.non_speaking_duration = 0.3

def normalizar(texto: str) -> str:
    texto = texto.lower()
    texto = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    return texto

def escuchar() -> str:
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
        hablar("Problema de conexion.")
        return ""

# =========================
# COMANDOS
# =========================
def procesar_comando(cmd: str) -> bool:
    if "hora" in cmd:
        hablar("Son las " + datetime.datetime.now().strftime("%H:%M"))
        return True

    if "abre" in cmd and ("google" in cmd or "gugel" in cmd):
        hablar("Abriendo Google")
        os.startfile("https://www.google.com")
        return True

    cmd = cmd.replace("you tube", "youtube")  
    if "abre" in cmd and ("youtube" in cmd or "yutu" in cmd):
        hablar("Abriendo YouTube")
        os.startfile("https://www.youtube.com")
        return True


    if "como estas" in cmd:
        hablar("Funcionando correctamente.")
        return True
    if "muestrame tu codigo" in cmd or "ver tu codigo" in cmd:
        hablar("Te muestro mi codigo fuente en GitHub.")
        webbrowser.open("https://github.com/Itskenfer360/Jarvis/blob/main/jarvis2.0.py")
        return True
    if "apaga" in cmd or "salir" in cmd:
        hablar("Hasta luego.")
        return False

    hablar("No entiendo el comando.")
    return True

# =========================
# PRINCIPAL
# =========================
def main():
    hablar("Sistema iniciado. Di Jarvis para activarme.")

    # Calibrar una sola vez
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)

    while True:
        # ===== ESTADO 1: REPOSO =====
        texto = escuchar()
        if not any(w in texto for w in WAKE_WORDS):
            continue

        # ===== ESTADO 2: ESPERAR COMANDO =====
        hablar("Te escucho")
        comando = escuchar()

        if not comando:
            hablar("No te he entendido.")
            time.sleep(0.5)
            continue

        # ===== ESTADO 3: EJECUTAR =====
        seguir = procesar_comando(comando)

        if not seguir:
            break  # salir del programa

        # ===== ESTADO 4: RESET SUAVE =====
        time.sleep(1.0)  # 🔑 
if __name__ == "__main__":
    main()
