#!/bin/bash

# 📦 Sicherstellen, dass notwendige Tools vorhanden sind
REQUIREMENTS_FILE="requirements.txt"
MISSING=()
while read -r TOOL; do
  [[ -z "$TOOL" || "$TOOL" == \#* ]] && continue
  if ! command -v "$TOOL" &> /dev/null; then
    MISSING+=("$TOOL")
  fi
done < "$REQUIREMENTS_FILE"

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
  echo "Usage: ./annotate_constellations.sh <Eingabe-Bild>"
  echo ""
  echo "Das Eingabebild muss gestretcht (PNG/JPG) und WCS-kompatibel sein."
  echo ""
  echo "Beispiel: ./annotate_constellations.sh ng_stretched.jpg"
  if [ "${#MISSING[@]}" -gt 0 ]; then
    echo "❗ Fehlende Tools:"
    for TOOL in "${MISSING[@]}"; do echo "  - $TOOL"; done
    echo ""
    echo "Installiere unter Debian z. B. mit:"
    echo "  sudo apt install astrometry.net nova netpbm file"
  else
    echo "✅ Alle erforderlichen Tools vorhanden."
  fi
  exit 0
fi

if [ "${#MISSING[@]}" -gt 0 ]; then
  echo "❌ Fehlende Tools erkannt:"
  for TOOL in "${MISSING[@]}"; do echo "  - $TOOL"; done
  echo "Bitte installieren mit: sudo apt install astrometry.net nova netpbm file"
  exit 1
fi

INPUT_IMAGE="$1"
INPUT_BASE=$(basename "$INPUT_IMAGE")
INPUT_NAME="${INPUT_BASE%.*}"
SOLVE_DIR="solver"
mkdir -p "$SOLVE_DIR"

# 🔭 Plate-Solving (auf gestretchtem Bild)
echo "🔍 Starte Plate-Solving mit Astrometry.net..."
solve-field --downsample 2 --depth 30 "$INPUT_IMAGE" -D "$SOLVE_DIR"

WCS_FILE="$SOLVE_DIR/${INPUT_NAME}.wcs"
if [ ! -f "$WCS_FILE" ]; then
  echo "❌ Fehler: WCS-Datei wurde nicht erzeugt."
  exit 1
fi

# 🌌 plot-constellations annotiert das gestretchte Bild
ANNOTATED_PNG="annotated_${INPUT_NAME}.png"
MIME_TYPE=$(file --brief --mime-type "$INPUT_IMAGE")
case "$MIME_TYPE" in
  image/png) CONVERTER="pngtopnm" ;;
  image/jpeg) CONVERTER="jpegtopnm" ;;
  *) echo "❌ Nicht unterstütztes Format: $MIME_TYPE"; exit 1 ;;
esac

echo "🧠 Annotiere mit plot-constellations..."
"$CONVERTER" "$INPUT_IMAGE" | plot-constellations -w "$WCS_FILE" -o "$ANNOTATED_PNG" -i - -N -C -B -OR -VT -f 50

# ➕ Grid per Python hinzufügen
FINAL_OUT="labeled_$ANNOTATED_PNG"
echo "📐 Füge Gitter hinzu..."
python3 add_grid_labels.py "$SOLVE_DIR/${INPUT_NAME}.new" "$ANNOTATED_PNG" "$FINAL_OUT"

# 🧹 Aufräumen
rm -rf "$SOLVE_DIR"
echo "✅ Fertig! Annotiertes Bild gespeichert als: $FINAL_OUT"
