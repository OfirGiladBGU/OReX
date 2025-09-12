import os
import subprocess

input_folder = './parse/input'
output_folder = './parse/slices'
log_folder = './log'
num = '100'

# Create log folder if it doesn't exist
os.makedirs(log_folder, exist_ok=True)

filenames = sorted(os.listdir(input_folder))
for idx, filename in enumerate(filenames):
    if idx + 1 < 46:
        continue
    if filename.endswith('.obj'):
        input_path = os.path.join(input_folder, filename)
        log_file = os.path.join(log_folder, f"{filename}.log")
        cmd = f"nohup python3 Slicer.py '{input_path}' '{output_folder}' '{num}' > '{log_file}' 2>&1 &"
        print(f"Running in background: {cmd}")
        subprocess.Popen(cmd, shell=True)
