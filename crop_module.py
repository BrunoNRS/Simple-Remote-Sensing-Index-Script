# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:19:32 2022

@author: Bruno do Nascimento
"""

import fiona
import rasterio
import rasterio.mask
from rasterio.plot import show
from rasterio.warp import calculate_default_transform, reproject, Resampling

import geopandas as gpd

import numpy as np

# Read shape file using geopandas
shape_file = gpd.read_file("sample_file.shp")

# Read image file
orto = rasterio.open("sample_file.tif")

# Plot image file
show(orto)

# Check coordinate reference system (CRS) of both datasets
print('Shape file Projection: ', shape_file.crs)
print('------------------------//////---------------------')
print('Imagery file Projection: ', orto.crs)

#---------------------------------------------------------------------------
#TO DO: If CRS is not the same reproject to the same crs of the shape file
#then load the equivalent crc reprojection for processing.
#---------------------------------------------------------------------------

# Specify output projection system
dst_crs = 'EPSG:32324'

# Input imagery file name before transformation
input_imagery_file = "sample_file.tif"

# Save output imagery file name after transformation
transformed_imagery_file = 'sample_file_*crs*.tif'

# Image reprojection script
with rasterio.open(input_imagery_file) as imagery:
    transform, width, height = calculate_default_transform(imagery.crs, dst_crs, imagery.width, imagery.height, *imagery.bounds)
    kwargs = imagery.meta.copy()
    kwargs.update({'crs': dst_crs, 'transform': transform, 'width': width, 'height': height})
    with rasterio.open(transformed_imagery_file, 'w', **kwargs) as dst:
        for i in range(1, imagery.count + 1):
            reproject(
                source=rasterio.band(imagery, i),
                destination=rasterio.band(dst, i),
                src_transform=imagery.transform,
                src_crs=imagery.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest)

# Check coordinate reference system (CRS) of both datasets AGAIN
print('Shape file Projection: ', shape_file.crs)
print('------------------------//////---------------------')
print('Imagery file Projection: ', transformed_imagery_file.crs)

# This is the crop module

# Read Shape file
with fiona.open("sample_file.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

# Read imagery file
with rasterio.open("sample_file_*crs*.tif") as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta

# Save clipped imagery
out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open("croped_sample_file.tif", "w", **out_meta) as dest:
    dest.write(out_image)