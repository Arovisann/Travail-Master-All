import pandas as pd
import matplotlib.pyplot as plt

# === PARAMÈTRES ===
csv_path = r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 1\2\2\fusion_emotions_bpm_taches2.csv"
task_names = ["task_1", "task_2", "task_3", "task_4"]

# === CHARGEMENT DES DONNÉES ===
df = pd.read_csv(csv_path)
df = df[df['task'].isin(task_names)]
df = df.dropna(subset=["dominant_emotion", "timestamp_sec"])

# === CRÉATION DU GRAPHE SEGMENTÉ PAR TÂCHE ===
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
axes = axes.flatten()

for i, task in enumerate(task_names):
    df_task = df[df["task"] == task].copy()
    df_task["time_bin"] = (df_task["timestamp_sec"] // 3) * 3

    emotion_counts_task = df_task.groupby(["time_bin", "dominant_emotion"]).size().unstack(fill_value=0)
    emotion_counts_reset = emotion_counts_task.reset_index().melt(id_vars='time_bin', var_name='emotion', value_name='count')
    pivot_data = emotion_counts_reset.pivot(index="time_bin", columns="emotion", values="count").fillna(0)

    x = pivot_data.index
    y = [pivot_data[emotion].values for emotion in pivot_data.columns]

    axes[i].stackplot(x, y, labels=pivot_data.columns)
    axes[i].set_title(f"Émotions durant {task.replace('_', ' ').title()}")
    axes[i].set_xlabel("Temps (s)")
    axes[i].set_ylabel("Occurrences")
    axes[i].legend(loc='upper left', fontsize=8)

plt.suptitle("Évolution des émotions segmentée par tâche (fenêtres de 3s)", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
