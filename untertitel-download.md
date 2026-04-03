# Untertitel-Download 

Dieses Skript lädt automatisch deutsche Untertitel (`.srt`) von den wichtigsten politischen Talkshows in der ZDF- und ARD-Mediathek herunter.

## Voraussetzungen

- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) muss installiert sein
- Nur Episoden **ab dem 01.03.2025** werden berücksichtigt
- Folgen unter **45 Minuten** und Gebärdensprach-Fassungen werden übersprungen

---

## Befehlsübersicht

Die folgenden Befehle können einzeln oder nacheinander ausgeführt werden. Jeder Befehl lädt die Untertitel einer Sendung herunter. Die Dateien werden im aktuellen Verzeichnis gespeichert, benannt nach dem Schema `YYYY-MM-DD - Titel.srt`.

---

### Maybrit Illner (ZDF Mediathek)

```bash
yt-dlp \
  --skip-download \
  --write-subs --sub-lang deu --convert-subs srt \
  --dateafter 20250301 \
  --match-filter 'duration >= 2700 & title !~= "(?i)gebärdensprache"' \
  -o "%(upload_date>%Y-%m-%d)s - %(title)s.%(ext)s" \
  "https://www.zdf.de/talk/maybrit-illner-128"
```

---

### Maischberger (ARD Mediathek)

```bash
yt-dlp \
  --skip-download \
  --write-subs --sub-lang deu --convert-subs srt \
  --dateafter 20250301 \
  --match-filter 'duration >= 2700 & title !~= "(?i)gebärdensprache"' \
  -o "%(upload_date>%Y-%m-%d)s - %(title)s.%(ext)s" \
  "https://www.ardmediathek.de/sendung/maischberger/Y3JpZDovL2Rhc2Vyc3RlLmRlL21lbnNjaGVuIGJlaSBtYWlzY2hiZXJnZXI"
```

---

### Caren Miosga (ARD Mediathek)

```bash
yt-dlp \
  --skip-download \
  --write-subs --sub-lang deu --convert-subs srt \
  --dateafter 20250301 \
  --match-filter 'duration >= 2700 & title !~= "(?i)gebärdensprache"' \
  -o "%(upload_date>%Y-%m-%d)s - %(title)s.%(ext)s" \
  "https://www.ardmediathek.de/sendung/caren-miosga/Y3JpZDovL2Rhc2Vyc3RlLmRlL2NhcmVuLW1pb3NnYQ"
```

---

### Hart aber fair (ARD Mediathek)

```bash
yt-dlp \
  --skip-download \
  --write-subs --sub-lang deu --convert-subs srt \
  --dateafter 20250301 \
  --match-filter 'duration >= 2700 & title !~= "(?i)gebärdensprache"' \
  -o "%(upload_date>%Y-%m-%d)s - %(title)s.%(ext)s" \
  "https://www.ardmediathek.de/sendung/hart-aber-fair/Y3JpZDovL3dkci5kZS9oYXJ0IGFiZXIgZmFpcg"
```

---

### Markus Lanz (ZDF Mediathek)

```bash
yt-dlp \
  --skip-download \
  --write-subs --sub-lang deu --convert-subs srt \
  --dateafter 20250301 \
  --match-filter 'duration >= 2700 & title !~= "(?i)gebärdensprache"' \
  -o "%(upload_date>%Y-%m-%d)s - %(title)s.%(ext)s" \
  "https://www.zdf.de/talk/markus-lanz-114"
```

---

## Parameter-Erklärung

| Parameter | Bedeutung |
|---|---|
| `--skip-download` | Lädt nur Untertitel, kein Video |
| `--write-subs` | Untertiteldatei herunterladen |
| `--sub-lang deu` | Nur deutsche Untertitel |
| `--convert-subs srt` | Konvertierung ins `.srt`-Format |
| `--dateafter 20250301` | Nur Episoden ab 01.03.2025 |
| `--match-filter 'duration >= 2700'` | Nur Folgen ≥ 45 Minuten |
| `--match-filter '... !~= "(?i)gebärdensprache"'` | Gebärdensprach-Fassungen ausschließen |
| `-o "..."` | Ausgabedateiname: `YYYY-MM-DD - Titel.srt` |
