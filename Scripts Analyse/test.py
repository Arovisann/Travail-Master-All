import pandas as pd
import numpy as np

# === PARAMÈTRES À ADAPTER ===
fichier_emotions = r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 3\3\3\gaze_emotion_data_1747762167.csv"
fichier_bpm = r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 3\3\3\bpm_par_timestamp.csv"
fichier_sortie = r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 3\3\3\fusion_emotions_bpm_taches.csv"
flags = [704.49,758.43,997.30,1078.95]  # timestamps (en secondes) marquant la fin de chaque tâche

# === 1. CHARGER LES DONNÉES ===
df_emotions = pd.read_csv(fichier_emotions)
df_bpm = pd.read_csv(fichier_bpm)

# Renommer pour harmoniser
df_bpm = df_bpm.rename(columns={"Timestamp (s)": "timestamp_sec"})

# === 2. INTERPOLATION DES BPM ===
# On crée une interpolation linéaire à partir des données BPM valides
df_bpm_clean = df_bpm.dropna()
bpm_interp = np.interp(df_emotions["timestamp_sec"], df_bpm_clean["timestamp_sec"], df_bpm_clean["BPM"])
df_emotions["BPM"] = bpm_interp

# === 3. ATTRIBUTION DES TÂCHES ===
boundaries = [0] + flags
tasks = [f"task_{i+1}" for i in range(len(flags))]

def assign_task(ts):
    for i in range(len(boundaries)-1):
        if boundaries[i] <= ts < boundaries[i+1]:
            return tasks[i]
    return "outside_range"

df_emotions["task"] = df_emotions["timestamp_sec"].apply(assign_task)

# === 4. SAUVEGARDE ===
df_emotions.to_csv(fichier_sortie, index=False)

print(f"✅ Fusion terminée. Fichier enregistré sous : {fichier_sortie}")
