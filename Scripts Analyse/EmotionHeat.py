import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === PARAMÈTRES ===
csv_path = r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 1\2\2\fusion_emotions_bpm_taches2.csv"
task_names = ["task_1", "task_2", "task_3", "task_4"]

# === CHARGEMENT DES DONNÉES ===
df = pd.read_csv(csv_path)
df = df[df['task'].isin(task_names)]
df = df.dropna(subset=["dominant_emotion", "timestamp_sec"])

# === CRÉATION DES HEATMAPS PAR TÂCHE ===
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
axes = axes.flatten()

for i, task in enumerate(task_names):
    df_task = df[df["task"] == task].copy()
    df_task["time_bin"] = (df_task["timestamp_sec"] // 3) * 3
    heatmap_data = df_task.groupby(["time_bin", "dominant_emotion"]).size().unstack(fill_value=0)

    sns.heatmap(heatmap_data.T, cmap="YlOrRd", cbar_kws={'label': 'Occurrences'}, ax=axes[i], linewidths=.5)
    axes[i].set_title(f"Carte thermique des émotions – {task.replace('_', ' ').title()}")
    axes[i].set_xlabel("Temps (s)")
    axes[i].set_ylabel("Émotions")

plt.suptitle("Évolution des émotions par tâche – Heatmaps (fenêtres de 3s)", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
