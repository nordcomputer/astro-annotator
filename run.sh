#!/bin/bash
docker run --rm -v "$PWD:/data" -w /data astro-annotator "$@"
