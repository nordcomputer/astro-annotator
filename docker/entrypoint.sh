#!/bin/bash
source /venv/bin/activate
# Wenn das erste Argument wie eine Bilddatei aussieht, führe annotate aus
if [[ "$1" =~ \.(jpg|jpeg|png|fits)$ ]]; then
  exec ./scripts/annotate_constellations.sh "$@"
else
  exec "$@"
fi
