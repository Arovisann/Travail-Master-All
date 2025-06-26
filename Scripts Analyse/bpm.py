import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.nonparametric.smoothers_lowess import lowess

# === Chargement des données ===
fichier = r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 1\2\2\fusion_emotions_bpm_taches2.csv"  # Remplace par ton chemin
df = pd.read_csv(fichier)

# === Nettoyage des données ===
df = df[df['task'] != 'outside_range'].copy()
df = df[df['BPM'].between(50, 100)]
df['bpm_diff'] = df['BPM'].diff().abs()
df = df[df['bpm_diff'] < 10]
df['BPM_interp'] = df['BPM'].interpolate()

# === Rééchantillonnage toutes les 3 secondes ===
df['time_bin_3s'] = (df['timestamp_sec'] // 3) * 3
df_grouped_3s = df.groupby(['time_bin_3s', 'task'])['BPM'].mean().reset_index()

# === Couleurs & statistiques ===
tasks = sorted(df['task'].unique())
colors = sns.color_palette("tab10", len(tasks))
mean_by_task = df_grouped_3s.groupby('task')['BPM'].mean()
mean_global = df_grouped_3s['BPM'].mean()

# === Plot final ===
plt.figure(figsize=(12, 5))

for task, color in zip(tasks, colors):
    sub = df_grouped_3s[df_grouped_3s['task'] == task]
    plt.plot(sub['time_bin_3s'], sub['BPM'], label=f"{task} ", color=color, alpha=0.5)

    # Courbe LOWESS
    if len(sub) > 5:
        smoothed = lowess(sub['BPM'], sub['time_bin_3s'], frac=0.3)
        plt.plot(smoothed[:, 0], smoothed[:, 1], linestyle='--', color=color, linewidth=2)

    # Ligne de moyenne par tâche
    y_mean = mean_by_task[task]
    plt.hlines(y_mean, sub['time_bin_3s'].min(), sub['time_bin_3s'].max(), colors=color, linestyles='dotted', alpha=0.6)

    # Affichage du texte encore plus bas
    plt.text(sub['time_bin_3s'].mean(), y_mean - 20, f"{y_mean:.1f} BPM", color=color,
             fontsize=9, ha='center', va='center', fontweight='bold')

# === Mise en page ===
plt.title(f"Évolution du BPM (moy. 3s) par tâche (moyenne globale : {mean_global:.1f} BPM)")
plt.xlabel("Temps (s)")
plt.ylabel("BPM")
plt.ylim(0, 150)
plt.grid(True)
plt.legend(title="Tâche")
plt.tight_layout()
plt.show()
