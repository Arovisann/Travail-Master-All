import pandas as pd
import numpy as np

# Charger les deux fichiers CSV
eyetracker_df = pd.read_csv("gaze_emotion_data_1746690062.csv")
bitalino_df = pd.read_csv("bpm_par_timestamp.csv")

# Renommer les colonnes pour uniformiser (optionnel selon noms exacts)
bitalino_df.columns = ["timestamp_sec", "bpm"]

# Ajouter une colonne bpm vide
eyetracker_df["bpm"] = np.nan

# Associer à chaque timestamp du fichier eyetracker la BPM la plus proche
for i, ts in enumerate(eyetracker_df["timestamp_sec"]):
    closest_index = (bitalino_df["timestamp_sec"] - ts).abs().idxmin()
    eyetracker_df.at[i, "bpm"] = bitalino_df.at[closest_index, "bpm"]

# Sauvegarde dans un nouveau fichier CSV
eyetracker_df.to_csv("eyetracker_emotions_bpm.csv", index=False)

print("Fusion terminée. Fichier sauvegardé sous : eyetracker_emotions_bpm.csv")
