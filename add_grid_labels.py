#!/usr/bin/env python3
import sys
import numpy as np
from PIL import Image
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
from astropy import units as u
from dotenv import dotenv_values

# 🔧 .env einlesen (für optionale manuelle Grid-Größe)
grid_config = dotenv_values("grid_config.env")
manual_spacing = grid_config.get("GRID_SPACING_DEG")
grid_color = grid_config.get("GRID_COLOR", "white") or "white"
label_color = grid_config.get("LABEL_COLOR", "white") or "white"

# 📥 Argumente prüfen
if len(sys.argv) != 4:
    print("Usage: add_grid_labels.py <wcs.fits> <input_image> <output_image>")
    sys.exit(1)

wcs_file = sys.argv[1]
input_img = sys.argv[2]
output_img = sys.argv[3]

# 🗺️ WCS laden
hdul = fits.open(wcs_file)
wcs = WCS(hdul[0].header)

# 📸 RGB-Bild laden (und vertikal spiegeln)
img = Image.open(input_img).convert("RGB")
img_data = np.asarray(img)[::-1, :, :]  # vertikal flippen für WCS-Koordinaten

# 📐 FOV berechnen
nx, ny = img_data.shape[1], img_data.shape[0]
pixel_scale = wcs.proj_plane_pixel_scales() * u.deg
fov_ra = (nx * pixel_scale[0]).to(u.deg).value
fov_dec = (ny * pixel_scale[1]).to(u.deg).value

# 📏 Gitterabstand festlegen
if manual_spacing:
    try:
        step_ra = step_dec = float(manual_spacing)
    except ValueError:
        print("❌ Fehler: GRID_SPACING_DEG ist keine gültige Zahl.")
        sys.exit(1)
else:
    def best_grid_step(fov):
        candidates = [0.05, 0.1, 0.2, 0.5, 1.0, 2.0]
        for c in candidates:
            if fov / c <= 8:
                return c
        return 5.0
    step_ra = best_grid_step(fov_ra)
    step_dec = best_grid_step(fov_dec)

# 🖼️ Bild + Gitter darstellen
fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(projection=wcs)
ax.imshow(img_data, origin='lower')

# 🧭 Achsenbeschriftung und Grid-Labels
ax.coords[0].set_axislabel('RA', fontsize=10, color=label_color)
ax.coords[1].set_axislabel('DEC', fontsize=10, color=label_color)
ax.coords[0].set_ticklabel(color=label_color, size=8)
ax.coords[1].set_ticklabel(color=label_color, size=8)

ax.coords[0].set_ticklabel_position('t')  # top
ax.coords[1].set_ticklabel_position('r')  # right

# 🌐 Grid anwenden
ax.coords[0].set_ticks(spacing=step_ra * u.deg)
ax.coords[1].set_ticks(spacing=step_dec * u.deg)
ax.grid(color=grid_color, ls='dotted', lw=0.5)

# 🖤 Schwarzer Hintergrund, keine übermäßigen Ränder
fig.patch.set_facecolor("black")
plt.savefig(output_img, dpi=150, facecolor='black', bbox_inches='tight', pad_inches=0.1)
plt.close(fig)

print(f"✅ Gitter mit Beschriftung gespeichert: {output_img}")
