# Description: Script analysing usage of different focal lengths in photos
#              existing in particular directory. Useful for helping with 
#              new fixed focal length lens selection.
# Usage:       Set directory with photos to analyze, set names of cameras
#              (from EXIF tags!) 'whose' photos you want to analyze and
#              set focal lengths that you want to approximate values into.
# Author:      Maciej 'mc' Suchecki

import os
from pylab import *
from PIL import Image, ExifTags
from sortedcontainers import SortedDict

# settings
photosDirectory = '/home/mc/Pictures/'
validExtensions = ('.JPG', '.jpg', '.jpeg')
validCameras = ['Canon EOS 400D DIGITAL', 'Canon EOS 100D']
focalLengths = [17.0, 20.0, 24.0, 28.0, 30.0, 35.0, 40.0, 50.0, 60.0, 85.0, 100.0, 135.0, 200.0, 250.0]

# EXIF tags
FOCALLENGTH_TAG = 0x920a
MODEL_TAG = 0x0110

def isPhoto(file) :
  return file.endswith(validExtensions)

def getExif(imagePath) :
  image = Image.open(imagePath)
  image.verify()
  return image._getexif()

def cameraIsValid(exif) :
  return exif[MODEL_TAG] in validCameras

# populate dictionary: keys - focal lengths, values - occurences
occurences = SortedDict()
for i in focalLengths :
  occurences[i] = 0

# iterate through whole directory
for subdir, dirs, files in os.walk(photosDirectory) :
  for file in files :

    if isPhoto(file) :
      try :
        exif = getExif(os.path.join(subdir, file))
        if not cameraIsValid(exif) :
          continue
        # get focal length and convert from rational data type to float
        focalLength = exif[FOCALLENGTH_TAG][0] / exif[FOCALLENGTH_TAG][1]
        # count every focal length occurence in dictionary
        if (focalLength in occurences) :
          occurences[focalLength] = occurences[focalLength] + 1
        else:   # find nearest
          index = occurences.bisect(focalLength)
          greater = occurences.iloc[index]
          smaller = occurences.iloc[index - 1]
          nearestFL = greater if (greater - focalLength < focalLength - smaller) else smaller
          occurences[nearestFL] = occurences[nearestFL] + 1
      except (KeyError, TypeError, IndexError) :
        # there is no focal length info in image exif data (Key/Type/IndexError)
        pass

# plot the graph
position = arange(len(focalLengths)) + .5
barh(position, occurences.values(), align='center', color='#FF0000')
yticks(position, occurences.keys())
xlabel('Occurrences')
ylabel('Focal length')
title('Focal length usage analysis')
grid(True)
show()
