import os
#Create nested directories
base_dir = "example_dir/subdir1/subdir2"
os.makedirs(base_dir, exist_ok=True)
print("Nested directories created.")

#List files and folders in current directory
print("\nFiles and folders in current directory:")
for item in os.listdir("."):
    print(item)

#Create some example files
open("example_dir/file1.txt", "w").close()
open("example_dir/file2.py", "w").close()
open("example_dir/file3.txt", "w").close()

#Find files by extension
print("\nFinding .txt files:")
for root, dirs, files in os.walk("example_dir"):
    for file in files:
        if file.endswith(".txt"):
            print(os.path.join(root, file))