import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Ebi Xhaferaj

# =========================
# 1. Load Data
# =========================
df = pd.read_json("talkshow_results_topics.jsonl", lines=True)
df['date'] = pd.to_datetime(df['date'])

# =========================
# 2. Function: Timeline with all months in the X-Axis
# =========================
def plot_show_timeline(show_name, rolling_window=2):
    df_show = df[df['show'] == show_name].copy()
    
    selected_topics = ['defense', 'government', 'international', 'macroeconomics', 'social']
    df_show = df_show[df_show['topic'].str.lower().isin(selected_topics)]
    
    # Group by Month
    df_timeline = df_show.groupby(
        [pd.Grouper(key='date', freq='MS'), 'topic']  # MS = Month Start
    ).size().unstack(fill_value=0)
    
    # Ensure ALL months are present (no gaps)
    full_index = pd.date_range(
        start=df_timeline.index.min(),
        end=df_timeline.index.max(),
        freq='MS'
    )
    df_timeline = df_timeline.reindex(full_index, fill_value=0)
    
    # Rolling Average
    df_timeline_smooth = df_timeline.rolling(window=rolling_window, min_periods=1).mean()
    
    fixed_colors = {
        'international': 'red',
        'defense': 'orange',
        'government': 'green'
    }
    
    plt.figure(figsize=(14,7))
    sns.set_style("whitegrid")
    
    for topic in df_timeline_smooth.columns:
        color = fixed_colors.get(topic.lower(), None)
        plt.plot(
            df_timeline_smooth.index,
            df_timeline_smooth[topic],
            marker='o',
            label=topic,
            linewidth=2,
            color=color
        )
    
    # ----SHOW ALL MONTHS ----
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator())         
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  
    plt.xticks(rotation=45)
    
    # Events
    event_dates = {
        'Russia-Ukraine Anniversary': pd.Timestamp('2026-02-24'),
        'Haushaltsdebatte 2025': pd.Timestamp('2025-11-25')
    }
    
    for event, date in event_dates.items():
        plt.axvline(x=date, linestyle='--', alpha=0.7)
        plt.text(date, plt.ylim()[1]*0.95, event, rotation=90, va='top')
    
    plt.title(f'Themen-Entwicklung bei {show_name}', fontsize=16)
    plt.xlabel('Zeit (Monate)')
    plt.ylabel('Anzahl Chunks')
    plt.legend(title='Topics', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()

# =========================
# 3. Talkshows
# =========================
plot_show_timeline('Lanz')
plot_show_timeline('Maischberger')
plot_show_timeline('Miosga')
plot_show_timeline('HartAberFair')
plot_show_timeline('Illner')