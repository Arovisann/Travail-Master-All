import pandas as pd
import numpy as np

# Charger les fichiers
# df_eyetracker = pd.read_csv(r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 2\1\gaze_emotion_data_1747750592.csv")   # ou ton nom de fichier réel
# df_bpm = pd.read_csv(r"C:\Users\alexa\OneDrive\Documents\GitHub\Master-Analysis\bpm_par_timestamp.csv")


import pandas as pd

# === PARAMÈTRES ===
FICHIER_EYE = r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 2\1\gaze_emotion_data_1747750592.csv"
FICHIER_BPM = r"C:\Users\alexa\OneDrive\Documents\GitHub\Master-Analysis\bpm_par_timestamp.csv"
FICHIER_SORTIE = '1eyetracker_emotions_bpm.csv'
TOLERANCE_SECONDES = 0.5  # maximum de différence autorisée entre les timestamps

# === CHARGEMENT DES DONNÉES ===
df_eye = pd.read_csv(FICHIER_EYE)
df_bpm = pd.read_csv(FICHIER_BPM)

# Renommer pour fusion correcte
df_bpm = df_bpm.rename(columns={'Timestamp (s)': 'timestamp_sec'})

# Tri obligatoire pour merge_asof
df_eye = df_eye.sort_values('timestamp_sec')
df_bpm = df_bpm.sort_values('timestamp_sec')

# === FUSION AVEC BPM LE PLUS PROCHE ===
df_fusion = pd.merge_asof(
    df_eye,
    df_bpm,
    on='timestamp_sec',
    direction='nearest',
    tolerance=TOLERANCE_SECONDES
)

# === EXPORT ===
df_fusion.to_csv(FICHIER_SORTIE, index=False)
print(f"✅ Fusion terminée : fichier exporté sous '{FICHIER_SORTIE}'")

