import pandas as pd
import os


def time_to_seconds(time_str):
    """Convert SRT time (HH:MM:SS,ms) to seconds."""
    h, m, s = time_str.split(":")
    s = s.replace(",", ".")
    return int(h) * 3600 + int(m) * 60 + float(s)

def get_next_episode_filename(folder="generated_episodes", prefix="ep", ext=".csv"):
    os.makedirs(folder, exist_ok=True)

    existing = [
        f for f in os.listdir(folder)
        if f.startswith(prefix) and f.endswith(ext)
    ]

    numbers = []
    for f in existing:
        try:
            num = int(f[len(prefix):-len(ext)])
            numbers.append(num)
        except:
            pass

    next_num = max(numbers, default=0) + 1
    return os.path.join(folder, f"{prefix}{next_num}{ext}")

def parse_srt(file_path):
    rows = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.isdigit():  # subtitle index
            segment_id = int(line)
            time_line = lines[i + 1].strip()
            start_time, end_time = time_line.split(" --> ")

            text_lines = []
            j = i + 2
            while j < len(lines) and lines[j].strip() != "":
                text_lines.append(lines[j].strip())
                j += 1

            text = " ".join(text_lines)

            rows.append({
                "segment_id": segment_id,
                "start_time": start_time,
                "end_time": end_time,
                "start_seconds": time_to_seconds(start_time),
                "end_seconds": time_to_seconds(end_time),
                "duration": time_to_seconds(end_time) - time_to_seconds(start_time),
                "text": text
            })

            i = j
        else:
            i += 1

    return pd.DataFrame(rows)


# Root folder where your channel subfolders are
root_folder = "untertitel-2026"

for channel_folder in os.listdir(root_folder):
    full_channel_path = os.path.join(root_folder, channel_folder)
    if os.path.isdir(full_channel_path):
        # Find SRT files in this channel folder
        for file_name in os.listdir(full_channel_path):
            if file_name.endswith(".srt"):
                srt_path = os.path.join(full_channel_path, file_name)
                print("Processing...")

                df = parse_srt(srt_path)
                csv_file = get_next_episode_filename()
                df.to_csv(csv_file, index=False, encoding="utf-8-sig")
                print("Saved")