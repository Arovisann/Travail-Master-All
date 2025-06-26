import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# === Paramètres ===
csv_filename = r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 1\2\2\fusion_emotions_bpm_taches2.csv"  # Remplace par ton fichier exact
output_image = "heatmap.png"
resolution = (1920, 1080)  # Résolution de l'écran utilisé (à adapter)

# === Récupération des données ===
gaze_points = []

with open(csv_filename, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        try:
            # Moyenne des deux yeux
            left_x = float(row['left_x'])
            left_y = float(row['left_y'])
            right_x = float(row['right_x'])
            right_y = float(row['right_y'])

            x = (left_x + right_x) / 2
            y = (left_y + right_y) / 2

            # Convertir en coordonnées pixel
            px = int(x * resolution[0])
            py = int(y * resolution[1])

            # Y inversé car matplotlib place (0,0) en bas à gauche
            gaze_points.append((px, resolution[1] - py))

        except ValueError:
            continue  # Si des données sont manquantes

# === Création de la matrice de chaleur ===
heatmap = np.zeros(resolution[::-1])  # [height, width]

for x, y in gaze_points:
    if 0 <= x < resolution[0] and 0 <= y < resolution[1]:
        heatmap[y, x] += 1

# Appliquer un flou pour lisser la heatmap
heatmap = gaussian_filter(heatmap, sigma=50)

# === Affichage et sauvegarde ===
plt.imshow(heatmap, cmap='jet', interpolation='bilinear')
plt.axis('off')
plt.savefig(output_image, bbox_inches='tight', pad_inches=0)
plt.show()
