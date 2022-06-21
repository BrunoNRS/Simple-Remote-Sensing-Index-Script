# Simple Remote Sensing Index Script
## About
This is a simple, general purpose, remote sensing python script,  with it, you are able to reproject, crop, extract indexes, and write a csv file.

This script is written with the MicaSense Altum camera in mind, but it also supports simpler RGB cameras, and the script is modular enough, that it can support any kind of camera model. 

## Usage 
### Module Instalation 
This script uses several [**Anaconda**](https://www.anaconda.com/) packages:
- [**gdal**](https://anaconda.org/conda-forge/gdal)
- [**earthpy**](https://anaconda.org/conda-forge/earthpy)
- [**rasterio**](https://anaconda.org/conda-forge/rasterio)
- [**numpy**](https://anaconda.org/conda-forge/numpy)
- [**matplotlib**](https://anaconda.org/conda-forge/matplotlib)
- [**fiona**](https://anaconda.org/conda-forge/fiona)

I recommend usage of the [**Mamba**](https://github.com/mamba-org/mamba) package manager for easy installation.

## 0.[**Reprojection**](https://github.com/BrunoNRS/Simple-Remote-Sensing-Index-Script/blob/main/Altum/0_reproject_module.py)
This is an optional step, the  reprojection script is to be used when the image file CRS (Coordinate Reference System) does not match with the CRS from the shape file.

- Insert the CRS reference number and the file directory to create a reprojected image.

## 1.[**Cropping**](https://github.com/BrunoNRS/Simple-Remote-Sensing-Index-Script/blob/main/Altum/1_crop_module.py)
This cropping process can accept a shape file or several, so they can crop one image.
- Insert the path to the image file
- The path to the shape file directory
- The output path of the cropped images
- The nodata values for the borders 

## 2.[**Index**](https://github.com/BrunoNRS/Simple-Remote-Sensing-Index-Script/blob/main/Altum/2_index_extract_moule_ALTUM.py)
This is the index module, here you can calculate several indexes generating a histogram graph and a GeoTiff image at the moment it supports these indexes:
- (NDVI) - Normalized Difference Vegetation Index
- (SAVI) - Soil-Adjusted Vegetation Index
- (VIG) - Vegetation Index Green
- (ExG) - Excess Green Index
- (GLI) - Green Leaf Index
- (MGRVI) - Modified Green Red Vegetation Index
- (NDWI) - Normalized Difference Water Index

## 3.[**CSV**](https://github.com/BrunoNRS/Simple-Remote-Sensing-Index-Script/blob/main/Altum/3_csv_extract_module.py)
This is a simple CSV script that calculates, median, variation, standard deviation, minimum and maximum values from several images and attaches them to a csv file.
- Insert the indexed images directory
- OPTIONAL: Insert the dataset name, by default the script will use the folder name
