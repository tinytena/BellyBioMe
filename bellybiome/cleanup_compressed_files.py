import os
import time

# Path to your compressed static files directory
compressed_files_dir = "bellybiome/staticfiles"

# Time in seconds (e.g., 30 days)
max_age = 30 * 24 * 60 * 60

now = time.time()

for root, dirs, files in os.walk(compressed_files_dir):
    for file in files:
        file_path = os.path.join(root, file)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > max_age:
                os.remove(file_path)
                print(f"Deleted {file_path}")
