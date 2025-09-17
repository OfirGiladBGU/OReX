import os
import subprocess
import pathlib

# input_folder = './parse_labels/input'
# output_folder = './parse_labels/slices'
# log_folder = './log1_labels'

input_folder = './parse_preds_fixed/input'
output_folder = './parse_preds_fixed/slices'
log_folder = './log1_preds_fixed'
num = '100'

# Create log folder if it doesn't exist
os.makedirs(log_folder, exist_ok=True)

filenames = sorted(pathlib.Path(input_folder).glob("*.obj"))
for idx, filename in enumerate(filenames):
    filename = filename.name
    if idx + 1 < 46:
        continue
    input_path = os.path.join(input_folder, filename)
    log_file = os.path.join(log_folder, f"{filename}.log")
    cmd = f"nohup python3 Slicer.py '{input_path}' '{output_folder}' '{num}' > '{log_file}' 2>&1 &"
    print(f"Running in background: {cmd}")
    subprocess.Popen(cmd, shell=True)
