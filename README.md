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
  --n_ref INTEGER        The index of the file that will be used as datum for
                         image registration (Default: 0)
  --pattern TEXT         The glob pattern to be used for file extraction
                         (Default: "*.TIFF")
  --circle_size INTEGER  The approximate diameter of a probe (Default: 15)
  --thresh FLOAT         Local percentile for intensity extraction (Default:
                         0.995)
  --window_size INTEGER  Size of the window used for local percentile
                         extraction (Default: 100)
  --img_scale FLOAT      Multiplier for image values to make it viewable
                         (Default: 1)
  --help                 Show this message and exit.
```
