#!/usr/bin/env python3
import sys
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from astropy import units as u

if len(sys.argv) != 4:
    print("Usage: add_grid_labels.py <wcs.fits> <input_image> <output_image>")
    sys.exit(1)

wcs_file = sys.argv[1]
input_img = sys.argv[2]
output_img = sys.argv[3]

# WCS laden
hdul = fits.open(wcs_file)
wcs = WCS(hdul[0].header)

# RGB-Bild laden und SPIEGELN (oben↔unten)
img = Image.open(input_img).convert("RGB")
img_data = np.asarray(img)[::-1, :, :]  # vertikal flippen

# WCS-Anzeige mit Achsenbeschriftung
fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(projection=wcs)
ax.imshow(img_data, origin='lower')

# Achsentitel und Ticklabels
ax.coords[0].set_axislabel('RA', fontsize=10, color='white')
ax.coords[1].set_axislabel('DEC', fontsize=10, color='white')
ax.coords[0].set_ticklabel(color='white', size=8)
ax.coords[1].set_ticklabel(color='white', size=8)

# Position der Beschriftung innerhalb des Bildes
ax.coords[0].set_ticks(spacing=0.25 * u.deg)
ax.coords[1].set_ticks(spacing=0.25 * u.deg)
ax.coords[0].set_ticklabel_position('t')
ax.coords[1].set_ticklabel_position('r')

# Gitter
ax.grid(color='white', ls='dotted', lw=0.5)

# Kein äußerer Rand
fig.patch.set_facecolor("black")
plt.savefig(output_img, dpi=150, facecolor='black', bbox_inches='tight', pad_inches=0.1) # kein bbox-cut!
plt.close(fig)

print(f"✅ Gitter mit Beschriftung gespeichert: {output_img}")
