# To create a conda environment with Python 3.10:
conda create -n orex python=3.10

# To activate the environment:
conda activate orex

# After activation, install requirements:
pip install -r requirements.txt

# For CUDA support (PyTorch), use the following in requirements.txt:
torch==1.13.1+cu117
# And add the following line at the top of requirements.txt:
--extra-index-url https://download.pytorch.org/whl/cu117

# This ensures PyTorch is installed with CUDA 11.7 support.
