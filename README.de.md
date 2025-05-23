
# 🪐 Astroplate Annotator
📘 README: [English](README.md) | [Deutsch](README.de.md)

Ein leichtgewichtiges Bash- und Python-Tool zur automatischen **Platesolving** und **Annotierung von Astrofotografie-Aufnahmen** – inklusive Gitter, Objektmarkierung und Achsenbeschriftung.

Ideal für DSLR-Aufnahmen mit solve-field + WCS-Koordinaten, z. B. aus Siril, KStars/Ekos oder ASTAP.

---

## ✨ Funktionen

- Automatisches **Platesolving** mit Astrometry.net
- Annotierung von Sternbildern & DeepSky-Objekten (über `plot-constellations`)
- Präzise Gitterbeschriftung (RA/DEC) per WCS-Auswertung
- Konfigurierbare Gitterabstände & Farben per `.env`
- Kompatibel mit PNG- oder JPG-Bildern

---

## 🧰 Abhängigkeiten

Das Projekt nutzt folgende Tools (alle per APT installierbar unter Debian/Ubuntu):

```bash
sudo apt install astrometry.net nova netpbm file python3-pip
pip3 install matplotlib pillow numpy astropy python-dotenv
```

---

## 🚀 Nutzung

```bash
./annotate_constellations.sh <bild.jpg|bild.png>
```

Beispiel:

```bash
./annotate_constellations.sh irisnebula.jpg
```

Ergebnis:
➡️ Ein Bild mit markierten Objekten + sauber beschriftetem Himmelsgitter unter dem Namen:

```bash
annotated_irisnebula.png
labeled_annotated_irisnebula.png
```

---

## ⚙️ Konfiguration

Erstelle (oder kopiere) eine Datei namens `.env` oder `grid_config.env` im Hauptverzeichnis:

```dotenv
# Gitterabstand in Grad (leer = automatisch)
GRID_SPACING_DEG=0.5

# Farben für Gitter und Beschriftung:
#   Erlaubt: "white", "black", "#ffcc00", "0.7" (Graustufe)
GRID_COLOR=white
LABEL_COLOR=white
```

> 🔍 Farbwerte sind kompatibel mit [Matplotlib-Farbdefinitionen](https://matplotlib.org/stable/users/explain/colors/colors.html).

---

## 🗂 Struktur

```bash
├── annotate_constellations.sh    # Bash-Workflow: Platesolve + Annotieren
├── add_grid_labels.py            # Fügt WCS-basiertes Gitter hinzu
├── grid_config.env               # (optional) Konfigurationsdatei
└── requirements.txt              # Liste der benötigten CLI-Tools
```

---

## 📷 Beispiel-Workflow

1. Du hast ein bearbeitetes DeepSky-Bild (`m42.jpg`)
2. Du führst aus:
   `./annotate_constellations.sh m42.jpg`
3. Das Tool führt durch:
   - solve-field (Platesolving)
   - Objektannotierung (NGC/IC/Messier)
   - Gitteroverlay mit richtiger RA/DEC-Ausrichtung

4. Du bekommst:
   ✅ `annotated_m42.png`
   ✅ `labeled_annotated_m42.png`

---

## 🔒 Lizenz

MIT License – frei verwendbar und anpassbar.

---

## 🙌 Credits

Verwendet:
- [astrometry.net](http://astrometry.net)
- [plot-constellations (nova)](https://github.com/astrometry/nova)
- [matplotlib](https://matplotlib.org)
- [Astropy](https://www.astropy.org)

---

## 📬 Feedback & Pull Requests willkommen!
