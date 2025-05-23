from dotenv import dotenv_values
import math
import os

# Load configuration from .env file
env = dotenv_values("config/astroplate.env")

sensor_width = int(env["SENSOR_WIDTH_PX"])
sensor_height = int(env["SENSOR_HEIGHT_PX"])
pixel_size = float(env["PIXEL_SIZE_UM"])
focal_length = float(env["FOCAL_LENGTH_MM"])

# Calculate field of view (in degrees)
def fov(pixels, pixel_size_um, focal_length_mm):
    return (pixels * pixel_size_um) / (focal_length_mm * 1000) * 57.3

fov_x = fov(sensor_width, pixel_size, focal_length)
fov_y = fov(sensor_height, pixel_size, focal_length)
fov_diag = math.sqrt(fov_x ** 2 + fov_y ** 2)

print(f"# [DEBUG] FOV X: {fov_x:.2f}°, FOV Y: {fov_y:.2f}°, Diagonal: {fov_diag:.2f}°")

# Index catalog with typical FOV ranges (degrees)
index_catalog = [
    ("index-4202", "astrometry-data-2mass-02", None, 0.1),
    ("index-4203", "astrometry-data-2mass-03", None, 0.2),
    ("index-4204", "astrometry-data-2mass-04", None, 0.35),
    ("index-4205", "astrometry-data-2mass-05", None, 0.5),
    ("index-4206", "astrometry-data-2mass-06", "astrometry-data-tycho2-06", 0.9),
    ("index-4207", "astrometry-data-2mass-07", "astrometry-data-tycho2-07", 1.4),
    ("index-4208", "astrometry-data-2mass-08-19", "astrometry-data-tycho2-08", 2.4),
    ("index-4209", "astrometry-data-2mass-08-19", "astrometry-data-tycho2-09", 4.0),
    ("index-4210", "astrometry-data-2mass-08-19", "astrometry-data-tycho2-10-19", 5.6),
]

# Find overlapping entries for the diagonal FOV
recommended = []
for i, (code, pkg2mass, pkgtycho, fov_limit) in enumerate(index_catalog):
    if 0.75 * fov_limit <= fov_diag <= 1.5 * fov_limit:
        recommended.extend(index_catalog[max(i-1, 0):min(i+2, len(index_catalog))])
        break

# Output
print("\n# Recommended APT packages:")
apt_packages = set()
for _, pkg2mass, pkgtycho, _ in recommended:
    if pkg2mass:
        apt_packages.add(pkg2mass)
    if pkgtycho:
        apt_packages.add(pkgtycho)
    print(f"  {pkg2mass or ''} {pkgtycho or ''}")

# Optional: export for shell
tychos = " ".join(r[2] for r in recommended if r[2])
masses = " ".join(r[1] for r in recommended if r[1])
print(f"\nTYCHO_INDEXES=\"{tychos}\"")
print(f"MASS_INDEXES=\"{masses}\"")

# As a single list for apt install
print("\nAPT_INDEX_PACKAGES=\"{}\"".format(" ".join(sorted(apt_packages))))