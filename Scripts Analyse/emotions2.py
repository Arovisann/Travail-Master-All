import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === PARAMÈTRES ===
csv_path = r"C:\chemin\vers\fusion_emotions_bpm_taches2.csv"  # Remplace ce chemin par le tien
output_folder = os.path.dirname(csv_path)

# === CHARGEMENT DES DONNÉES ===
df = pd.read_csv(csv_path)

# Filtrer les lignes avec tâche définie
df = df[df['task'] != 'outside_range'].copy()
df['dominant_emotion'] = df['dominant_emotion'].fillna('neutral')

# Créer une colonne par tranches de 3 secondes
df['timestamp_bin'] = (df['timestamp_sec'] // 3) * 3

# === PLOT PAR TÂCHE ===
tasks = df['task'].unique()

for task in sorted(tasks):
    df_task = df[df['task'] == task]

    # Compter les émotions par intervalle
    emotion_counts = df_task.groupby(['timestamp_bin', 'dominant_emotion']).size().unstack(fill_value=0)

    # Création de la heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(emotion_counts.T, cmap='YlOrRd', cbar_kws={'label': 'Occurrences'})
    plt.title(f"Évolution des émotions – {task}")
    plt.xlabel("Temps (s)")
    plt.ylabel("Émotion dominante")
    plt.tight_layout()

    # Sauvegarde
    output_path = os.path.join(output_folder, f"heatmap_emotions_{task}.png")
    plt.savefig(output_path)
    plt.close()

print("✅ Heatmaps des émotions par tâche générées avec succès.")
