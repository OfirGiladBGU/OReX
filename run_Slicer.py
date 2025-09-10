import os
import subprocess

input_folder = './parse/input'
output_folder = './parse/slices'
num = '100'

for filename in os.listdir(input_folder):
    if filename.endswith('.obj'):
        input_path = os.path.join(input_folder, filename)
        cmd = ['python3', 'Slicer.py', input_path, output_folder, num]
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd)
