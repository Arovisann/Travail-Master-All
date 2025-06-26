import pandas as pd

# Chargement des données
df = pd.read_csv(r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 2\1\gaze_emotion_data_1747750592.csv", header=None, names=["timestamp", "left_x", "left_y", "right_x", "right_y", "dominant_emotion"])

# Compter les émotions
emotion_counts = df["dominant_emotion"].value_counts()

# Convertir en pourcentage
emotion_percentages = (emotion_counts / emotion_counts.sum()) * 100

# Afficher proprement
print("Pourcentage des émotions détectées :")
print(emotion_percentages.round(2).to_string())

import matplotlib.pyplot as plt

# Reprendre les mêmes calculs que ci-dessus
emotion_counts = df["dominant_emotion"].value_counts()
emotion_percentages = (emotion_counts / emotion_counts.sum()) * 100

# Camembert
plt.figure(figsize=(8, 8))
plt.pie(emotion_percentages, labels=emotion_percentages.index, autopct='%1.1f%%', startangle=90)
plt.title("Répartition des émotions détectées")
plt.axis('equal')
plt.show()
