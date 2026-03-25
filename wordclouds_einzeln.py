"""
Wortwolken-Generator
--------------------
Eingabe:  JSON/NDJSON-Datei mit Chunks, jeder mit 'text' und 'topic'
Ausgabe:  wordclouds/wordcloud_<Kategorie>.png

Wie wird eine Wortwolke gebaut?
================================

1. TEXT SAMMELN
   Alle Texte einer Kategorie werden zusammengeführt.

2. TEXT BEREINIGEN
   Der Text wird in Kleinbuchstaben umgewandelt.
   Alles außer Buchstaben (Zahlen, Satzzeichen) wird entfernt.

3. TOKENISIEREN
   Der bereinigte Text wird in einzelne Wörter ("Tokens") aufgeteilt.

4. STOPWÖRTER ENTFERNEN
   Häufige, bedeutungslose Wörter ("und", "der", "ist", ...) werden
   herausgefiltert. Sie würden sonst die Wolke dominieren, obwohl sie
   nichts über den Inhalt aussagen.

5. WÖRTER ZÄHLEN
   Für jedes verbleibende Wort wird gezählt, wie oft es vorkommt.

6. WORTWOLKE RENDERN
   Die WordCloud-Bibliothek ordnet die Wörter so an, dass häufige Wörter
   größer dargestellt werden. Die Anordnung ist zufällig, aber platzsparend.
   Ein Farbschema (Colormap) wird pro Kategorie festgelegt.

7. SPEICHERN
   Das fertige Bild wird als PNG gespeichert.
"""

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
    """Bereinigt Text und gibt eine Liste gefilterter Wörter zurück."""
    # Kleinschreibung
    text = text.lower()
    # Nur Buchstaben behalten
    text = re.sub(r"[^a-zäöüß\s]", " ", text)
    # Mehrfache Leerzeichen normalisieren
    text = re.sub(r"\s+", " ", text).strip()
    # In Wörter aufteilen, Stopwörter und kurze Wörter entfernen
    return [w for w in text.split() if w not in stopwords and len(w) >= min_length]


def make_wordcloud(texts: list, category: str, stopwords: set, output_dir: str) -> Counter:
    """Erstellt Wortwolke und gibt die Worthäufigkeiten zurück."""
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


# ── Wortlisten exportieren ─────────────────────────────────────────────────────

def export_word_lists_optimized(
    all_frequencies: dict,
    output_dir: str,
    top_n: int = 40,
    compress: bool = True,
    use_vocab: bool = True
):
    """
    Optimierter Export der Worthäufigkeiten.

    Features:
    - reduziert auf Top-N Wörter pro Kategorie
    - speichert kompakt (kein Pretty-Print)
    - optional gzip-Kompression
    - optional Vokabular-Encoding (vermeidet doppelte Strings)

    Ausgabeformate:

    use_vocab=False:
      { "Politik": {"regierung": 42, ...}, ... }

    use_vocab=True:
      {
        "vocab": ["regierung", "deutschland", ...],
        "data": {
          "Politik": [[0, 42], [1, 38]]
        }
      }
    """
    os.makedirs(output_dir, exist_ok=True)

    # ── Schritt 1: Top-N reduzieren ─────────────────────
    reduced = {
        cat: freq.most_common(top_n)
        for cat, freq in all_frequencies.items()
    }

    # ── Schritt 2: Optional Vokabular bauen ─────────────
    if use_vocab:
        vocab = {}
        vocab_list = []
        next_id = 0

        data = {}

        for cat, words in reduced.items():
            encoded = []
            for word, count in words:
                if word not in vocab:
                    vocab[word] = next_id
                    vocab_list.append(word)
                    next_id += 1
                encoded.append([vocab[word], count])
            data[cat] = encoded

        export_data = {
            "vocab": vocab_list,
            "data": data
        }

    else:
        export_data = {
            cat: dict(words)
            for cat, words in reduced.items()
        }

    # ── Schritt 3: Speichern ────────────────────────────
    filename = "wordcloud_woerter_optimized.json"

    if compress:
        import gzip
        filepath = os.path.join(output_dir, filename + ".gz")
        with gzip.open(filepath, "wt", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, separators=(",", ":"))
    else:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, separators=(",", ":"))

    print(f"  ✓ Optimierte Wortlisten gespeichert: {filepath}")


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

    print("\nExportiere Wortlisten ...")
    export_word_lists_optimized(
        all_frequencies,
        OUTPUT_DIR,
        top_n=40,        # kannst du anpassen
        compress=True,   # gzip aktivieren
        use_vocab=True   # maximale Kompression
)

    print("\nFertig! Dateien liegen in:", os.path.abspath(OUTPUT_DIR))


if __name__ == "__main__":
    main()