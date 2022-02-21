"""
@author: Bruno do Nascimento (bruno.do.nrs@gmail.com)
"""
# WARNING: This script is designed for rgb cameras
# Ver 2.5
from builtins import WindowsError
import glob, os
import matplotlib.pyplot as plt
#import numpy as np
import rioxarray as rxr
#import geopandas as gpd
#import earthpy as et
#import earthpy.spatial as es
import earthpy.plot as ep
import matplotlib as mpl
#import fiona
import rasterio
import rasterio.mask
#from rasterio.plot import show
#from rasterio.warp import calculate_default_transform, reproject, Resampling
mpl.use('Agg')

# Define GeoTiff files location
img = ("SAMPLE/LOCATION")

# Define Index Output files location
out = ("SAMPLE/LOCATION")

for imgpath in glob.glob(os.path.join(img, '*.tif')):
    #print(imgpath)
    imgfile =  os.path.basename(imgpath)
    #print(imgfile)
    imgname = os.path.splitext(imgfile)[0]
    #print(imgname)
    
    output_path = imgname + "_output"
    
    try:
        os.mkdir(out, output_path)
    except WindowsError:
    # Handle the case where the target dir already exist.
        pass

    try:
        os.mkdir(os.path.join(out, output_path, "Index_GeoTIFFF"))
    except WindowsError:
        pass

    with rasterio.open(imgpath) as src:
        R = src.read(1)
    with rasterio.open(imgpath) as src:
        G = src.read(2)
    with rasterio.open(imgpath) as src:
        B = src.read(3)
    L = 0.5
        
    kwargs = src.meta
    kwargs.update(
        dtype=rasterio.float32,
        count = 1)
    #------------------------------------------------------------------------------------------------------------------------#    
    vndvi_index = (0.5268*((R ** -0.1294) * (G ** 0.3389) * (B ** -0.3118)))
    
    ep.plot_bands(vndvi_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Visible Normalized Difference Vegetation Index(vNDVI)\n" + imgname)

    plt.savefig(os.path.join(out, output_path,  imgname + " NDVI.png"), bbox_inches='tight')
    
    with rasterio.open(os.path.join(out, output_path, "Index_GeoTIFF", imgname + "NDVI.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, vndvi_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    vig_index = (G - R) / (G + R)

    ep.plot_bands(vig_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Vegetation Index Green(VIG)\n " + imgname)

    plt.savefig(os.path.join(out, output_path, imgname + " VIG.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, output_path, "Index_GeoTIFF", imgname + "VIG.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, vig_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    exg_index = 2 * G - R - B

    ep.plot_bands(exg_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Excess Green Index(ExG)\n " + imgname)

    plt.savefig(os.path.join(out, output_path, imgname + " ExG.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, output_path, "Index_GeoTIFF", imgname + "ExG.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, exg_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    gli_index = (2.0 * G - R - B) / (2.0 * G + R + B)

    ep.plot_bands(gli_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Green Leaf Index(GLI)\n " + imgname)

    plt.savefig(os.path.join(out, output_path, imgname + " GLI.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, output_path, "Index_GeoTIFF", imgname + "GLI.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, gli_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    mgrvi_index = (G ** 2.0 - R ** 2.0) / (G ** 2.0 + R ** 2.0)

    ep.plot_bands(mgrvi_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Modified Green Red Vegetation Index(MGRVI)\n " + imgname)

    plt.savefig(os.path.join(out, output_path, imgname + " MGRVI.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, output_path, "Index_GeoTIFF", imgname + "MGRVI.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, mgrvi_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#       
    colors = ['r', 'g', 'b']
    titles = [ imgname + " \n Red",  imgname + " \n Green",  imgname + " \n Blue",  imgname + " \n Near Infrared",  imgname + " \n Red Edge",  imgname + " \n Thermal"]
    
    ep.hist(src.values, 
            colors=colors, 
            title=titles, 
            cols=2)

    plt.savefig(os.path.join(out, output_path, imgname + " Histogram.png"), bbox_inches='tight')
    #------------------------------------------------------------------------------------------------------------------------#
    for saved_indexes in glob.glob(os.path.join(out, output_path, "Index_GeoTIFF", '*.tif')):
        indexes = rxr.open_rasterio(saved_indexes)

        colors = ['b', 'g', 'r', 'k', 'tomato', 'purple']
        titles = [ imgname + " \n Blue",  imgname + " \n Green",  imgname + " \n Red",  imgname + " \n Near Infrared",  imgname + " \n Red Edge",  imgname + " \n Thermal"]
        
        ep.hist(saved_indexes.values, 
            colors=colors, 
            title=titles, 
            cols=2)