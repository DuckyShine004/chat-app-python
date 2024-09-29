#!/bin/bash

RESOURCE_DIR="../src/common/resources"
INPUT_DIR="../src/common/resources/ui"
OUTPUT_DIR="../src/client/ui"

if [ $# -lt 1 ]; then
    echo "Need at least one input"
    echo "Usage: $0 <input_file>"
    exit 1
fi

input_file="$1"
output_file="$2"

extension="${input_file##*.}"
filename="$(basename "$input_file" ."$extension")"

if [ "$extension" == "qrc" ]; then
    pyside6-rcc -o "$RESOURCE_DIR/${filename}_rc.py" "$RESOURCE_DIR/$input_file"
    echo "[INFO] Compiled $input_file to $RESOURCE_DIR/${filename}_rc.py"
else
    pyside6-uic "$INPUT_DIR/$input_file" -o "$OUTPUT_DIR/$output_file"
    echo "[INFO] Compiled $input_file to $OUTPUT_DIR/$output_file"
fi

# pyuic6 -x "$INPUT_DIR/$input_file" -o "$OUTPUT_DIR/$output_file"
# python3 -m PyQt6.uic.pyuic -x "$INPUT_DIR/$input_file" -o "$OUTPUT_DIR/$output_file"
