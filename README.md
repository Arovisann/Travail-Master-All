# Analyse UX – Frustration et Réactions Physiologiques

Ce projet fait partie d’un travail de Master visant à étudier les éléments de design générant de la frustration, à travers des mesures subjectives (questionnaires) et objectives (données physiologiques, mouvements oculaires et expressions faciales).

## 📦 Contenu du projet

- Le dossier "Interface" contient les trois interfaces que les utilisateurs ont manipulé.
- Le dossier "Résultat Test Master" contient toutes les données des résultats des tests utilisateurs.
- `test.py` / `Test2.py` : Scripts de capture de données (gaze, émotions) avec DeepFace, Tobii et BITalino.
- `heatmap_generator.py` : Script de génération de heatmaps à partir des données de l'eyetracker.
- `fusion_emotions_bpm_taches.csv` : Fichier CSV fusionné des données gaze + émotion + BPM + tâches.
- `hrv_analysis.py` : Script d’analyse HRV avec `pyhrv`, `biosppy`, `opensignalsreader`.

## 🧪 Technologies utilisées

- **Python 3.x**
- [DeepFace](https://github.com/serengil/deepface) – Reconnaissance d’émotions via webcam
- [Tobii Pro SDK](https://developer.tobii.com/) – Récupération des données d’eye tracking
- [BITalino + OpenSignals](https://bitalino.com/en/software/) – Acquisition des signaux physiologiques
- [pyhrv](https://pyhrv.readthedocs.io/) – Analyse HRV (variabilité de la fréquence cardiaque)
- [biosppy](https://biosppy.readthedocs.io/) – Traitement du signal ECG
- [matplotlib / numpy / scipy / pandas] – Visualisation et traitement des données

## 🚀 Lancement des interfaces
Pour lancer les interfaces sous HTML. Lancer le fichier Reset.html afin d'initialiser l'interface pour utilisation. 

### 1. Capture des données
Lancer depuis une console "python Test2.py"
