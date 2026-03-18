#Write to an Existing File
with open("demofile.txt", "a") as f:
    f.write("Now the file has more content!")
with open("demofile.txt") as f:
    print(f.read())

#Overwrite Existing Content
with open("demofile.txt", "w") as f:
    f.write("Woops! I have deleted the content!")
with open("demofile.txt") as f:
    print(f.read())

#Create a New File
f = open("myfile.txt", "x")