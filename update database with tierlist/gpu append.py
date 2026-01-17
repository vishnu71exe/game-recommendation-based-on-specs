import sqlite3
import csv
import re

def normalise(text):
    text = text.lower()
    text = text.replace("/", " ").replace("-", " ")
    text = re.sub(r"[^a-z0-9 ]", " ", text)

    words = text.split()
    fixed_words = []
    for w in words:
        fixed_words += re.findall(r"[a-z]+|\d+", w)

    remove = {
        "nvidia","amd","geforce","graphics","graphic",
        "equivalent","or","greater","than",
        "minimum","recommended","series",
        "video","card","gpu","with","and"
    }

    return " ".join(w for w in fixed_words if w not in remove)


def gpu_tier(score):
    if score >= 20000:
        return "Ultra"
    elif score >= 12000:
        return "High"
    elif score >= 7000:
        return "Medium"
    elif score >= 3000:
        return "Low"
    else:
        return "Very Low"


# ---------- Load GPU reference ----------
gpu_ref = {}
with open("data/gpu_data.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    for name, score in reader:
        gpu_ref[name] = int(score)

# ---------- DB ----------
conn = sqlite3.connect("data6_partial.db")
cur = conn.cursor()

cur.execute("SELECT appid, graphics FROM sreq_min")
rows = cur.fetchall()

matched = 0

for appid, gpu_text in rows:
    if not gpu_text:
        continue

    gpu_text_n = normalise(gpu_text)

    best_score = 0
    best_gpu = None

    for name, score in gpu_ref.items():
        if normalise(name) in gpu_text_n:
            if score > best_score:
                best_score = score
                best_gpu = name

    if best_gpu:
        tier = gpu_tier(best_score)

        cur.execute("""
            UPDATE sreq_min
            SET gpu_score = ?, gpu_tier = ?
            WHERE appid = ?
        """, (best_score, tier, appid))

        matched += 1

conn.commit()
print("Matched GPUs:", matched)
