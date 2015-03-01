# Author:      Maciej 'mc' Suchecki

# Description: Script used to upload photos to Dropbox public folder.
# Usage:       Just fill the setting variables and run the sript.

import os
import zipfile
import dropbox
from PIL import Image, ExifTags

# settings
desiredSize = 1920                  # longer side
directoryToPublish = '/home/mc/Pictures/.../.../'
archiveName = 'photos.zip'
validExtensions = ('.JPG', '.jpg', '.jpeg', '.gif')

# resizes photo while keeping the aspect raito unmodified
def resizePhoto(photo) :
  aspect = float(photo.size[0]) / float(photo.size[1])
  if aspect > 1 :
    return photo.resize((desiredSize, round(desiredSize/aspect)))
  else :
    return photo.resize((round(desiredSize*aspect), desiredSize))

def isPhoto(file) :
  return file.endswith(validExtensions)

# connect to Dropbox
appKey = 'put key here'
appSecret = 'put secret here'
flow = dropbox.client.DropboxOAuth2FlowNoRedirect(appKey, appSecret)
# TODO improve this...
authorizeUrl = flow.start()
print('1. Go to: ' + authorizeUrl)
print('2. Click "Allow" (you might have to log in first)')
print('3. Copy the authorization code.')
code = input("Enter the authorization code here: ").strip()
# ...part of code
accessToken, userID = flow.finish(code)
dropboxClient = dropbox.client.DropboxClient(accessToken)

# create /tmp folder
os.makedirs(os.path.join(directoryToPublish, 'tmp'))
os.chdir(os.path.join(directoryToPublish, 'tmp'))

# resize and copy photos
print('Resizing and compressing photos...')
archive = zipfile.ZipFile(os.path.join(directoryToPublish, 'tmp', archiveName), 'w')
for file in os.listdir(directoryToPublish) :
  if isPhoto(file) :
    print(os.path.join(directoryToPublish, file))
    image = Image.open(os.path.join(directoryToPublish, file))
    if not file.endswith('.gif') :
      image = resizePhoto(image)
    image.save(file)
    archive.write(file)
    os.remove(file)

# upload archive
print('Uploading...')
archive.close()
archive = open(archiveName, 'rb')
uploadResponse = dropboxClient.put_file('/Public/' + archiveName, archive)
archive.close()

# remove zip file and tmp directory
os.remove(archiveName)
os.chdir(directoryToPublish)
os.rmdir('tmp')

# get link
shareResponse = dropboxClient.share(uploadResponse['path'], short_url=True)
print(uploadResponse['size'] + ' uploaded! Link to published pictures: ' + shareResponse['url'])
print('Link expires at: ' + shareResponse['expires'])
