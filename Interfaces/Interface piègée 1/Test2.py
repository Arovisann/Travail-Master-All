import tobii_research as tr
import csv
import time
import os
import cv2
from deepface import DeepFace
from datetime import datetime
import threading

# Récupère le chemin du dossier courant (où est le script)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Nom du fichier CSV
filename = f"gaze_emotion_data_{int(time.time())}.csv"
filepath = os.path.join(script_dir, filename)

# Ouvre le fichier CSV
csv_file = open(filepath, mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["timestamp_sec", "left_x", "left_y", "right_x", "right_y", "dominant_emotion"])

# Début du chrono pour timestamp commun
start_time = time.time()

# Trouver l'eye tracker
eyetracker = tr.find_all_eyetrackers()[0]
print(f"Eye tracker trouvé : {eyetracker.model} à {eyetracker.address}")
print(f"Les données seront enregistrées dans : {filepath}")

# Variable partagée pour les émotions
emotion_data = {"dominant_emotion": ""}

# Fonction d'enregistrement des données du eye tracker
def gaze_data_callback(gaze_data):
    left = gaze_data['left_gaze_point_on_display_area']
    right = gaze_data['right_gaze_point_on_display_area']
    timestamp_sec = time.time() - start_time  # Calcul du timestamp commun

    # S'assurer que les coordonnées existent
    if left and right:
        # Ajouter l'émotion à la ligne des données de l'eye tracker
        csv_writer.writerow([
            f"{timestamp_sec:.3f}",  # timestamp arrondi à la milliseconde
            left[0], left[1],
            right[0], right[1],
            emotion_data["dominant_emotion"]  # Ajouter l'émotion dominante
        ])

# Fonction d'enregistrement des émotions
def emotion_data_callback():
    cap = cv2.VideoCapture(0)  # Initialisation de la caméra
    derniere_sauvegarde = time.time()

    print("Appuie sur 'q' pour quitter la détection des émotions")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            # Analyse de l’émotion
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotions = result[0]['emotion']
            dominant_emotion = result[0]['dominant_emotion']

            # Sauvegarde à intervalle régulier
            current_time = time.time()
            if current_time - derniere_sauvegarde >= 1:  # Sauvegarde toutes les secondes
                emotion_data["dominant_emotion"] = dominant_emotion  # Mise à jour de l'émotion dominante
                derniere_sauvegarde = current_time

        except Exception as e:
            print(f"Erreur lors de l'analyse de l'émotion : {e}")

        # Affichage de la frame
        #cv2.imshow('Détection des émotions', frame)

        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

    cap.release()
    cv2.destroyAllWindows()

# Fonction principale pour lancer les deux enregistrements en parallèle
def main():
    # Lancer l'enregistrement du eye tracker en parallèle
    eyetracker.subscribe_to(
        tr.EYETRACKER_GAZE_DATA,
        gaze_data_callback,
        as_dictionary=True
    )

    # Lancer la reconnaissance d'émotion en parallèle dans un thread
    emotion_thread = threading.Thread(target=emotion_data_callback)
    emotion_thread.start()

    try:
        print("Enregistrement en cours... (Ctrl+C pour arrêter)")
        while True:
            time.sleep(0.1)  # Ajout d'un petit délai pour ne pas surcharger le CPU
    except KeyboardInterrupt:
        print("Arrêt demandé.")

    # Nettoyage et fin du processus
    eyetracker.unsubscribe_from(
        tr.EYETRACKER_GAZE_DATA,
        gaze_data_callback
    )

    emotion_thread.join()  # Assurer que le thread des émotions se termine correctement
    csv_file.close()
    print(f"Fichier final enregistré : {filepath}")

# Lancer le script
if __name__ == "__main__":
    main()
