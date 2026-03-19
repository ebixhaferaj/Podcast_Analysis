import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Daten laden
df = pd.read_json("talkshow_results_topics.jsonl", lines=True)

# Top Themen zählen
plt.figure(figsize=(12, 6))
sns.countplot(data=df, y='topic', order=df['topic'].value_counts().index, palette='viridis')
plt.title('Häufigste Themen in allen Talkshows')
plt.xlabel('Anzahl der Chunks')
plt.ylabel('Thema')
plt.show()

# Die Top 5 Themen filtern, sonst wird die Grafik zu voll
top_topics = df['topic'].value_counts().nlargest(5).index
df_filtered = df[df['topic'].isin(top_topics)]

plt.figure(figsize=(14, 7))
sns.countplot(data=df_filtered, x='topic', hue='show', palette='muted')
plt.title('Themenvergleich nach Talkshow')
plt.xticks(rotation=45)
plt.legend(title='Sendung')
plt.show()