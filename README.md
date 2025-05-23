# Astro Annotator

**Astro Annotator** is a Docker-based tool that automatically performs plate solving, overlays constellation outlines and grid labels, and outputs labeled images. It is particularly useful for astrophotographers who want to annotate their images with minimal setup.

---

## 🚀 Features

- Automatic plate solving using [astrometry.net](http://astrometry.net/)
- Constellation outlines, NGC objects, and bright stars
- Equatorial coordinate grid with customizable spacing and colors
- Easy-to-use Docker container
- Automatic index file selection based on your camera and telescope settings

---

## 📦 Requirements

- Docker installed on your system
- Input images must be **already stretched** (JPG or PNG)
- Index file recommendations are based on your configuration in `config/astroplate.env`

---

## ⚙️ Configuration

Edit the file:

```
config/astroplate.env
```

Specify your imaging setup:

```env
SENSOR_WIDTH_PX=4272
SENSOR_HEIGHT_PX=2848
PIXEL_SIZE_UM=5.2
FOCAL_LENGTH_MM=650
```

These values are used to determine the optimal astrometry index files.
If you change this file, you **must rebuild the Docker image** using the instructions below.

---

## 🔨 Building the Docker Image

To build the Docker image, run:


### for Linux
```bash
./build.sh
```

or

### for Windows
```cmd
./build.sh
```

This will:
- Create necessary folders (`_originals`, `_annotated_solutions`)
- Calculate the recommended astrometry index files
- Install all dependencies
- Prepare the environment

---

## 🖼️ Annotating Images

Place your **stretched images** (JPG or PNG) in the `_originals/` folder.

Then run:
### for Linux
```bash
./run.sh
```
or

### for Windows
```cmd
./run.bat
```

This will:
- Process all images in `_originals/`
- Perform plate solving
- Annotate with constellation overlays
- Add an equatorial grid with labels
- Save the result to `_annotated_solutions/`

A log file is saved as `_annotated_solutions/processing.log`.

---

## 🧪 Optional Customization

You can customize the grid display by editing:

```
config/grid_config.env
```

Examples:

```env
GRID_SPACING_DEG=1.0
GRID_COLOR=gray
LABEL_COLOR=white
```

If left empty, values will be chosen automatically.

---

## 📂 Folder Structure

```
.
├── _originals/               # Place your stretched input images here
├── _annotated_solutions/     # Output will be saved here
├── config/
│   ├── astroplate.env        # Imaging system settings
│   └── grid_config.env       # Grid display configuration
├── requirements/
│   ├── apt-requirements.txt
│   └── python-requirements.txt
├── scripts/
│   ├── annotate_constellations.sh
│   ├── add_grid_labels.py
│   └── index_file_helper.py
├── docker/
│   └── Dockerfile
├── build.sh
├── build.bat
├── run.sh
├── run.bat
└── README.md
```

---

## 🤝 License

MIT – free to use and modify. Attribution appreciated.