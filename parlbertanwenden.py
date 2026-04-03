import torch
from datasets import load_dataset
from transformers import pipeline
import json
import time

# 1. Device-Check (M-Chip Beschleunigung)
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Nutze Device: {device}")

# 2. Daten & Modell Konfiguration
INPUT_FILE = "talkshow_data_for_bert.jsonl"
OUTPUT_FILE = "talkshow_results_topics.jsonl"
MODEL_NAME = "chkla/parlbert-topic-german"

# Daten laden
dataset = load_dataset('json', data_files=INPUT_FILE)['train']

# 3. Pipeline initialisieren
# Wir setzen return_all_scores=False, um nur das wahrscheinlichste Thema zu bekommen
classifier = pipeline(
    "text-classification", 
    model=MODEL_NAME, 
    device=device
)

# 4. Batch-Verarbeitung
def process_batch(batch):
    results = classifier(batch["text"], truncation=True, max_length=512)
    batch["topic"] = [r["label"] for r in results]
    batch["confidence"] = [r["score"] for r in results]
    return batch

# 5. Startschuss
start_time = time.time()
print(f"Klassifiziere {len(dataset)} Chunks...")

# batched=True und eine Batch-Größe von 16-32 nutzt die GPU effizient aus
results_dataset = dataset.map(
    process_batch, 
    batched=True, 
    batch_size=32, 
    desc="Themen-Analyse"
)

# 6. Speichern
results_dataset.to_json(OUTPUT_FILE, force_ascii=False)

end_time = time.time()
duration = (end_time - start_time) / 60
print(f"Fertig! Dauer: {duration:.2f} Minuten.")
print(f"Ergebnisse gespeichert in: {OUTPUT_FILE}")