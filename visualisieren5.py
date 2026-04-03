import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Daten laden
df = pd.read_json("talkshow_results_topics.jsonl", lines=True)
df['date'] = pd.to_datetime(df['date'])

# 2. Aggregation: Thema pro Sendung bestimmen
# Wir gruppieren nach Datum und Sendungsname, um eine einzelne Show zu identifizieren
# Dann nehmen wir das Thema, das am häufigsten vorkommt (Mode)
def get_main_topic(series):
    return series.mode().iloc[0] if not series.empty else None

# Wir gruppieren und behalten das Datum bei
df_shows = df.groupby(['date', 'show'])['topic'].agg(get_main_topic).reset_index()

# 3. Filter für Markus Lanz
df_lanz_shows = df_shows[df_shows['show'] == 'Lanz'].copy()

# 4. Top 5 Hauptthemen für die Übersicht finden
top_main_topics = df_lanz_shows['topic'].value_counts().nlargest(5).index
df_lanz_top = df_lanz_shows[df_lanz_shows['topic'].isin(top_main_topics)]

# 5. Daten für die Visualisierung vorbereiten (Monatliche Zählung der Hauptthemen)
df_timeline = df_lanz_top.groupby([pd.Grouper(key='date', freq='ME'), 'topic']).size().unstack(fill_value=0)

# 6. Plotten
plt.figure(figsize=(14, 7))
sns.set_style("whitegrid")

for topic in df_timeline.columns:
    plt.plot(df_timeline.index, df_timeline[topic], marker='o', label=topic, linewidth=2)

plt.title('Hauptthemen pro Sendung bei Markus Lanz (Zeitverlauf)', fontsize=16)
plt.xlabel('Zeitverlauf (Monate)', fontsize=12)
plt.ylabel('Anzahl der Sendungen mit diesem Hauptthema', fontsize=12)
plt.legend(title='Hauptthemen', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()