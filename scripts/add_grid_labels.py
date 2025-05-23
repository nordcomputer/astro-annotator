#!/usr/bin/env python3
import sys
import numpy as np
from PIL import Image
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
from astropy import units as u
from dotenv import dotenv_values

# 🔧 Load .env (for optional manual grid spacing)
grid_config = dotenv_values("config/grid_config.env")
manual_spacing = grid_config.get("GRID_SPACING_DEG")
grid_color = grid_config.get("GRID_COLOR", "white") or "white"
label_color = grid_config.get("LABEL_COLOR", "white") or "white"

# 📥 Validate arguments
if len(sys.argv) != 4:
    print("Usage: add_grid_labels.py <wcs.fits> <input_image> <output_image>")
    sys.exit(1)

wcs_file = sys.argv[1]
input_img = sys.argv[2]
output_img = sys.argv[3]

# 🗺️ Load WCS
hdul = fits.open(wcs_file)
wcs = WCS(hdul[0].header)

# 📸 Load RGB image and vertically flip
img = Image.open(input_img).convert("RGB")
img_data = np.asarray(img)[::-1, :, :]  # flip vertically for WCS alignment

# 📐 Calculate FOV
nx, ny = img_data.shape[1], img_data.shape[0]
pixel_scale = wcs.proj_plane_pixel_scales() * u.deg
fov_ra = (nx * pixel_scale[0]).to(u.deg).value
fov_dec = (ny * pixel_scale[1]).to(u.deg).value

# 📏 Determine grid spacing
if manual_spacing:
    try:
        step_ra = step_dec = float(manual_spacing)
    except ValueError:
        print("❌ Error: GRID_SPACING_DEG is not a valid number.")
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

# 🖼️ Plot image and overlay grid
fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(projection=wcs)
ax.imshow(img_data, origin='lower')

# 🧭 Axis labels and tick labels
ax.coords[0].set_axislabel('RA', fontsize=10, color=label_color)
ax.coords[1].set_axislabel('DEC', fontsize=10, color=label_color)
ax.coords[0].set_ticklabel(color=label_color, size=8)
ax.coords[1].set_ticklabel(color=label_color, size=8)

ax.coords[0].set_ticklabel_position('t')  # top
ax.coords[1].set_ticklabel_position('r')  # right

# 🌐 Apply grid
ax.coords[0].set_ticks(spacing=step_ra * u.deg)
ax.coords[1].set_ticks(spacing=step_dec * u.deg)
ax.grid(color=grid_color, ls='dotted', lw=0.5)

# 🖤 Black background, no excessive borders
fig.patch.set_facecolor("black")
plt.savefig(output_img, dpi=150, facecolor='black', bbox_inches='tight', pad_inches=0.1)
plt.close(fig)

print(f"✅ Grid with labels saved: {output_img}")
