import cv2
import pandas as pd
from deepface import DeepFace
import time
from datetime import datetime

# Paramètres
intervalle_sauvegarde = 1  # En secondes
fichier_csv = "emotions_log.csv"

# Initialisation
cap = cv2.VideoCapture(0)
derniere_sauvegarde = time.time()
data_emotions = []

print("Appuie sur 'q' pour quitter")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # Analyse de l’émotion
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotions = result[0]['emotion']
        dominant_emotion = result[0]['dominant_emotion']

        # Affichage sur la vidéo
        cv2.putText(frame, f"Émotion : {dominant_emotion}", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Sauvegarde à intervalle régulier
        current_time = time.time()
        if current_time - derniere_sauvegarde >= intervalle_sauvegarde:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            emotions['timestamp'] = timestamp
            emotions['dominant_emotion'] = dominant_emotion
            data_emotions.append(emotions)
            derniere_sauvegarde = current_time

    except Exception as e:
        print(f"Erreur : {e}")

    # Affichage de la frame
    cv2.imshow('Détection des émotions', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Sauvegarde finale dans un CSV
df = pd.DataFrame(data_emotions)
df.to_csv(fichier_csv, index=False)
print(f"Émotions enregistrées dans {fichier_csv}")

cap.release()
cv2.destroyAllWindows()
