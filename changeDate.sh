#!/bin/bash

# Author:      Maciej 'mc' Suchecki
# Description: Script for changing the EXIF time/date data written in photo file.
# Usage:       Set the following constants to different values as needed and run the script.

HOUR=16
MINUTE=0
DATE=2013:09:15

for file in "$1"/*;
do 
  # set image metadata
  exiv2 -v -M"set Exif.Image.DateTime $DATE $(printf %02d $HOUR):$(printf %02d $MINUTE):00" "$file"
  exiv2 -v -M"set Exif.Photo.DateTimeDigitized $DATE $(printf %02d $HOUR):$(printf %02d $MINUTE):00" "$file"
  exiv2 -v -M"set Exif.Photo.DateTimeOriginal $DATE $(printf %02d $HOUR):$(printf %02d $MINUTE):00" "$file"
  # this would rename the file as well
  new_path=`pwd`/new_filename$(printf %02d $HOUR)$(printf %02d $MINUTE).jpg
  cp "$file" "$new_path"
done

