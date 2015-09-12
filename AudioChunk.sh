#!/bin/bash

if [ -z "$1" ]
  then
  cat README.md
  exit 1;
fi

execDir=${PWD}
copyDir=$(basename "$1")
mkdir -p "$copyDir"

#Remove all previously processed files
echo "Removing previously processed files..."
rm -r "$copyDir"/*/ 2> /dev/null

#Copy audio files to keep the original untouched
echo "Copying files for analysis..."
find "$1" -type f -iname "*.wav" | while read line; do
  file=$(basename "$line")
  sox "$line" -e signed-integer "$copyDir"/"$file" 2>/dev/null
done

#Analysis templates
#save RDF and modify parameters according to your need
#sonic-annotator -s vamp:qm-vamp-plugins:qm-segmenter:segmentation > qm-segmenter.n3
#sonic-annotator -s vamp:segmentino:segmentino:segmentation > segmentino.n3
#sonic-annotator -s vamp:libvamp_essentia:MFCC_35:sbic > sbic.n3
#sonic-annotator -s vamp:bbc-vamp-plugins:bbc-speechmusic-segmenter:segmentation > bbcsegment.n3
#sonic-annotator -s vamp:bbc-vamp-plugins:bbc-speechmusic-segmenter:skewness > bbcskew.n3
#sonic-annotator -s vamp:vamp-aubio:aubioonset:odf > odf.n3
#sonic-annotator -s vamp:vamp-aubio:aubiosilence:silent > silent.n3

#TODO analyze should be done on flag basis for different kind of sound. e.g. music->onset, speech->bbc
echo "Analyzing audio files..."
sonic-annotator -t qm-segmenter.n3 -r "$copyDir" -w csv --csv-basedir "$copyDir" 2> /dev/null
#sonic-annotator -t sbic.n3 -r "$1" -w csv --csv-basedir "$1"

echo "Segementing audio files..."
python SplitWave.py "$copyDir"

echo "Deleting invalid audio files..."
python DeleteWaveByDuration.py "$copyDir" "$2" "$3"

# echo "Deleting analysis files..."
rm "$copyDir"/*.csv 2> /dev/null

#FadeInOut.sh take additional two arguments: fadeInTime and fadeOutPercent
echo "Applying fade in/out and normalize..."
sh FadeInOut.sh "$copyDir" 0.1 0.2

#Move all the sounds to processed
# mkdir -p "$2"/processed
# COUNTER=0
# find "$2" -type f -iname "*.wav" | while read line; do
# mv "$line" "$2"/processed/$COUNTER.wav
# let COUNTER=COUNTER+1
# done
#
# shopt -s extglob
# rm -rf "$2"/!(/processed)
# shopt -u extglob

echo "Done :)"

exit 0
