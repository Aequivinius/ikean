#!/bin/bash

# Check for required argument
if [ -z "$1" ]; then
  echo "Usage: $0 <input_directory> [output_directory]"
  exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="${2:-$INPUT_DIR/output}"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Check if ImageMagick's convert is installed
if ! command -v convert &> /dev/null; then
  echo "Error: 'convert' command not found. Install ImageMagick first (brew install imagemagick)."
  exit 1
fi

# Convert .webp to .jpg
for file in "$INPUT_DIR"/*.webp; do
  [ -e "$file" ] || continue  # Skip if no .webp files
  filename=$(basename "$file" .webp)
  magick "$file" "$OUTPUT_DIR/$filename.jpg"
  echo "Converted: $file -> $OUTPUT_DIR/$filename.jpg"
done
