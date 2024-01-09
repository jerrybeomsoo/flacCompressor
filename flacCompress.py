# Usage

# For compression (Any file -> wav -> flac) : "flacCompress.py --compress|-C 8|16 <sampleRate> <file path>"
# Example : flacCompress.py --compress/-C/ 8 44100 C:\Users\user\Documents\test.txt
# Result : test.txt.flac at the same directory of flacCompress.py

# For decompression (flac -> wav -> original file) : "flacCompress.py --decompress|-D <file path>"
# Example : flacCompress.py --decompress/-D C:\Users\user\Documents\test.txt.flac
# Result : test.txt at the same directory of flacCompress.py


import sys, os
from pathlib import Path
# Requires Xiph.Org flac to be installed and added to PATH

class wavfile:
    inputHeader = bytes()

    chunkSize_4to7 = 0
    chunkSize_16to19 = 16
    numberOfChannels = 1
    sampleRate = 0
    byteRate = 1
    blockAlign = 1
    bitsPerSample = 8
    chunkSize_40to43 = 0

    byte_chunkSize_4to7 = None
    byte_chunkSize_16to19 = None
    byte_numberOfChannels = None
    byte_sampleRate = None
    byte_byteRate = None
    byte_blockAlign = None
    byte_bitsPerSample = None
    byte_chunkSize_40to43 = None

    def extractData(self):
        self.chunkSize_4to7 = int.from_bytes(self.inputHeader[4:8], "little", signed=True)
        self.chunkSize_16to19 = int.from_bytes(self.inputHeader[16:20], "little", signed=True)
        self.numberOfChannels = int.from_bytes(self.inputHeader[22:24], "little", signed=True)
        self.sampleRate = int.from_bytes(self.inputHeader[24:28], "little", signed=True)
        self.byteRate = int.from_bytes(self.inputHeader[28:32], "little", signed=True)
        self.blockAlign = int.from_bytes(self.inputHeader[32:34], "little", signed=True)
        self.bitsPerSample = int.from_bytes(self.inputHeader[34:36], "little", signed=True)
        self.chunkSize_40to43 = int.from_bytes(self.inputHeader[40:44], "little", signed=True)

    def generateData(self):
        self.byte_chunkSize_4to7 = (self.chunkSize_4to7).to_bytes(4, "little")
        self.byte_chunkSize_16to19 = (self.chunkSize_16to19).to_bytes(4, "little")
        self.byte_numberOfChannels = (self.numberOfChannels).to_bytes(2, "little")
        self.byte_sampleRate = (self.sampleRate).to_bytes(4, "little")
        self.byte_byteRate = (self.byteRate).to_bytes(4, "little")
        self.byte_blockAlign = (self.blockAlign).to_bytes(2, "little")
        self.byte_bitsPerSample = (self.bitsPerSample).to_bytes(2, "little")
        self.byte_chunkSize_40to43 = (self.chunkSize_40to43).to_bytes(4, "little")

        newHeaderString = "RIFF" + str(self.byte_chunkSize_4to7)[2:-1] + "WAVEfmt " + str(self.byte_chunkSize_16to19)[2:-1] + "\\x01\\x00" + str(self.byte_numberOfChannels)[2:-1] + str(self.byte_sampleRate)[2:-1] + str(self.byte_byteRate)[2:-1] + str(self.byte_blockAlign)[2:-1] + str(self.byte_bitsPerSample)[2:-1] + "data" + str(self.byte_chunkSize_40to43)[2:-1] 
        self.inputHeader = bytes(newHeaderString, "ascii")
        self.inputHeader = self.inputHeader.decode('unicode_escape').encode('raw_unicode_escape')


if not((len(sys.argv) == 3) or (len(sys.argv) == 5)):
    print("Invalid number of arguments.\n")
    sys.exit()

compressMode = None
        
if sys.argv[1] == "--compress" or sys.argv[1] == "-C":
    compressMode = True
    file_path = sys.argv[4]
    bitDepth = int(sys.argv[2])
    if not((bitDepth == 8) or (bitDepth == 16)):
        print("Invalid bit depth.\n8 or 16 is allowed as bit depth.\n")
        sys.exit()
    sampleRate = int(sys.argv[3])
elif sys.argv[1] == "--decompress" or sys.argv[1] == "-D":
    compressMode = False
    file_path = sys.argv[2]
else: 
    print("Invalid arguments.")
    print("Usage\nfor compression: flacCompress.py --compress|-C 8|16 <sampleRate> <file path>\nfor decompression: flacCompress.py --decompress|-D <file path>\n")
    sys.exit()
    
if os.path.exists(file_path) == False:
    print("File does not exist.\n")
    sys.exit()
    
fileSize = os.path.getsize(file_path)
fileName = os.path.basename(file_path)
fileNameNoExt = Path(file_path).stem

if compressMode == True:
    if (fileSize % 2 != 0):
        if bitDepth == 16:
            print("The selected file could not be compressed into 16-bit audio file.\nPlease enter 8 as the bit depth.\n")
            sys.exit()
    
    print("Compressing...\n")
    
    fileToWav_Header = wavfile()
    fileToWav_Header.chunkSize_4to7 = fileSize + 36
    fileToWav_Header.sampleRate = sampleRate
    fileToWav_Header.bitsPerSample = bitDepth
    fileToWav_Header.blockAlign = int(fileToWav_Header.bitsPerSample/8)
    fileToWav_Header.byteRate = fileToWav_Header.sampleRate * fileToWav_Header.blockAlign
    fileToWav_Header.chunkSize_40to43 = fileSize
    fileToWav_Header.generateData()
    
    with open(file_path, "rb") as fileToCompressBin, open('temp.wav', "wb") as wavToWrite:
        wavToWrite.write(fileToWav_Header.inputHeader)
        for data in fileToCompressBin:
            wavToWrite.write(data)
    
    os.system('flac temp.wav --force')
    os.rename('temp.flac', '{0}.flac'.format(fileName))
    originalFileSize = os.path.getsize(file_path)
    flacFileSize = os.path.getsize((fileName) + ".flac")
    os.remove('temp.wav')
    
    print("\nCompression ratio: {0:.2f}%".format((flacFileSize/originalFileSize)*100))
    print("Original file size: {0} bytes".format(originalFileSize))
    print("Compressed file size: {0} bytes".format(flacFileSize))

else: # compressMode == False
    print("Decompressing...\n")
    
    os.system('flac -d -f {0}'.format(file_path))
    
    with open("{0}.wav".format(fileNameNoExt), "rb") as wavToRead, open(file_path[:-5], "wb") as fileToWrite:
        wavToRead.seek(44)
        for data in wavToRead:
            fileToWrite.write(data)
    
    os.remove('{0}.wav'.format(fileNameNoExt))

print("\nDone.\n")