# dps.training_qrcode_generator

This repository contains scripts for generating QR Code Printouts that can be used for digital MCI trainings with
the "dps.training" software that can be found in the following repositories:
- [dps.training_server](https://github.com/hpi-sam/dps.training_server) 
- [dps.training_player](https://github.com/hpi-sam/dps.training_player) 
- [dps.training_trainer](https://github.com/hpi-sam/dps.training_trainer) 

There actually are three different scripts for the different types of QR Code Printouts to be generated (patients, 
containers, vehicles). 

The scripts compile a LaTeX `.tex` document using different `.tex`-fragments from the `components` folder based on the
presets specified as `.csv` files in the `input` directory, and starts `pdflatex` to create the final PDF document.



## Usage and Installation

### Installation
1. Make sure you have [poetry](https://python-poetry.org/docs/#installation) installed.
2. Clone this repository and run `poetry install` in the root directory.
3. Make sure you have LaTeX installed, as the python program calls upon the `pdflatex` command. 

### Usage
1. Choose the script you want to use (python files in the root folder).
2. Change any settings you like in the top section of the script or in the referenced `.csv` files.
3. Run `python generate_<xxxx>_qr_codes.py`.
4. After the script is finished, retrieve the generated PDF file from the `output` folder.
