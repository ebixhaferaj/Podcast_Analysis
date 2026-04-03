import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Daten laden
df = pd.read_json("talkshow_results_topics.jsonl", lines=True)

# 2. Vorbereitung: Nur Lanz & Datum konvertieren
df_lanz = df[df['show'] == 'Lanz'].copy()
df_lanz['date'] = pd.to_datetime(df_lanz['date'])

# 3. Die Top 5 Themen bei Lanz finden (damit die Grafik übersichtlich bleibt)
top_topics = df_lanz['topic'].value_counts().nlargest(5).index
df_top = df_lanz[df_lanz['topic'].isin(top_topics)]

# 4. Daten nach Monat und Thema gruppieren
# Wir zählen, wie oft jedes Thema pro Monat vorkommt
df_timeline = df_top.groupby([pd.Grouper(key='date', freq='ME'), 'topic']).size().unstack(fill_value=0)

# 5. Plotten
plt.figure(figsize=(14, 7))
sns.set_style("whitegrid")

# Wir zeichnen für jedes Top-Thema eine Linie
for topic in df_timeline.columns:
    plt.plot(df_timeline.index, df_timeline[topic], marker='o', label=topic, linewidth=2)

plt.title('Themen-Entwicklung bei Markus Lanz (Top 5 Themen)', fontsize=16)
plt.xlabel('Zeitverlauf (Monate)', fontsize=12)
plt.ylabel('Anzahl der Diskussions-Chunks', fontsize=12)
plt.legend(title='Politik-Felder', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()