import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# === Paramètres ===
csv_filename = r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 1\2\2\fusion_emotions_bpm_taches2.csv"
resolution = (1920, 1080)  # Résolution de l'écran utilisé
task_names = ["task_1", "task_2", "task_3", "task_4"]

# === Initialiser les heatmaps par tâche ===
heatmaps_by_task = {task: np.zeros(resolution[::-1]) for task in task_names}

# === Lecture des données ===
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

                # Moyenne des yeux
                x = (left_x + right_x) / 2
                y = (left_y + right_y) / 2

                # Conversion en pixels
                px = int(x * resolution[0])
                py = int(y * resolution[1])

                if 0 <= px < resolution[0] and 0 <= py < resolution[1]:
                    # Inverser Y car matplotlib place (0,0) en bas à gauche
                    heatmaps_by_task[task][resolution[1] - py, px] += 1

        except (ValueError, KeyError):
            continue  # Ignore les lignes avec données manquantes ou invalides

# === Affichage ===
fig, axes = plt.subplots(1, 4, figsize=(20, 5))

for i, task in enumerate(task_names):
    blurred = gaussian_filter(heatmaps_by_task[task], sigma=50)
    axes[i].imshow(blurred, cmap='jet', interpolation='bilinear')
    axes[i].axis('off')
    axes[i].set_title(task.replace("_", " ").title())

plt.suptitle("Heatmaps segmentées par tâche", fontsize=16)
plt.tight_layout()
plt.show()
