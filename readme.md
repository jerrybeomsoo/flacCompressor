# flacCompress.py

A Python script for compressing/decompressing **ANY** files into FLAC audio files using Xiph.Org flac.

## Description

flacCompress.py is a command-line tool written in Python that allows you to **compress _any kind of files using FLAC_, and decompress it**.
The script converts the chosen file to mono 8/16 bit PCM .wav file, and then utilises the Xiph.Org flac library to compress the .wav file.
For decompression, vice versa.

## Dependencies

- Xiph.Org flac (or other compatible flac implementations) installed and added to PATH

## Usage

### To compress a file into flac format:
```python flacCompress.py --compress|-C <bitDepth> <sampleRate> <filePath>```

Example : ```python flacCompress.py --compress/-C/ 8 44100 C:\Users\user\Documents\test.txt```

*Result : test.txt.flac (which is mono 8-bit 44.1kHz audio) at the same directory of flacCompress.py*


### To decompress the file that is in flac format:
```python flacCompress.py --decompress|-D <filePath>```

Example : ```python flacCompress.py --decompress/-D C:\Users\user\Documents\test.txt.flac```

*Result : test.txt at the same directory of flacCompress.py*
