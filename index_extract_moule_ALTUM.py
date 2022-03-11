"""
@author: Bruno do Nascimento (bruno.do.nrs@gmail.com)
"""
# WARNING: This script is designed for the micasense altum multiespectral camera
# Ver 2.5
#from builtins import WindowsError
import os, glob
import matplotlib.pyplot as plt
import numpy as np
import earthpy.plot as ep
import matplotlib as mpl
import rasterio
import rasterio.mask
import rioxarray as rxr
mpl.use('Agg')

# Define GeoTiff files location
img = "/home/bruno/Projects/Orto Fotos/Projeto Uva/Plant"

# Define Index Output files location
out = "/home/bruno/Projects/Orto Fotos/Projeto Uva/Plant/Output"

for imgpath in glob.glob(os.path.join(img, '*.tif')):
    imgfile =  os.path.basename(imgpath)
    imgname = os.path.splitext(imgfile)[0]
    
    output_path = imgname + "_output"
    
    raster = rasterio.open(imgpath)

    def normalize(array):
        array_min, array_max = array.min(), array.max()
        return (array - array_min) / (array_max - array_min)

    Bnn = raster.read(1)
    Gnn = raster.read(2)
    Rnn = raster.read(3)
    Nnn = raster.read(4)
    
    B = normalize(Bnn)
    G = normalize(Gnn)
    R = normalize(Rnn)
    N = normalize(Nnn)

    T = raster.read(6) / 100 -  273.15
    L = 0.5
    
    ImgSet = rxr.open_rasterio(imgpath)

    kwargs = raster.meta
    kwargs.update(
        dtype=rasterio.float32,
        count = 1)
    
    #------------------------------------------------------------------------------------------------------------------------#
    ndvi_index = (N - R)/(N + R)
    ndvi_index[ndvi_index == 0] = np.nan

    ep.plot_bands(ndvi_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Normalized Difference Vegetation Index(NDVI)\n" + imgname)

    plt.savefig(os.path.join(out, imgname + " NDVI.png"), bbox_inches='tight')

    ep.hist(ndvi_index,
            figsize=(12, 6),
            title="Normalized Difference Vegetation Index(NDVI) Histogram\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " NDVI Histogram.png"), bbox_inches='tight')
    
    with rasterio.open(os.path.join(out, imgname + " NDVI.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, ndvi_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    savi_index = ((N - R) / (N + R + L)) * (1 + L)
    savi_index[savi_index == 0] = np.nan

    ep.plot_bands(savi_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Soil-Adjusted Vegetation Index(SAVI)\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " SAVI.png"), bbox_inches='tight')

    ep.hist(savi_index,
            figsize=(12, 6),
            title="Soil-Adjusted Vegetation Index(SAVI) Histogram\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " SAVI Histogram.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, imgname + " SAVI.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, savi_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    vig_index = (G - R) / (G + R)
    vig_index[vig_index == 0] = np.nan

    ep.plot_bands(vig_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Vegetation Index Green(VIG)\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " VIG.png"), bbox_inches='tight')

    ep.hist(savi_index,
            figsize=(12, 6),
            title="Vegetation Index Green(VIG) Histogram\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " VIG Histogram.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, imgname + " VIG.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, vig_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    exg_index = 2 * G - R - B 
    exg_index[exg_index == 0] = np.nan 

    ep.plot_bands(exg_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Excess Green Index(ExG)\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " ExG.png"), bbox_inches='tight')

    ep.hist(savi_index,
            figsize=(12, 6),
            title="Excess Green Index(ExG) Histogram\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " ExG Histogram.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, imgname + " ExG.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, exg_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    gli_index = (2.0 * G - R - B) / (2.0 * G + R + B)
    gli_index[gli_index == 0] = np.nan

    ep.plot_bands(gli_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Green Leaf Index(GLI)\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " GLI.png"), bbox_inches='tight')

    ep.hist(gli_index,
            figsize=(12, 6),
            title="Green Leaf Index(GLI) Histogram\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " GLI Histogram.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, imgname + " GLI.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, gli_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    mgrvi_index = (G ** 2.0 - R ** 2.0) / (G ** 2.0 + R ** 2.0)
    mgrvi_index[mgrvi_index == 0] = np.nan

    ep.plot_bands(mgrvi_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Modified Green Red Vegetation Index(MGRVI)\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " MGRVI.png"), bbox_inches='tight')

    ep.hist(mgrvi_index,
            figsize=(12, 6),
            title="Modified Green Red Vegetation Index(MGRVI) Histogram\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " MGRVI Histogram.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, imgname + " MGRVI.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, mgrvi_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    ndwi_index = (G - N) / (G + N)
    ndwi_index[ndwi_index == 0] = np.nan

    ep.plot_bands(ndwi_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Normalized Difference Water Index(NDWI)\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " NDWI.png"), bbox_inches='tight')

    ep.hist(ndwi_index,
            figsize=(12, 6),
            title="Normalized Difference Water Index(NDWI) Histogram\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " NDWI Histogram.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, imgname + " NDWI.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, ndwi_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#
    colors = ['b', 'g', 'r', 'k', 'tomato', 'purple']
    titles = [ imgname + " \n Blue",  imgname + " \n Green",  imgname + " \n Red",  imgname + " \n Near Infrared",  imgname + " \n Red Edge",  imgname + " \n Thermal"]

    ep.hist(ImgSet.values,
            colors=colors, 
            title=titles, 
            cols=2)

    plt.savefig(os.path.join(out, imgname + " Histogram.png"), bbox_inches='tight')
    #------------------------------------------------------------------------------------------------------------------------#
    ep.plot_bands(T,
                  title=imgname + " \n Thermal",
                  cbar=True,
                  cmap='CMRmap',
                  scale=False,
                  vmin=15, vmax=50)

    plt.savefig(os.path.join(out, imgname + " Thermal.png"), bbox_inches='tight')
