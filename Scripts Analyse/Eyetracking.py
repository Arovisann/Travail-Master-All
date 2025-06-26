import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Charge le fichier CSV
df = pd.read_csv(r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 2\1\gaze_emotion_data_1747750592.csv") 

# Supprime les lignes avec des valeurs manquantes
df = df.dropna(subset=['timestamp_sec', 'left_x', 'left_y', 'right_x', 'right_y'])

# Moyenne des coordonnées gauche et droite pour une position "centrale" de l’œil
df['gaze_x'] = (df['left_x'] + df['right_x']) / 2
df['gaze_y'] = (df['left_y'] + df['right_y']) / 2

# Calcul de la distance euclidienne entre deux points consécutifs
df['distance'] = np.sqrt(df['gaze_x'].diff()**2 + df['gaze_y'].diff()**2)

# Temps en secondes
df['time'] = df['timestamp_sec'] - df['timestamp_sec'].iloc[0]

# Seuil de détection (95e percentile)
threshold = df['distance'].quantile(0.95)

# Détection des moments d'agitation prolongée
df['high_movement'] = df['distance'] > threshold
df['sequence'] = (
    df['high_movement'] &
    df['high_movement'].shift(1, fill_value=False) &
    df['high_movement'].shift(2, fill_value=False)
)

# Tracer
plt.figure(figsize=(16, 6))
plt.plot(df['time'], df['distance'], label="Distance (Mouvements oculaires)", color='blue')
plt.axhline(threshold, color='red', linestyle='--', label="Seuil 95e percentile")
plt.scatter(df[df['sequence']]['time'], df[df['sequence']]['distance'], color='orange', label="Agitation prolongée", s=20)

plt.xlabel("Temps (s)")
plt.ylabel("Distance entre points de fixation")
plt.title("Détection des mouvements oculaires inhabituels")
plt.legend()
plt.tight_layout()
plt.show()
