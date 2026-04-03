import os
import re
import json

# Konfiguration
INPUT_FOLDERS = ["Lanz", "Illner", "Miosga", "Maischberger", "HartAberFair"]
OUTPUT_FILE = "talkshow_data_for_bert2.jsonl"
WORDS_PER_CHUNK = 250 

# Sender-Zuordnung
SENDER = {
    "Lanz": "ZDF",
    "Illner": "ZDF",
    "Miosga": "ARD",
    "Maischberger": "ARD",
    "HartAberFair": "ARD",
}

# Diese Endungen werden am Ende des Dateinamens entfernt
ENDINGS_TO_REMOVE = [".deu.srt", ".srt", ".txt"]

# Phrasen die aus dem Text entfernt werden sollen
PHRASES_TO_REMOVE = [
    r"Wir begr[üu]ßen Sie zur Live-Untertitelung",
    r"Untertitel:\s*WDR mediagroup GmbH\s*im Auftrag des WDR",
    r"Diese Untertitel sind live produziert\.?",
    r"Diese Sendung wurde vom NDR live untertitelt\s*\(\d{2}\.\d{2}\.\d{4}\)",
    r"Diese Themen und G[äa]ste erwarten Sie heute\.?",
    r"Wir sind live\.?",
    r"Sie sind zu Gast bei [^.]+\.",
    r"Die begr[üu]ßt alle G[äa]ste dieser Sendung herzlich\.?",
    r"Willkommen zu [^.]+\.",
]

def clean_srt(content):
    # SRT-Struktur entfernen
    text = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', content)
    # Newlines normalisieren
    text = re.sub(r'\n', ' ', text)
    # Unerwünschte Phrasen entfernen
    for phrase in PHRASES_TO_REMOVE:
        text = re.sub(phrase, '', text, flags=re.IGNORECASE)
    # Sprecherkürzel entfernen (nur 2 Großbuchstaben, sicher für SPD/CDU etc.)
    text = re.sub(r'\b[A-Z]{2}:\s*', '', text)
    # Pausenmarker entfernen
    text = re.sub(r'\s-\s', ' ', text)
    # Doppelte Wörter entfernen
    text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text, flags=re.IGNORECASE)
    # Überschüssige Leerzeichen entfernen
    text = re.sub(r'\s+', ' ', text).strip()
    # Kürzel in Klammern entfernen z.B. "(SG)", "(NR)"
    text = re.sub(r'\([A-Z]{2}\)', '', text)
    return text

def process_all_talkshows():
    all_chunks_count = 0
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        for folder in INPUT_FOLDERS:
            if not os.path.exists(folder):
                print(f"Ordner übersprungen: {folder} wurde nicht gefunden.")
                continue

            print(f"Verarbeite Sendung: {folder}...")
            
            for filename in os.listdir(folder):
                if not filename.endswith(".srt"):
                    continue
                
                try:
                    if " - " in filename:
                        parts = filename.split(" - ", 1)
                        datum = parts[0].strip()
                        rest = parts[1]
                        
                        titel = rest
                        for ending in ENDINGS_TO_REMOVE:
                            if titel.endswith(ending):
                                titel = titel[:-len(ending)]
                        titel = titel.strip()
                    else:
                        datum = "unknown"
                        titel = filename
                except Exception as e:
                    print(f"Fehler bei {filename}: {e}")
                    continue

                file_path = os.path.join(folder, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                clean_text = clean_srt(content)
                words = clean_text.split()
                
                for i in range(0, len(words), WORDS_PER_CHUNK):
                    chunk_words = words[i:i + WORDS_PER_CHUNK]
                    
                    # Kurze Chunks überspringen
                    if len(chunk_words) < 50:
                        continue

                    data_point = {
                        "show": folder,
                        "sender": SENDER[folder],
                        "date": datum,
                        "title": titel,
                        "text": " ".join(chunk_words),
                        "chunk_id": i // WORDS_PER_CHUNK
                    }
                    
                    outfile.write(json.dumps(data_point, ensure_ascii=False) + "\n")
                    all_chunks_count += 1

    print(f"Fertig! Insgesamt {all_chunks_count} Chunks gespeichert.")

if __name__ == "__main__":
    process_all_talkshows()