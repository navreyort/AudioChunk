#! /usr/bin/python
import os, sys, wave, struct, pandas
from contextlib import closing

usage = """
Segments wave file based on csv file provided
Usage:
    python SplitWave.py /path/to/csv

Example:
    python SplitWave.py ~/Desktop/example.csv
"""
#Recursively get file name
def getFileNames(path,fileExt):
	dirList = os.listdir(path)
	fileList = []
	for file in dirList:
		(filePath, fileName) = os.path.split(file)
		(title, extension) = os.path.splitext(fileName)
		if extension in fileExt:
			fullPathFile = os.path.join(path,file)
			if os.path.isfile(fullPathFile):
				fileList.append(fullPathFile)
			else:
				fileList.extend(getFileNames(fullPathFile))

	return fileList

def main(path):
	waveFiles = getFileNames(path,[".wav", ".WAV"])
	csvFiles = getFileNames(path,[".csv"])

	for waveFile in waveFiles:
		(filePath, fileName) = os.path.split(waveFile)
		(title, extension) = os.path.splitext(fileName)
		csvFile = [s for s in csvFiles if title in s]
		if len(csvFile) > 0:
			split(waveFile, csvFile[0])
		else:
			print('Cannot process:',waveFile)

	sys.exit()

def split(waveFile, csvFile):
	(filePath, fileName) = os.path.split(waveFile)
	(title, extension) = os.path.splitext(fileName)

	if not os.path.exists(filePath+'/'+title):
	    os.makedirs(filePath+'/'+title)
	    #os.makedirs(filePath+'/'+title+'/stereo')
	    #os.makedirs(filePath+'/'+title+'/mono')

	with closing(wave.open(waveFile,'r')) as file:

		frames = file.getnframes()
		rate = float(file.getframerate())
		duration=frames/rate

		df = pandas.read_csv(csvFile, index_col=False, header=None)
		durations = df[0]

		for i in range(durations.size):

			if i < 9:
				saveStereoName = filePath+'/'+title+"/0"+str(i+1)+extension
				#saveStereoName = filePath+'/'+title+"/stereo/0"+str(i+1)+extension
				#saveMonoName = filePath+'/'+title+"/mono/0"+str(i+1)+extension
			else:
				saveStereoName = filePath+'/'+title+"/"+str(i+1)+extension
				#saveStereoName = filePath+'/'+title+"/stereo/"+str(i+1)+extension
				#saveMonoName = filePath+'/'+title+"/mono/"+str(i+1)+extension

			#Save stereo file to keep originals
			with closing(wave.open(saveStereoName,'w')) as splitFile:
				#get duration to save in nframes
				if i+1 < durations.size:
					frameDur = int((durations[i+1]-durations[i])*rate)
				else:
					frameDur = int((duration - durations[i])*rate)

				#read data from original file
				file.setpos(int(durations[i]*rate))
				saveFrames = file.readframes(frameDur)

				#set parameters for a write file
				splitFile.setnchannels(file.getnchannels())
				splitFile.setsampwidth(file.getsampwidth())
				splitFile.setframerate(rate)
				splitFile.setcomptype(file.getcomptype(),file.getcompname())
				splitFile.setnframes(frameDur)

				#write
				splitFile.writeframes(saveFrames)

			#Save mono version for analysis
			#with closing(wave.open(saveMonoName,'w')) as splitFile:
			#get duration to save in nframes
			# splitFile = wave.open(saveMonoName,'w')
            #
			# if i+1 < durations.size:
			# 	frameDur = int((durations[i+1]-durations[i])*rate)
			# else:
			# 	frameDur = int((duration - durations[i])*rate)
            #
			# #read data from original file
			# file.setpos(int(durations[i]*rate))
			# saveFrames = file.readframes(frameDur)
            #
			# total_samples = frameDur * file.getnchannels()
            #
			# if file.getsampwidth() == 1:
			# 	fmt = "%iB" % total_samples # read unsigned chars
			# elif file.getsampwidth() == 2:
			# 	fmt = "%ih" % total_samples # read signed 2 byte shorts
			# else:
			# 	raise ValueError("Only supports 8 and 16 bit audio formats.")
            #
			# saveFrames = struct.unpack(fmt, saveFrames)
			# monoFrames = []
			# for j in xrange(0,len(saveFrames),2):
			# 	monoFrames.append((saveFrames[j]+saveFrames[j+1])/2)
            #
			# if file.getsampwidth() == 1:
			# 	fmt = "%iB" % frameDur # read unsigned chars
			# elif file.getsampwidth() == 2:
			# 	fmt = "%ih" % frameDur # read signed 2 byte shorts
			# else:
			# 	raise ValueError("Only supports 8 and 16 bit audio formats.")
            #
			# monoFrames = struct.pack(fmt,*monoFrames)
            #
			# #set parameters for a write file
			# splitFile.setnchannels(1)
			# splitFile.setsampwidth(file.getsampwidth())
			# splitFile.setframerate(rate)
			# splitFile.setcomptype(file.getcomptype(),file.getcompname())
			# splitFile.setnframes(frameDur)
            #
			# #write
			# splitFile.writeframes(monoFrames)
			splitFile.close()

if __name__ == '__main__':
  try:
    path = sys.argv[1]
  except:
    print usage
    sys.exit(-1)
  main(path)
