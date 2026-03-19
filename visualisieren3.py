import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Daten laden
df = pd.read_json("talkshow_results_topics.jsonl", lines=True)
df['date'] = pd.to_datetime(df['date'])

# --- TEIL B: Normalisierter Show-Vergleich (Themen-Profile) ---

# Wir berechnen für jede Show, wie viel Prozent jedes Thema einnimmt
show_profiles = df.groupby(['show', 'topic']).size().unstack(fill_value=0)
show_profiles_norm = show_profiles.div(show_profiles.sum(axis=1), axis=0).reset_index()

# Umwandeln für Seaborn (Melt)
df_plot = show_profiles_norm.melt(id_vars='show', var_name='topic', value_name='percentage')
# Nur Top Themen zeigen
top_overall = df['topic'].value_counts().nlargest(8).index
df_plot = df_plot[df_plot['topic'].isin(top_overall)]

plt.figure(figsize=(14, 7))
sns.barplot(data=df_plot, x='topic', y='percentage', hue='show', palette='viridis')
plt.title('Themen-Profile der Sendungen (Normalisierter Vergleich)', fontsize=15)
plt.ylabel('Relativer Anteil (0.0 - 1.0)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()