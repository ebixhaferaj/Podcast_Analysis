###Code von Jacob Tunger###

import matplotlib.pyplot as plt
import numpy as np

data = {
    'agriculture': 47, 'civil': 500, 'culture': 11, 'defense': 951,
    'domestic': 217, 'education': 36, 'energy': 79, 'environment': 43,
    'foreign': 82, 'government': 1760, 'health': 154, 'housing': 40,
    'immigration': 202, 'international': 2206, 'labor': 245, 'law': 159,
    'macroeconomics': 473, 'public': 1, 'social': 500, 'technology': 129,
    'transportation': 14
}

# Nach Wert sortieren (absteigend)
sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))

categories = list(sorted_data.keys())
values = list(sorted_data.values())

colors = plt.cm.tab20(np.linspace(0, 1, len(categories)))

fig, ax = plt.subplots(figsize=(14, 6))

bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=0.5)

ax.set_xlabel('Kategorie', fontsize=12)
ax.set_ylabel('Anzahl', fontsize=12)
ax.set_title('Verteilung nach Kategorien', fontsize=14, fontweight='bold')
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories, rotation=45, ha='right', fontsize=9)
ax.yaxis.grid(True, linestyle='--', alpha=0.4)
ax.set_axisbelow(True)

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 15,
            str(val), ha='center', va='bottom', fontsize=7.5)

plt.tight_layout()
plt.savefig('kategorien.png', dpi=300, bbox_inches='tight')
plt.show()