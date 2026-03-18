import os
import shutil
source = "example_dir/file1.txt"
destination_dir = "example_dir/subdir1"

#Move file
if os.path.exists(source):
    shutil.move(source, destination_dir)
    print("File moved successfully.")

#Copy file
src_copy = "example_dir/file2.py"
dest_copy = "example_dir/subdir1/file2_copy.py"
if os.path.exists(src_copy):
    shutil.copy(src_copy, dest_copy)
    print("File copied successfully.")