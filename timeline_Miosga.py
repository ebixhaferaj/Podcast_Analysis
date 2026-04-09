import pandas as pd
import matplotlib.pyplot as plt
import json

# Ebi Xhaferaj

# To assess the reliability of our methodology, we conducted a human evaluation. 
# In this section we use the visualizations to analyze how precisely the model was developed for classifying topics.
# For this evaluation, we consider the episodes from the Miosga Talkshow.

# --- Load data (JSONL) ---
file_path = "talkshow_results_topics.jsonl"

data = []
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        data.append(json.loads(line))

df = pd.DataFrame(data)

# --- Filter only Miosga episodes ---
df = df[df["show"] == "Miosga"].copy()

# --- Keep relevant columns ---
df = df[["title", "chunk_id", "topic", "confidence"]]

# --- Sort properly ---
df = df.sort_values(["title", "chunk_id"])

# =========================================================
# 1. CLEAN TABLE
# =========================================================
print("\n=== SAMPLE TABULAR DATA ===")
print(df.head(20))

# Optional: save to CSV
df.to_csv("miosga_all_chunks.csv", index=False)

# =========================================================
# 2. AGGREGATED VIEW (topic counts per episode)
# =========================================================
topic_counts = df.groupby(["title", "topic"]).size().unstack(fill_value=0)

print("\n=== TOPIC DISTRIBUTION PER EPISODE ===")
print(topic_counts)

# Optional: save
topic_counts.to_csv("miosga_topic_distribution.csv")

# =========================================================
# 4. VISUALIZATION — Timeline for each episode on Miosga
# =========================================================
for title, group in df.groupby("title"):
    group = group.sort_values("chunk_id")

    # encode topics
    group["topic_code"] = group["topic"].astype("category").cat.codes
    topic_map = dict(enumerate(group["topic"].astype("category").cat.categories))

    plt.figure()
    plt.plot(group["chunk_id"], group["topic_code"], marker='o')

    plt.yticks(list(topic_map.keys()), list(topic_map.values()))
    plt.title(f"Topic Flow: {title}")
    plt.xlabel("Chunk ID")
    plt.ylabel("Topic")
    plt.grid(True)
    plt.tight_layout()
    plt.show()