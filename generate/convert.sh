#!/bin/bash

# Find all .jpg files in the current directory and its subdirectories
find . -type f -name '*.jpg' | while read -r file; do
    # Get the directory and filename without the extension
    dir=$(dirname "$file")
    filename=$(basename "$file" .jpg)

    # Define the output .webp file
    output="${dir}/${filename}.webp"

    # Convert the .jpg file to .webp using cwebp
    cwebp "$file" -o "$output" -resize 1000 1000

    # Check if the conversion was successful
    if [ $? -eq 0 ]; then
        echo "Converted: $file -> $output"
        rm $file
    else
        echo "Failed to convert: $file"
    fi
done
