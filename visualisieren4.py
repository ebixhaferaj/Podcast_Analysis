import pandas as pd
import matplotlib.pyplot as plt

# 1. Daten laden
df = pd.read_json("talkshow_results_topics.jsonl", lines=True)

# 2. Shows identifizieren
shows = df['show'].unique()

# 3. Für jede Show ein Diagramm erstellen
for show in shows:
    # Daten für die aktuelle Show filtern
    show_df = df[df['show'] == show]
    
    # Themen zählen
    topic_counts = show_df['topic'].value_counts()
    
    # Optional: Kleinstthemen zusammenfassen (für die Lesbarkeit)
    # Alles unter 3% wird zu "Other"
    total = topic_counts.sum()
    big_topics = topic_counts[topic_counts / total > 0.03]
    small_topics_sum = topic_counts[topic_counts / total <= 0.03].sum()
    if small_topics_sum > 0:
        big_topics['Other'] = small_topics_sum
    
    # Plot erstellen
    plt.figure(figsize=(10, 8))
    plt.pie(
        big_topics, 
        labels=big_topics.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=plt.cm.Paired.colors,
        explode=[0.05 if i == 0 else 0 for i in range(len(big_topics))] # Hebt das größte Stück leicht ab
    )
    
    plt.title(f'Thematisches Profil: {show}', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()