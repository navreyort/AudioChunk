#!/bin/bash

FADE_IN=$2
FADE_OUT=$3

find "$1" -type f -iname "*.wav" | while read line; do
	file=$(basename "$line")
	dir=$(dirname "$line")
	mkdir -p "$dir"/fade/
	new="$dir"/fade/`echo "$file"`
	#echo "Applying fade in/out: $new"
	LENGTH=`sox "$line" 2>&1 -n stat | grep Length | cut -d : -f 2 | cut -f 1`
	fadeOutTime=$(echo "$FADE_OUT"*"$LENGTH" | bc)
	sox "$line" -e signed-integer --norm=-1 -G "$new" fade t "$FADE_IN" "$LENGTH" "$fadeOutTime";
	rm "$line"
done
