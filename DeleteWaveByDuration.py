#! /usr/bin/python
import os, sys, wave, struct, pandas
from contextlib import closing

usage = """
Deletes audio files based on their durations
Usage:
    python SplitWave.py /path/to/wav/ minDur maxDur

Example:
    python SplitWave.py ~/Desktop/example/ 1 10
"""
#Recursively get file name
def getFileNames(path,fileExt):
	dirList = os.listdir(path)
	fileList = []
	for file in dirList:
		(filePath, fileName) = os.path.split(file)
		(title, extension) = os.path.splitext(fileName)
		fullPathFile = os.path.join(path,file)
		if extension in fileExt:
			if os.path.isfile(fullPathFile):
				fileList.append(fullPathFile)
		elif not os.path.isfile(fullPathFile):
			fileList.extend(getFileNames(fullPathFile,fileExt))

	return fileList

def main(path,minDur,maxDur):
	waveFiles = getFileNames(path,[".wav", ".WAV"])
	
	for waveFile in waveFiles:
		check(waveFile,minDur,maxDur)

	sys.exit()

def check(waveFile,minDur,maxDur):
    duration = 0

    with closing(wave.open(waveFile,'r')) as file:
		duration=file.getnframes()/float(file.getframerate())

    if duration < minDur or duration > maxDur:
        os.remove(waveFile)

if __name__ == '__main__':
  try:
    path = sys.argv[1]
    minDur = float(sys.argv[2])
    maxDur = float(sys.argv[3])
  except:
    print usage
    sys.exit(-1)
  main(path,minDur,maxDur)
