# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:58:08 2022

@author: Bruno do Nascimento (bruno.do.nrs@gmail.com)
"""

from builtins import WindowsError
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
mpl.use('Agg')

# Define Original GeoTiff file location
imagery = ("Photos/")


# Define Shapefile file or files location
shape_directory = ("Shapes/")

# Define Output for Indexing
outimg = ("Crop/")

# # TESTING: Specify output projection system
# dst_crs = 'EPSG:32324'

# # Input imagery file name before transformation
# input_imagery_file = "20210106_uva_andorinhas_altum_orto_crop.tif"

# # Save output imagery file name after transformation
# transformed_imagery_file = '20210106_uva_andorinhas_altum_orto_crop_32324.tif'

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
for shapepath in glob.glob(os.path.join(shape_directory, '*.shp')):
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
        
    for primetif in glob.glob(os.path.join(imagery, '*.tif')):
        #print(primetif)
        # Read imagery file
        with rasterio.open(primetif) as src:
            out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
            out_meta = src.meta
            
        # Save clipped imagery
        out_meta.update({"driver": "GTiff",
                          "height": out_image.shape[1],
                          "width": out_image.shape[2],
                          "transform": out_transform})

        with rasterio.open(os.path.join("Crop", shapename + '.tif'), "w", **out_meta) as dest:
            dest.write(out_image)
            
        for outpath in glob.glob(os.path.join(outimg, '*.tif')):
            #print(outpath)
            outfile =  os.path.basename(outpath)
            #print(outfile)
            outname = os.path.splitext(outfile)[0]
            #print(outname)
            
            # orto = rxr.open_rasterio(outpath)
            
            output_path = outname + "_output"
            
            try:
                os.mkdir(output_path)
            except WindowsError:
            # Handle the case where the target dir already exist.
                pass

            try:
                os.mkdir(os.path,join(output_path, "Index_GeoTIFFF"))
            except WindowsError:
                pass
            
            # B = orto[0]
            # G = orto[1]
            # R = orto[2]
            # N = orto[3]
            # T = orto[5] / 100 - 273.15
            # L = 0.5
            
            with rasterio.open(outpath) as src:
                B = src.read(1)
            with rasterio.open(outpath) as src:
                G = src.read(2)
            with rasterio.open(outpath) as src:
                R = src.read(3)
            with rasterio.open(outpath) as src:
                N = src.read(4)
            with rasterio.open(outpath) as src:
                T = src.read(6)
            L = 0.5
                
            kwargs = src.meta
            kwargs.update(
                dtype=rasterio.float32,
                count = 1)
            
            ndvi_index = (N - R)/(N + R)
            
            ep.plot_bands(ndvi_index,
                          cmap='RdYlGn',
                          scale=False,
                          vmin=0, vmax=1,
                          title="Normalized Difference Vegetation Index(NDVI)\n" + outname)

            plt.savefig(os.path.join(output_path,  outname + " NDVI.png"), bbox_inches='tight')
            
            with rasterio.open(os.path.join(output_path, "Index_GeoTIFF", outname + "NDVI.tif"), 'w', **kwargs) as dst:
                    dst.write_band(1, ndvi_index.astype(rasterio.float32))
            
            
            savi_index = ((N - R) / (N + R + L)) * (1 + L)

            ep.plot_bands(savi_index,
                          cmap='RdYlGn',
                          scale=False,
                          vmin=0, vmax=1,
                          title="Soil-Adjusted Vegetation Index(SAVI)\n " + outname)

            plt.savefig(os.path.join(output_path, outname + " SAVI.png"), bbox_inches='tight')

            with rasterio.open(os.path.join(output_path, "Index_GeoTIFF", outname + "SAVI.tif"), 'w', **kwargs) as dst:
                    dst.write_band(1, savi_index.astype(rasterio.float32))

            vig_index = (G - R) / (G + R)

            ep.plot_bands(vig_index,
                          cmap='RdYlGn',
                          scale=False,
                          vmin=0, vmax=1,
                          title="Vegetation Index Green(VIG)\n " + outname)

            plt.savefig(os.path.join(output_path, outname + " VIG.png"), bbox_inches='tight')

            with rasterio.open(os.path.join(output_path, "Index_GeoTIFF", outname + "VIG.tif"), 'w', **kwargs) as dst:
                    dst.write_band(1, vig_index.astype(rasterio.float32))

            exg_index = 2 * G - R - B

            ep.plot_bands(exg_index,
                          cmap='RdYlGn',
                          scale=False,
                          vmin=0, vmax=1,
                          title="Excess Green Index(ExG)\n " + outname)

            plt.savefig(os.path.join(output_path, outname + " ExG.png"), bbox_inches='tight')

            with rasterio.open(os.path.join(output_path, "Index_GeoTIFF", outname + "ExG.tif"), 'w', **kwargs) as dst:
                    dst.write_band(1, exg_index.astype(rasterio.float32))

            gli_index = (2.0 * G - R - B) / (2.0 * G + R + B)

            ep.plot_bands(gli_index,
                          cmap='RdYlGn',
                          scale=False,
                          vmin=0, vmax=1,
                          title="Green Leaf Index(GLI)\n " + outname)

            plt.savefig(os.path.join(output_path, outname + " GLI.png"), bbox_inches='tight')

            with rasterio.open(os.path.join(output_path, "Index_GeoTIFF", outname + "GLI.tif"), 'w', **kwargs) as dst:
                    dst.write_band(1, gli_index.astype(rasterio.float32))

            mgrvi_index = (G ** 2.0 - R ** 2.0) / (G ** 2.0 + R ** 2.0)

            ep.plot_bands(mgrvi_index,
                          cmap='RdYlGn',
                          scale=False,
                          vmin=0, vmax=1,
                          title="Modified Green Red Vegetation Index(MGRVI)\n " + outname)

            plt.savefig(os.path.join(output_path, outname + " MGRVI.png"), bbox_inches='tight')

            with rasterio.open(os.path.join(output_path, "Index_GeoTIFF", outname + "MGRVI.tif"), 'w', **kwargs) as dst:
                    dst.write_band(1, mgrvi_index.astype(rasterio.float32))

            ndwi_index = (G - N) / (G + N)

            ep.plot_bands(ndwi_index,
                          cmap='RdYlGn',
                          scale=False,
                          vmin=0, vmax=1,
                          title="Normalized Difference Water Index(NDWI)\n " + outname)

            plt.savefig(os.path.join(output_path, outname + " NDWI.png"), bbox_inches='tight')

            with rasterio.open(os.path.join(output_path, "Index_GeoTIFF", outname + "NDWI.tif"), 'w', **kwargs) as dst:
                    dst.write_band(1, ndwi_index.astype(rasterio.float32))

            colors = ['b', 'g', 'r', 'k', 'tomato', 'purple']
            titles = [ outname + " \n Blue",  outname + " \n Green",  outname + " \n Red",  outname + " \n Near Infrared",  outname + " \n Red Edge",  outname + " \n Thermal"]

            ep.hist(src.values, 
                    colors=colors, 
                    title=titles, 
                    cols=2)

            plt.savefig(os.path.join(output_path, outname + " Histogram.png"), bbox_inches='tight')

            ep.plot_bands(T,
                          title=outname + " \n Thermal",
                          cbar=True,
                          cmap='CMRmap',
                          scale=False,
                          vmin=15, vmax=50)

            plt.savefig(os.path.join(output_path, outname + " Thermal.png"), bbox_inches='tight')

            for saved_indexes in glob.glob(os.path.join(output_path, "Index_GeoTIFF", '*.tif')):
                indexes = rxr.open_rasterio(saved_indexes)

                colors = ['b', 'g', 'r', 'k', 'tomato', 'purple']
                titles = [ outname + " \n Blue",  outname + " \n Green",  outname + " \n Red",  outname + " \n Near Infrared",  outname + " \n Red Edge",  outname + " \n Thermal"]
                
                ep.hist(saved_indexes.values, 
                    colors=colors, 
                    title=titles, 
                    cols=2)


            


        



            
            
                