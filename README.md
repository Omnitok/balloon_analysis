# balloon_analysis
codes for analyzing B-ICI balloon data

Use typhon package for ginding equilibrium vapor pressure of water and ice
https://www.radiativetransfer.org/misc/typhon/doc/index.html

Convert the PTU and the ETAG file from esrange. 
Use 'plots.py' to create the plot, and 'ptu_data.py' to convert the ptu file

## Segmentation model
The model is in snow_crystal_segmentation folder. Already pretrained, currently using model #m232.
Run it with "sudo ./tools/run_inference.sh". Here you can change the input-output directories.
on "run_inference.py" One can set the detection limit for the model, and also can tweak the particle properties that the model will produce.

## Classification model
The model is in the folder "classification".
Pretrained, but ideally with every measurements the hand/automaticly classified particles are fed back to the training, to train a new model.

Run it with "classify.py" where the input/oputput folders can be set.
