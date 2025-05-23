# 🪐 Astroplate Annotator
📘 README: [English](README.md) | [Deutsch](README.de.md)

A lightweight Bash and Python tool for automatic **platesolving** and **annotation of astrophotography images** – including grids, object marking, and axis labeling.

Ideal for DSLR images with solve-field + WCS coordinates (e.g., from Siril, KStars/Ekos, or ASTAP).

---

## ✨ Features

- Automatic **platesolving** using Astrometry.net
- Annotation of constellations & DeepSky objects (via `plot-constellations`)
- Precise RA/DEC grid overlay based on WCS
- Configurable grid spacing & colors via `.env`
- Compatible with PNG and JPG input images

---

## 🧰 Requirements

This tool uses the following (all installable via APT on Debian/Ubuntu):

```bash
sudo apt install astrometry.net nova netpbm file python3-pip
pip3 install matplotlib pillow numpy astropy python-dotenv
```

---

## 🚀 Usage

```bash
./annotate_constellations.sh <image.jpg|image.png>
```

Example:

```bash
./annotate_constellations.sh irisnebula.jpg
```

This will create:

```bash
annotated_irisnebula.png
labeled_annotated_irisnebula.png
```

---

## ⚙️ Configuration

Create (or copy) a file called `.env` or `grid_config.env` in the root directory:

```dotenv
# Grid spacing in degrees (leave empty for automatic calculation)
GRID_SPACING_DEG=0.5

# Colors for grid and labels:
#   Supported: "white", "black", "#ffcc00", "0.7" (grayscale)
GRID_COLOR=white
LABEL_COLOR=white
```

> 🔍 Colors follow [Matplotlib color syntax](https://matplotlib.org/stable/users/explain/colors/colors.html)

---

## 🗂 Project Structure

```bash
├── annotate_constellations.sh    # Bash script: Platesolve + annotate
├── add_grid_labels.py            # Python script: overlay labeled RA/DEC grid
├── grid_config.env               # (optional) configuration file
└── requirements.txt              # list of required CLI tools
```

---

## 📷 Example Workflow

1. You have a processed DeepSky image (`m42.jpg`)
2. Run:
   `./annotate_constellations.sh m42.jpg`
3. The tool performs:
   - solve-field (plate solving)
   - object annotation (NGC/IC/Messier)
   - grid overlay with proper RA/DEC orientation

4. You get:
   ✅ `annotated_m42.png`
   ✅ `labeled_annotated_m42.png`

---

## 🔒 License

MIT License – free to use and modify.

---

## 🙌 Credits

Uses:
- [astrometry.net](http://astrometry.net)
- [plot-constellations (nova)](https://github.com/astrometry/nova)
- [matplotlib](https://matplotlib.org)
- [Astropy](https://www.astropy.org)

---

## 📬 Feedback & Pull Requests welcome!
