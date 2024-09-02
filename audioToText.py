import os
from pydub import AudioSegment
import speech_recognition as sr
from docx import Document

def split_audio(audio_path, chunk_length_ms):
    audio = AudioSegment.from_file(audio_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

def convert_audio_chunk_to_text(audio_chunk):
    recognizer = sr.Recognizer()
    wav_path = "temp_chunk.wav"
    audio_chunk.export(wav_path, format="wav")
    
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data, language="es-ES")
        return text
    except sr.UnknownValueError:
        return "No se pudo entender el audio"
    except sr.RequestError as e:
        return f"Error al solicitar resultados del servicio de reconocimiento de voz; {e}"
    finally:
        os.remove(wav_path)

def save_text_to_word(text, word_path):
    os.makedirs(os.path.dirname(word_path), exist_ok=True)
    
    doc = Document()
    doc.add_paragraph(text)
    doc.save(word_path)

def main(audio_path, word_path, chunk_length_ms=60000):
    chunks = split_audio(audio_path, chunk_length_ms)
    full_text = ""
    
    for i, chunk in enumerate(chunks):
        print(f"Procesando fragmento {i+1}/{len(chunks)}")
        text = convert_audio_chunk_to_text(chunk)
        full_text += text + "\n"
    
    save_text_to_word(full_text, word_path)
    print(f"Transcripción guardada en {word_path}")

if __name__ == "__main__":
    audio_path = "audio/linda.mp3"
    word_path = "doc/salida.docx"
    main(audio_path, word_path)
