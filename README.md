# AudioChunk
WARNING: This project is highly experimental and unpolished at this point.  

AudioChunk is for when you don't have time to cut audio samples after samples... It is batch processing bash and python scripts to automate sample cutting and editing using sonic-annotator and sox. I use these scripts to cut up samples, apply fade in/out, and apply normalization to each cut up audio sample. Often times, it requires me to listen through each sample after processing to see if the scripts are actually cutting up sounds at interesting and right places.  

This probably isn't the best approach but Vamp-plugins I have used for this experiment so far are: qm-segmenter, aubio-onsets, and bbc-speechmusic-segmenter. Audio segmentation method really is case by case depending on the sound content at this point.  

## Prerequisite

[sonic-annotator](http://vamp-plugins.org/sonic-annotator/)  
[sox](http://sox.sourceforge.net/)  
[pandas](http://pandas.pydata.org/)

## Run
The main script assumes that you are executing it from the same directory:

    sh AudioChunk.sh /Path/to/Samples/ minDuration maxDuration

## License
MIT
