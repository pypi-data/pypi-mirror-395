# morphodeep

[![License GNU LGPL v3.0](https://img.shields.io/pypi/l/morphodeep.svg?color=green)](https://github.com/Gitlab /morphodeep/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/morphodeep.svg?color=green)](https://pypi.org/project/morphodeep)
[![Python Version](https://img.shields.io/pypi/pyversions/morphodeep.svg?color=green)](https://python.org)
[![tests](https://github.com/Gitlab /morphodeep/workflows/tests/badge.svg)](https://github.com/Gitlab /morphodeep/actions)
[![codecov](https://codecov.io/gh/Gitlab /morphodeep/branch/main/graph/badge.svg)](https://codecov.io/gh/Gitlab /morphodeep)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/morphodeep)](https://napari-hub.org/plugins/morphodeep)
[![npe2](https://img.shields.io/badge/plugin-npe2-blue?link=https://napari.org/stable/plugins/index.html)](https://napari.org/stable/plugins/index.html)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)

# MorphoDeep

MorphoDeep is a **Python package** for performing **membrane instance segmentation** using a pre-trained **U-Net** model based on the Semantic format.  
It produces a dense **labels image** where each unique integer corresponds to a segmented cell instance.
It also includes a **napari plugin**

The plugin is designed for:

- fluorescence images of cell membranes  
- 2D and 3D volumes (with optional isotropic rescaling)  
- interactive use in napari or scripted use in Python

---
## Key features

- **Pre-trained U-Net** for 2D / pseudo-3D membrane instance segmentation  
- **Napari widget** with:
  - image layer selection
  - network patch size (`128` or `256`)
  - 2D / 3D mode
  - optional tiling (“patches mode”) for large images
  - voxel size and Z-axis selection
  - optional isotropic rescaling for anisotropic volumes
  - Automatic model download and caching on first use

---

## Installation
Setup your environnement 
```
conda create -y -n morphodeep-env python=3.10
conda activate morphodeep-env
```
You can install `morphodeep` via ff[pip]:

```
pip install morphodeep
```

## Installation with napari
Setup your environnement 
```
conda create -y -n napari-env -c conda-forge python=3.11
conda activate napari-env
```
You can install `morphodeep` plugin with napari and Qt via:

```
pip install "napari[all]"
pip install "morphodeep[napari]"

```


---


# MorphoDeep library Usage 
You  have 3 way to use the morphodeep library: 
1. with a command line :  ` python morphodeep.py  <args> `
2. directly inside the python code using the semantic library: `MorphoModel(args)`
3. directly in napari with the morphodeep plugin


## Arguments  

#### JOBS (run the command line in a job )
  - `--job` : Launch the corresponding job 
  - `--exe` : Execute the method ( ground_truth ... )
  - `--path_jobs` : path job output
  - `--job_number` :  Launch a sepecif job in job array list
  - `--job_filename` : The file of the job array list
  - 
#### ACTION
  - `--train` :  Launch the training
  - `--predict` :  Launch the prediction
  - `--ground_truth` : Generate all the ground truth
  - `--setdata` : Generate the data list files used for train/test/predict
  - `--export` : Compute the testing set and plot the results in figures
  - `--evolution` : Evaluation the testing set throught the different epochs
  - `--export_evol` : Predict for each epochs 
  - `--eval` : Evaluation of training database 
  - `--plot` : Compute export and plot loss
  - `--plot_loss` : Plot the loss and accuracy

#### METHOD
 - `-mode` :  2D or 3D
  - `--img_size` :  image size
  - `--full` :  Use a several layers to complete a tiles network to a work with image size
  - `--weight_files` :  weight files
  - 
#### TRAINING
  - `--batch_size` :  "batch_size
  - `--steps_per_epoch` :  steps_per_epoch
  - `--epochs` :  number of epochs
  - `--log_path` :  log path for tensorboard
  - `--specie` :  which specie ? (PM,DR,AT,DM,or PM-AT, PM-DM-AT, CP (for CellPose)
  - `--microscope` :  which microscope ? (SPIM (for lightsheet), CONF (for confocal),SIM (for simulated))
  - `--augmentation` :  Use Data Augmentation ? Default is False
  - `--pondere` :  Keep only the worst element (10%) for training 

#### DATA Management
  - `--input_path` :  Input Path (depend on the called method )
  - `--output_path` :  Output Path (depend on the called method 
  - `--membrane_filename` :  Filename membrane")
  - `--nucleus_filename` :  Filename nucleus")
  - `--segmented_filename` :  Filename segmented")
  - `--embryo_name` :  Embryo Name")
  - `--ratio` :  Resize the full database")
  - `--input_method` :  Input Method (for Ground Truth Calculcation)")

#### DATASET
  - `--dataset_file` :  Dataset File without .train, .valid and .test
  - `--test_split` :  Float between 0 and 1. Fraction of the data to be used as test data.
  - `--validation_split` :  Float between 0 and 1. Fraction of the data to be used as validate data.

#### PREDICTION
  - `--input_file` :  Input Filename to predict
  - `--output_file` :  Output Filename of the predicted image
  - `--patches` :  uses for prediction 

#### RESULT
  - `--export_path` :  The export path for the results

---
## DATA PREPARATION  

### 1. Extract segmentation and Raw Images data
#### SPIM PHALLUSIA MAMILATA
example :`python morphodeep.py --microscope SPIM --specie PM --phallusia_data`  
#### CONF ARABIDOPSSIS 
example :`python morphodeep.py --microscope CONF --specie AT --arabidopsis_data` 
#### CONF LATERAL ROOTS
example :`python morphodeep.py --microscope CONF --specie LP --plantseg_data` 
#### CONF OVULES 
example :`python morphodeep.py --microscope CONF --specie OV --plantseg_data` 
#### CONF SEA STAR
example :`python morphodeep.py --microscope CONF --specie SS --seastar_data `   
#### CONF C ELEGANS
example :`python morphodeep.py --microscope CONF --specie CE --celegans_data`    

### 2. Generate all Ground Truth
args : ` --ground_truth `
example :`python morphodeep.py --ground_truth --microscope CONF --specie SS  ` 

### 3. Split Train,Test Valid data 
args : ` --setdata `
example :`python morphodeep.py  --setdata --microscope CONF --specie SS `

#### 3.b To transfert your data in 128 patches 
example : `python morphodeep.py  --setdata --img_size 128`

### 4. Predict Cellpose (on test data)
args : ` --predict_cellpose `
example :`python morphodeep.py  --predict_cellpose --exe --microscope SPIM --specie PM ` 

### 5. Predict PlantSeg (on test data)
args : ` --predict_plantseg `
example :`python morphodeep.py  --predict_plantseg --exe --microscope CONF --specie OV `  

### 6. DataManagement 
To compress or uncompress data from $STORE path in Jean Zay : `morphodeep/DataManagement/store_data.py`
example :`python store_data.py --compress --microscope CONF --specie PM `
  
### 7. Train Semantic Networks
args : ` --train `
example : ` python morphodeep.py  --train  --microscope SPIM --specie PM `

### 8. Compute accuracy and plot loss evolution
args : ` --plot `
example : ` python morphodeep.py --plot --microscope CONF --specie AT `

### 9. Benchmark Test data (from figures path)
example : `  python Benchmark.py --predict`

### 11. Benchmark on external data
args : ` python Benchmark.py --predict -f figure_5/EXTERNAL_DATA/external_data_3D.txt`

---
## 2D 
Everything is by default in 3D, add ` --mode 2D`  to comptue evertyhing in 2D

### 1. Convert in 2D DATA  (and generate txt files)
We extract all the 3D datbase to 2D slices 
args : ` --extract_2D `
example :`python morphodeep.py --mode 3D  --microscope ALL --specie all --extract_2D [-wh <test;train;valid>]`  

### 2. Generate all Ground Truth for all species (includ in all)
args : ` --ground_truth `
example :`python morphodeep.py --mode 2D --ground_truth  --microscope SPIM --specie PM ` 

### 3. Predict Cellpose (on test data)
args : ` --predict_cellpose `
example :`python morphodeep.py  --mode 2D --predict_cellpose   ` 

### 4. Predict PlantSseg (on test data)
args : ` --predict_plantseg `
example :`python morphodeep.py  --mode 2D --predict_plantseg   `  

### 6. DataManagement 
To compress or uncompress data from $STORE path in Jean Zay : `semantic/DataManagement/store_data.py`
example :`python store_data.py --mode 2D --compress --microscope CONF --specie PM `
 
### 7. Train Semantic Networks
args : ` --train `
example : ` python morphodeep.py  --mode 2D --batch_size 32  --train `

### 8. Compute accuracy and plot loss evolution
args : ` --plot `
example : ` python morphodeep.py --mode 2D --plot `

### 12. Benchmark Test data (from figures path)
example : `python Benchmark.py --predict -t 2D  -p True`

### 12. Benchmark on external data
example : `python Benchmark.py --predict -t 2D -p True -n DUNNET -f /lustre/fsn1/projects/rech/dhp/uhb36wd/DATA_INTEGRATION//EXTERNAL_DATA_2D/external_data_2D.txt`


---

This [napari] plugin was generated with [copier] using the [napari-plugin-template] (None).


## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [GNU LGPL v3.0] license,
"morphodeep" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[copier]: https://copier.readthedocs.io/en/stable/
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[napari-plugin-template]: https://github.com/napari/napari-plugin-template

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
