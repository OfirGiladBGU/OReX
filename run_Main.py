import os
import subprocess
import pathlib

input_folder = './parse_preds_fixed/slices'
output_folder = './parse_preds_fixed/output'
log_folder = './log2'
num = '0'

# Create log folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(log_folder, exist_ok=True)

filenames = sorted(pathlib.Path(input_folder).glob("*.csl"))
for idx, filename in enumerate(filenames):
    filename = filename.name
    input_path = os.path.join(input_folder, filename)
    log_file = os.path.join(log_folder, f"{filename}.log")
    cmd = f"nohup python3 Main.py '{output_folder}' '{input_path}' --cuda_device '{num}' > '{log_file}' 2>&1 &"
    print(f"Running in background: {cmd}")
    subprocess.Popen(cmd, shell=True)
