import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
INPUT_CSV = BASE_DIR / "equiposChampions.csv"
OUTPUT_CSV = BASE_DIR / "tabla_posiciones.csv"
OUTPUT_PNG = BASE_DIR / "grafica_puntos_champions.png"

equipos = []
datos_numericos = []

with open(INPUT_CSV, mode="r", encoding="utf-8-sig") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        nombre_equipo = fila["equipo"].strip()
        if not nombre_equipo:
            continue
        equipos.append(nombre_equipo)
        datos_numericos.append([
            int(fila["ganados"]),
            int(fila["empatados"]),
            int(fila["perdidos"]),
            int(fila["goles_favor"]),
            int(fila["goles_contra"]),
        ])


stats = np.array(datos_numericos, dtype=np.int64)

ganados = stats[:, 0]
empatados = stats[:, 1]
perdidos = stats[:, 2]
goles_favor = stats[:, 3]
goles_contra = stats[:, 4]


puntos = ganados * 3 + empatados * 1 + perdidos * 0


diferencia_goles = goles_favor - goles_contra


with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as archivo_salida:
    escritor = csv.writer(archivo_salida)
    escritor.writerow(["equipo", "puntos", "diferencia_goles"])
    for equipo, pts, dg in zip(equipos, puntos, diferencia_goles):
        escritor.writerow([equipo, int(pts), int(dg)])


plt.figure(figsize=(13, 6))
plt.bar(equipos, puntos, color="#1f77b4")
plt.title("Puntos por equipo - Champions League")
plt.xlabel("Equipo")
plt.ylabel("Puntos")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT_PNG, dpi=300)
plt.close()

print("Proceso completado.")
print(f"Generado: {OUTPUT_CSV.name}")
print(f"Generado: {OUTPUT_PNG.name}")