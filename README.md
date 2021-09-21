# merFISH Barcode Visualizer

This application allows for decoding of imaging spots of unmerged vancouver merFISH data.

## Installation

This visualizer requires no installation. However, the conda environment `barcode_env` can be created with 

```
conda env create -f environment.yml
```

## Usage

```
conda activate barcode_env
python main.py makeBarcodeWithBead --help
Usage: main.py makeBarcodeWithBead [OPTIONS] IMG647_DIR IMG750_DIR BEAD_DIR

Options:
  --n_ref INTEGER
  --pattern TEXT
  --circle_size INTEGER
  --thresh FLOAT
  --window_size INTEGER
  --img_scale FLOAT
  --help                 Show this message and exit.
```
