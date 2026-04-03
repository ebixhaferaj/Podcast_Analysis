import json
import re
import os
from collections import defaultdict, Counter

import matplotlib.pyplot as plt
from wordcloud import WordCloud

# ── Konfiguration ──────────────────────────────────────────────────────────────

JSON_PATH       = "talkshow_results_topics.jsonl"
STOPWORDS_PATH  = "german_stopwords_full.txt"
OUTPUT_DIR      = "wordclouds"
MIN_CONFIDENCE  = 0.0   # Nur Chunks ab diesem Confidence-Wert verwenden
MAX_WORDS       = 80    # Maximale Anzahl Wörter pro Wolke

# Farbschema pro Kategorie (Matplotlib-Colormaps)
CATEGORY_COLORS = {
    "International": "Blues",
    "Civil":         "Reds",
    "Government":    "Greens",
    "Law":           "Purples",
    "Politics":      "Oranges",
    "Economy":       "YlOrBr",
    "Society":       "PuRd",
}
DEFAULT_COLORMAP = "viridis"

# ── Schritt 1: Stopwörter laden ────────────────────────────────────────────────

def load_stopwords(path: str) -> set:
    stopwords = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(";"):
                continue
            stopwords.add(line.lower())
    return stopwords

# ── Schritt 2: Chunks laden ────────────────────────────────────────────────────

def load_chunks(path: str) -> list:
    with open(path, encoding="utf-8") as f:
        content = f.read().strip()
    try:
        data = json.loads(content)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        return [json.loads(line) for line in content.splitlines() if line.strip()]

# ── Schritt 3: Nach Kategorie gruppieren ───────────────────────────────────────

def group_by_category(chunks: list, min_confidence: float) -> dict:
    groups = defaultdict(list)
    for chunk in chunks:
        if chunk.get("confidence", 1.0) >= min_confidence and chunk.get("text"):
            groups[chunk["topic"]].append(chunk["text"])
    return dict(groups)

# ── Schritte 4–7: Text bereinigen, tokenisieren, zählen, Wolke bauen ──────────

def clean_and_tokenize(text: str, stopwords: set, min_length: int = 3) -> list:
    # Kleinschreibung
    text = text.lower()
    # Nur Buchstaben behalten
    text = re.sub(r"[^a-zäöüß\s]", " ", text)
    # Mehrfache Leerzeichen normalisieren
    text = re.sub(r"\s+", " ", text).strip()
    # In Wörter aufteilen, Stopwörter und kurze Wörter entfernen
    return [w for w in text.split() if w not in stopwords and len(w) >= min_length]


def make_wordcloud(texts: list, category: str, stopwords: set, output_dir: str) -> Counter:
    # Alle Texte der Kategorie zusammenführen und tokenisieren
    all_tokens = []
    for text in texts:
        all_tokens.extend(clean_and_tokenize(text, stopwords))

    if not all_tokens:
        print(f"  [!] Keine Tokens für '{category}' – übersprungen.")
        return Counter()

    # Wörter zählen
    word_frequencies = Counter(all_tokens)

    # Wortwolke erstellen
    colormap = CATEGORY_COLORS.get(category, DEFAULT_COLORMAP)
    wc = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        colormap=colormap,
        max_words=MAX_WORDS,
        collocations=False,      # Keine Wortpaare, nur Einzelwörter
        prefer_horizontal=0.85,  # 85 % der Wörter horizontal ausrichten
    ).generate_from_frequencies(word_frequencies)

    # Bild speichern
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"wordcloud_{category}.png")

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(
        f"Kategorie: {category}  ({len(texts)} Chunk{'s' if len(texts) != 1 else ''})",
        fontsize=16, fontweight="bold", pad=14
    )
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✓ Gespeichert: {filepath}")

    return word_frequencies


# ── Hauptprogramm ──────────────────────────────────────────────────────────────

def main():
    stopwords = load_stopwords(STOPWORDS_PATH)

    print(f"Lade Chunks aus: {JSON_PATH}")
    chunks = load_chunks(JSON_PATH)
    print(f"  → {len(chunks)} Chunks geladen.")

    category_texts = group_by_category(chunks, MIN_CONFIDENCE)
    for cat, texts in sorted(category_texts.items()):
        print(f"  {cat:20s}: {len(texts)} Chunks")

    print(f"\nErstelle Wortwolken → {OUTPUT_DIR}/")
    all_frequencies = {}
    for cat, texts in sorted(category_texts.items()):
        freq = make_wordcloud(texts, cat, stopwords, OUTPUT_DIR)
        if freq:
            all_frequencies[cat] = freq

    print("\nFertig! Dateien liegen in:", os.path.abspath(OUTPUT_DIR))


if __name__ == "__main__":
    main()