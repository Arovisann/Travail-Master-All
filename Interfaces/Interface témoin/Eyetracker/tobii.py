import tobii_research as tr
import csv
import time
import os

# Récupère le chemin du dossier courant (où est le script)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Nom du fichier CSV
filename = f"gaze_data_{int(time.time())}.csv"
filepath = os.path.join(script_dir, filename)

# Ouvre le fichier CSV
csv_file = open(filepath, mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["timestamp_sec", "left_x", "left_y", "right_x", "right_y"])

# Début du chrono
start_time = time.time()

# Trouver l'eye tracker
eyetracker = tr.find_all_eyetrackers()[0]
print(f"Eye tracker trouvé : {eyetracker.model} à {eyetracker.address}")
print(f"Les données seront enregistrées dans : {filepath}")

# Callback d'enregistrement
def gaze_data_callback(gaze_data):
    left = gaze_data['left_gaze_point_on_display_area']
    right = gaze_data['right_gaze_point_on_display_area']
    timestamp_sec = time.time() - start_time

    if left and right:
        csv_writer.writerow([
            f"{timestamp_sec:.3f}",  # timestamp arrondi à la milliseconde
            left[0], left[1],
            right[0], right[1]
        ])

# Lancer l'enregistrement
eyetracker.subscribe_to(
    tr.EYETRACKER_GAZE_DATA,
    gaze_data_callback,
    as_dictionary=True
)

print("Enregistrement en cours... (Ctrl+C pour arrêter)")
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Arrêt demandé.")

# Nettoyage
eyetracker.unsubscribe_from(
    tr.EYETRACKER_GAZE_DATA,
    gaze_data_callback
)
csv_file.close()
print(f"Fichier final enregistré : {filepath}")
