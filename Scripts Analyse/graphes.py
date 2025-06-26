# === SCRIPT BPM.PY ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
from scipy.ndimage import gaussian_filter
from statsmodels.nonparametric.smoothers_lowess import lowess
import os

# === Partie 1 : GRAPHE BPM ===
fichier = r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 3\3\3\fusion_emotions_bpm_taches.csv"
df = pd.read_csv(fichier)
output_dir = os.path.dirname(fichier)

df = df[df['task'] != 'outside_range'].copy()
df = df[df['BPM'].between(50, 100)]
df['bpm_diff'] = df['BPM'].diff().abs()
df = df[df['bpm_diff'] < 10]
df['BPM_interp'] = df['BPM'].interpolate()

df['time_bin_3s'] = (df['timestamp_sec'] // 3) * 3
df_grouped_3s = df.groupby(['time_bin_3s', 'task'])['BPM'].mean().reset_index()

tasks = sorted(df['task'].unique())
colors = sns.color_palette("tab10", len(tasks))
mean_by_task = df_grouped_3s.groupby('task')['BPM'].mean()
mean_global = df_grouped_3s['BPM'].mean()

plt.figure(figsize=(12, 5))
for task, color in zip(tasks, colors):
    sub = df_grouped_3s[df_grouped_3s['task'] == task]
    plt.plot(sub['time_bin_3s'], sub['BPM'], label=f"{task} ", color=color, alpha=0.5)
    if len(sub) > 5:
        smoothed = lowess(sub['BPM'], sub['time_bin_3s'], frac=0.3)
        plt.plot(smoothed[:, 0], smoothed[:, 1], linestyle='--', color=color, linewidth=2)
    y_mean = mean_by_task[task]
    plt.hlines(y_mean, sub['time_bin_3s'].min(), sub['time_bin_3s'].max(), colors=color, linestyles='dotted', alpha=0.6)
    plt.text(sub['time_bin_3s'].mean(), y_mean - 20, f"{y_mean:.1f} BPM", color=color,
             fontsize=9, ha='center', va='center', fontweight='bold')

plt.title(f"Évolution du BPM (moy. 3s) par tâche (moyenne globale : {mean_global:.1f} BPM)")
plt.xlabel("Temps (s)")
plt.ylabel("BPM")
plt.ylim(0, 150)
plt.grid(True)
plt.legend(title="Tâche")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "bpm_par_tache.png"))
plt.close()


# === SCRIPT HEATMAP.PY ===
csv_filename = fichier
resolution = (1920, 1080)
task_names = ["task_1", "task_2", "task_3", "task_4"]
heatmaps_by_task = {task: np.zeros(resolution[::-1]) for task in task_names}

with open(csv_filename, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            task = row["task"]
            if task in task_names:
                left_x = float(row['left_x'])
                left_y = float(row['left_y'])
                right_x = float(row['right_x'])
                right_y = float(row['right_y'])

                x = (left_x + right_x) / 2
                y = (left_y + right_y) / 2

                # Conversion en pixels
                px = int(x * resolution[0])
                py = int(y * resolution[1])

                # Clamp pour rester dans les limites de l'image
                px = min(max(px, 0), resolution[0] - 1)
                py = min(max(py, 0), resolution[1] - 1)

                # Inversion verticale et ajout dans la heatmap
                heatmaps_by_task[task][(resolution[1] - 1) - py, px] += 1

        except (ValueError, KeyError):
            continue


fig, axes = plt.subplots(2, 2, figsize=(12, 10))
for i, task in enumerate(task_names):
    row = i // 2
    col = i % 2
    blurred = gaussian_filter(heatmaps_by_task[task], sigma=50)
    axes[row, col].imshow(blurred, cmap='jet', interpolation='bilinear')
    axes[row, col].axis('off')
    axes[row, col].set_title(task.replace("_", " ").title())

plt.suptitle("Heatmaps segmentées par tâche", fontsize=16)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "heatmaps_yeux_par_tache.png"))
plt.close()


# === SCRIPT EMOTIONHEAT.PY ===
df = pd.read_csv(fichier)
df = df[df['task'].isin(task_names)]
df = df.dropna(subset=["dominant_emotion", "timestamp_sec"])

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
axes = axes.flatten()

for i, task in enumerate(task_names):
    df_task = df[df["task"] == task].copy()
    df_task["time_bin"] = (df_task["timestamp_sec"] // 3) * 3
    heatmap_data = df_task.groupby(["time_bin", "dominant_emotion"]).size().unstack(fill_value=0)

    if heatmap_data.empty:
        axes[i].axis('off')
        axes[i].set_title(f"Aucune donnée – {task.replace('_', ' ').title()}")
        continue

    # Générer la heatmap
    sns.heatmap(heatmap_data.T, cmap="YlOrRd", cbar_kws={'label': 'Occurrences'}, ax=axes[i], linewidths=.5)
    axes[i].set_title(f"Carte thermique des émotions – {task.replace('_', ' ').title()}")
    axes[i].set_xlabel("Temps (s)")
    axes[i].set_ylabel("Émotions")

    # Calcul des pourcentages des émotions
    emotion_counts = df_task["dominant_emotion"].value_counts(normalize=True) * 100
    emotion_summary = ", ".join([f"{emo}: {pct:.1f}%" for emo, pct in emotion_counts.items()])
    
    axes[i].text(0.5, 1.08, f"Répartition : {emotion_summary}", transform=axes[i].transAxes,
                 ha='center', fontsize=9, color='black')

plt.suptitle("Évolution des émotions par tâche – Heatmaps (fenêtres de 3s)", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(output_dir, "heatmaps_emotions_par_tache.png"))
plt.close()
