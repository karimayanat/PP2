#Copy files
import shutil
shutil.copy('demofile.txt', 'destination.txt')

#Check if File exist and Delete a File
import os
if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")