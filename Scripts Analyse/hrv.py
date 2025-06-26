# Import packages
from pyhrv.hrv import hrv
from opensignalsreader import OpenSignalsReader
from biosppy.signals.ecg import ecg
import os
from pyhrv.tools import hrv_export

# Chemin du fichier
fpath = r"C:\Users\alexa\OneDrive\Bureau\Résultat Test Master\Interface 3\27\27\opensignals_201806130253_2025-06-01_19-30-02.txt"

# Charger
acq = OpenSignalsReader(fpath)
signal = acq.signal('ECG')

# Fréquence réelle
FS = 1000
print(f"Sampling rate utilisé pour ECG: {FS} Hz")
print(f"Nombre d'échantillons ECG: {len(signal)}")
print(f"Durée effective du signal: {len(signal)/FS:.1f} s")

# Détection R-peaks avec BioSPPy en précisant sampling_rate=1000
out = ecg(signal, sampling_rate=FS, show=False)
times = out[0]
filtered_signal = out[1]
rpeaks = out[2]
print(f"Durée perçue par BioSPPy: {times[-1]:.1f} s")


# Calcul HRV sur 1023 s
results = hrv(rpeaks=rpeaks, sampling_rate=FS, show=False)



# Export
output_dir = os.path.dirname(fpath)
os.makedirs(output_dir, exist_ok=True)
filename = "MyFirstHRVExport"
hrv_export(results, path=output_dir, efile=filename, comment="Analyse HRV", plots=True)
print(f"Export HRV généré dans {output_dir}")
