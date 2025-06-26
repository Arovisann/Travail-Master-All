import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import datetime
from scipy.signal import butter, filtfilt, find_peaks

# === PARAMÈTRES GÉNÉRAUX ===
FICHIER_ECG = r"C:\Users\alexa\Documents\OpenSignals (r)evolution\temp\opensignals_201806130253_2025-04-15_10-40-39.txt"
FS = 100  # fréquence d'échantillonnage en Hz

# === FONCTIONS UTILITAIRES ===

def load_ecg_file(path):
    """Charge le fichier ECG et retourne un DataFrame pandas"""
    with open(path, 'r') as file:
        lines = file.readlines()
    data_start = next(i for i, line in enumerate(lines) if 'EndOfHeader' in line) + 1
    data_str = ''.join(lines[data_start:])
    df = pd.read_csv(io.StringIO(data_str), sep=r'\s+', header=None)
    df.columns = ['nSeq', 'I1', 'I2', 'O1', 'O2', 'A2']
    return df

def butter_bandpass(lowcut, highcut, fs, order=4):
    """Crée un filtre passe-bande Butterworth"""
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def ajouter_temps(df, fs):
    """Ajoute une colonne de timestamp en secondes et en horodatage absolu"""
    timestamps = np.arange(len(df)) / fs
    df['Time (s)'] = timestamps

    # Timestamp absolu fictif (à adapter si tu as un vrai start time dans le header)
    start_time = datetime.datetime.now()
    df['Horodatage'] = [start_time + datetime.timedelta(seconds=t) for t in timestamps]
    return df

def analyser_ecg(signal, fs):
    """Filtre le signal, détecte les pics, et calcule la fréquence cardiaque"""
    b, a = butter_bandpass(1, 40, fs)
    filtered = filtfilt(b, a, signal)
    peaks, _ = find_peaks(filtered, distance=fs * 0.6, height=np.mean(filtered))
    rr_intervals = np.diff(peaks) / fs  # en secondes
    bpm = 60 / rr_intervals if len(rr_intervals) > 0 else []
    bpm_moy = np.mean(bpm) if len(bpm) > 0 else 0
    return filtered, peaks, bpm_moy

def creer_df_bpm(peaks, timestamps, fs):
    """Crée un DataFrame associant un timestamp à chaque valeur de BPM"""
    rr_intervals = np.diff(peaks) / fs  # secondes
    bpm = 60 / rr_intervals if len(rr_intervals) > 0 else []

    # Timestamps associés à chaque BPM (au 2ème pic)
    bpm_timestamps = timestamps[peaks[1:]]  # ignore le premier pic
    df_bpm = pd.DataFrame({
        'Timestamp (s)': bpm_timestamps,
        'BPM': bpm
    })
    return df_bpm


def afficher_resultats(timestamps, signal, peaks, bpm_moyenne):
    """Affiche le signal ECG avec les pics détectés"""
    plt.figure(figsize=(14, 5))
    plt.plot(timestamps, signal, label='ECG filtré')
    plt.plot(timestamps[peaks], signal[peaks], 'ro', label='Battements détectés')
    plt.title(f"Signal ECG filtré - Fréquence cardiaque moyenne : {bpm_moyenne:.1f} bpm")
    plt.xlabel('Temps (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# === MAIN ===

df = load_ecg_file(FICHIER_ECG)
df = ajouter_temps(df, FS)
ecg_raw = df['A2'].values

ecg_filtered, peaks, bpm_moyenne = analyser_ecg(ecg_raw, FS)
afficher_resultats(df['Time (s)'].values, ecg_filtered, peaks, bpm_moyenne)

df_bpm = creer_df_bpm(peaks, df['Time (s)'].values, FS)

# Export CSV
df_bpm.to_csv("bpm_par_timestamp.csv", index=False)
print("✅ Fichier 'bpm_par_timestamp.csv' généré avec succès.")

