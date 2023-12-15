# Exploring Image Processing Algorithms Extracting Measurement Instrument Information on an ESP32 Microcontroller

This is the Repository for the Master Thesis of Lukas Schmid and Jonas Paul.

The contents of this Repository is structured as follows:

## Master_PIO
In this repository, the embedded Part of our Work is stored. It includes 7 folders and 2 files. The important parts for out thesis are the "models" and "src" folder.

### models
Here, the C++ file of our TFLite models used on the ESP32 is stored. They Are loaded from the main C++ file in the folder "src". To change the model, go to the models folder in the top most directory. Here, the 8 models are stored in C++ and TFLite form. When a model is chosen, copy the C++ file into this directory.

### src
Here, the main file containing the code run on the ESP32 is stored.

## models
Here our models are stored in 8 different folders. Model 1 to 8 are stored in their respective folder with a TFLite and C++ file each.

## Utils
This folder contains 6 files with helper functions.

### create_data_set
This file was used to create the basic structure of our data sets. It organizes the images taken into different folders, where each folder contains images with the same value.

### grad_cam
This file contains the XAI framework grad_cam. We utilized the gradcam algorithm in addition to the loss to monitor the performance of our models and their corresponding preprocess operations. However, in the end, it became obsolete since we knew what preprocessing works and did not deploy gradcam any further. 

### image_display
Code to display images loaded into our Jupyter Notebooks can be seen here.

### preprocessing
This file contains two key processing steps:
1. Loading the data
2. Preprocessing the data

### transform_data
Here, functions to perform the data normalizations are stored.

## Model 1-8 Jupyter Notebooks
8 notebooks are stored. Each notebook contains the prediction of one of our 8 TFLite models tested during the expereimentation phase of our thesis.

## Notebook
Here, the pipeline to load and preprocess data, train models, evaluating them and creating the TFLite and C++ files are is presented.


# Images
The images of our work can be found in the following google drive folder:
https://drive.google.com/drive/folders/1wGEVjMup2ORU_9aknFUfYyV61re7CPlg?usp=sharing