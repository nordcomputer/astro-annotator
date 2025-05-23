#!/bin/bash

REQUIREMENTS_FILE="requirements/requirements.txt"
ORIGINALS_DIR="_originals"
OUTPUT_DIR="_annotated_solutions"
LOGFILE="$OUTPUT_DIR/processing.log"

# 📦 Check required tools
MISSING=()
while read -r TOOL; do
  [[ -z "$TOOL" || "$TOOL" == \#* ]] && continue
  if ! command -v "$TOOL" &> /dev/null; then
    MISSING+=("$TOOL")
  fi
done < "$REQUIREMENTS_FILE"

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo "Usage: ./annotate_constellations.sh"
  echo ""
  echo "All images inside $ORIGINALS_DIR/ will be annotated."
  exit 0
fi

if [ "${#MISSING[@]}" -gt 0 ]; then
  echo "❌ Missing tools:"
  for TOOL in "${MISSING[@]}"; do echo "  - $TOOL"; done
  exit 1
fi

# 📂 Prepare folders
mkdir -p "$ORIGINALS_DIR" "$OUTPUT_DIR"
chmod 777 "$ORIGINALS_DIR" "$OUTPUT_DIR"

# 📂 Get list of images
shopt -s nullglob
FILES=("$ORIGINALS_DIR"/*.{jpg,jpeg,png})
if [ ${#FILES[@]} -eq 0 ]; then
  echo "⚠️  No input images found in $ORIGINALS_DIR/!"
  exit 1
fi

# 📝 Start log file
echo "🔧 Processing started: $(date)" > "$LOGFILE"

process_image() {
  INPUT_IMAGE="$1"
  echo "🔍 Processing: $INPUT_IMAGE" | tee -a "$LOGFILE"

  INPUT_BASE=$(basename "$INPUT_IMAGE")
  INPUT_NAME="${INPUT_BASE%.*}"
  SOLVE_DIR="solver_$INPUT_NAME"
  mkdir -p "$SOLVE_DIR"

  echo "🔭 Starting plate solving..." | tee -a "$LOGFILE"
  solve-field --downsample 2 --depth 30 "$INPUT_IMAGE" -D "$SOLVE_DIR"
  WCS_FILE="$SOLVE_DIR/${INPUT_NAME}.wcs"
  if [ ! -f "$WCS_FILE" ]; then
    echo "⚠️  No WCS file generated for $INPUT_IMAGE." | tee -a "$LOGFILE"
    return
  fi

  MIME_TYPE=$(file --brief --mime-type "$INPUT_IMAGE")
  case "$MIME_TYPE" in
    image/png) CONVERTER="pngtopnm" ;;
    image/jpeg) CONVERTER="jpegtopnm" ;;
    *) echo "❌ Unsupported format: $MIME_TYPE" | tee -a "$LOGFILE"; return ;;
  esac

  ANNOTATED_PNG="$OUTPUT_DIR/annotated_${INPUT_NAME}.png"
  "$CONVERTER" "$INPUT_IMAGE" | plot-constellations -w "$WCS_FILE" -o "$ANNOTATED_PNG" -i - -N -C -B -OR -VT -f 50

  FINAL_OUT="$OUTPUT_DIR/labeled_${INPUT_NAME}.png"
  echo "📐 Adding grid to $INPUT_IMAGE..." | tee -a "$LOGFILE"
  python3 scripts/add_grid_labels.py "$SOLVE_DIR/${INPUT_NAME}.new" "$ANNOTATED_PNG" "$FINAL_OUT"

  rm -rf "$SOLVE_DIR"
  echo "✅ Done: $FINAL_OUT" | tee -a "$LOGFILE"
}

for f in "${FILES[@]}"; do
  process_image "$f"
done
