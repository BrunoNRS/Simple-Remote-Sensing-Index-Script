# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:58:08 2022

@author: Bruno do Nascimento (bruno.do.nrs@gmail.com)
"""

import glob, os
import matplotlib.pyplot as plt
import numpy as np
import rioxarray as rxr
import geopandas as gpd
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import matplotlib as mpl
import fiona
import rasterio
import rasterio.mask
from rasterio.plot import show
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Specify output projection system
dst_crs = 'EPSG:32324'

# # Input imagery file name before transformation
# input_imagery_file = "65-Orthomosaic-Uva de suco_rgb_20170515.tif"

# # Save output imagery file name after transformation
# transformed_imagery_file = '65-Orthomosaic-Uva de suco_rgb_20170515_32324.tif'

# #---------------------------------------------------------------------------
# #TO DO: If CRS is not the same reproject to the same crs of the shape file
# #then load the equivalent crc reprojection for processing.
# #---------------------------------------------------------------------------

# # Image reprojection script
# with rasterio.open(input_imagery_file) as imagery:
#     transform, width, height = calculate_default_transform(imagery.crs, dst_crs, imagery.width, imagery.height, *imagery.bounds)
#     kwargs = imagery.meta.copy()
#     kwargs.update({'crs': dst_crs, 'transform': transform, 'width': width, 'height': height})
#     with rasterio.open(transformed_imagery_file, 'w', **kwargs) as dst:
#         for i in range(1, imagery.count + 1):
#             reproject(
#                 source=rasterio.band(imagery, i),
#                 destination=rasterio.band(dst, i),
#                 src_transform=imagery.transform,
#                 src_crs=imagery.crs,
#                 dst_transform=transform,
#                 dst_crs=dst_crs,
#                 resampling=Resampling.nearest)

#Start crop module, crate a crop directory, and crop and output
for shapepath in glob.glob('shapes_amarelo/*.shp'):
    try:
        os.mkdir("Crop")
    except WindowsError:
    # Handle the case where the target dir already exist.
        pass
    # print(shapepath)
    shapefile =  os.path.basename(shapepath)
    # print(shapefile)
    shapename = os.path.splitext(shapefile)[0]
    print(shapename)
   
    # Read Shape file
    with fiona.open(shapepath, "r") as shapepath:
        shapes = [feature["geometry"] for feature in shapepath]

    # Read imagery file
    with rasterio.open("65-Orthomosaic-Uva de suco_rgb_20170515_32324.tif") as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    # Save clipped imagery
    out_meta.update({"driver": "GTiff",
                      "height": out_image.shape[1],
                      "width": out_image.shape[2],
                      "transform": out_transform})

    with rasterio.open(os.path.join("Crop", shapename + '.tif'), "w", **out_meta) as dest:
        dest.write(out_image)

