# Conda Setup:

## To create a conda environment with Python 3.10:
conda create -n orex python=3.10

## To activate the environment:
conda activate orex

## After activation, install requirements:
pip install -r requirements.txt

## For CUDA support (PyTorch), use the following in requirements.txt:
torch==1.13.1+cu117
# And add the following line at the top of requirements.txt:
--extra-index-url https://download.pytorch.org/whl/cu117

## This ensures PyTorch is installed with CUDA 11.7 support.

---

# Files Setup:

- Use the copy script in `TreesAutoEncoder` to create the dirs:
    - `parse_labels/input`
    - `parse_preds_fixed/input`
- Run the `run_Slicer.py` to create slices for both labels and preds_fixed
- Run the `run_Main.py` to get the final OReX predictions.
- Copy the results to `TreesAutoEncoder` under: `datasets_visualize/orex`.
- Copy the `parse_labels` (as `labels`) and `parse_preds_fixed` (as `preds_fixed`).
- Remove uncessary files:
    - Unused `obj` files in `input` folders
    - The `csl` and `ply` files in `slices` folders
    - All the files in the `output` folder expect the `mesh_last_300.obj` files.
- Update the files:
    - Every `mesh_last_300.obj` file renambe by it's sub folder name and put it in the output folder.
- Run the `datasets_visualize/restore_original_scale.py` script for scale fix.
- Run the `datasets_visualize/translate_and_voxelize.py` script for voxelization alignment.

---

The commands format in use:

```bash
python3 Slicer.py ./parse_preds_fixed/input/PA000005_vessel.obj ./parse/slices 100
python3 Main.py ./parse_preds_fixed/output ./parse/slices/PA000005_vessel.csl --cuda_device 0 
```