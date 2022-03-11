"""
@author: Bruno do Nascimento (bruno.do.nrs@gmail.com)
"""
# WARNING: This script is designed for rgb cameras
# Ver 2.5

#from builtins import WindowsError
import glob, os
import matplotlib.pyplot as plt
import numpy as np
import rioxarray as rxr
import earthpy.plot as ep
import matplotlib as mpl
import rasterio
import rasterio.mask
mpl.use('Agg')

# Define GeoTiff files location
img = ("SAMPLE/LOCATION")

# Define Index Output files location
out = ("SAMPLE/LOCATION")

for imgpath in glob.glob(os.path.join(img, '*.tif')):
    imgfile =  os.path.basename(imgpath)
    imgname = os.path.splitext(imgfile)[0]
    
    raster = rasterio.open(imgpath)

    def normalize(array):
        array_min, array_max = array.min(), array.max()
        return (array - array_min) / (array_max - array_min)

    Rnn = raster.read(1)
    Gnn = raster.read(2)
    Bnn = raster.read(3)
    
    R = normalize(Rnn)
    G = normalize(Gnn)
    B = normalize(Bnn)

    ImgSet = rxr.open_rasterio(imgpath)

    L = 0.5
        
    kwargs = raster.meta
    kwargs.update(
        dtype=rasterio.float32,
        count = 1)
    #------------------------------------------------------------------------------------------------------------------------#    
    vndvi_index = (0.5268*((R ** -0.1294) * (G ** 0.3389) * (B ** -0.3118)))
    vndvi_index[vndvi_index == 0] = np.nan

    ep.plot_bands(vndvi_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Visible Normalized Difference Vegetation Index(vNDVI)\n" + imgname)

    plt.savefig(os.path.join(out, imgname + " vNDVI.png"), bbox_inches='tight')

    ep.hist(vndvi_index,
            figsize=(12, 6),
            title="Visible Normalized Difference Vegetation Index(NDVI) Histogram\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " vNDVI Histogram.png"), bbox_inches='tight')
    
    with rasterio.open(os.path.join(out, imgname + " vNDVI.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, vndvi_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    vig_index = (G - R) / (G + R)
    vig_index[vndvi_index == 0] = np.nan

    ep.plot_bands(vig_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Vegetation Index Green(VIG)\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " VIG.png"), bbox_inches='tight')

    ep.hist(vig_index,
            figsize=(12, 6),
            title="Vegetation Index Green(VIG) Histogram\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " VIG Histogram.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, imgname + " VIG.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, vig_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    exg_index = 2 * G - R - B
    exg_index[vndvi_index == 0] = np.nan

    ep.plot_bands(exg_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Excess Green Index(ExG)\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " ExG.png"), bbox_inches='tight')

    ep.hist(exg_index,
            figsize=(12, 6),
            title="Excess Green Index(ExG) Histogram\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " ExG Histogram.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, imgname + " ExG.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, exg_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    gli_index = (2.0 * G - R - B) / (2.0 * G + R + B)
    gli_index[vndvi_index == 0] = np.nan

    ep.plot_bands(gli_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Green Leaf Index(GLI)\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " GLI.png"), bbox_inches='tight')

    ep.hist(exg_index,
            figsize=(12, 6),
            title="Green Leaf Index(GLI) Histogram\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " GLI Histogram.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, imgname + " GLI.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, gli_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#        
    mgrvi_index = (G ** 2.0 - R ** 2.0) / (G ** 2.0 + R ** 2.0)
    mgrvi_index[vndvi_index == 0] = np.nan

    ep.plot_bands(mgrvi_index,
                  cmap='RdYlGn',
                  scale=False,
                  vmin=0, vmax=1,
                  title="Modified Green Red Vegetation Index(MGRVI)\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " MGRVI.png"), bbox_inches='tight')

    ep.hist(exg_index,
            figsize=(12, 6),
            title="Modified Green Red Vegetation Index(MGRVI) Histogram\n " + imgname)

    plt.savefig(os.path.join(out, imgname + " MGRVI Histogram.png"), bbox_inches='tight')

    with rasterio.open(os.path.join(out, imgname + " MGRVI.tif"), 'w', **kwargs) as dst:
            dst.write_band(1, mgrvi_index.astype(rasterio.float32))
    #------------------------------------------------------------------------------------------------------------------------#
    colors = ['r', 'g', 'b']
    titles = [ imgname + " \n Red",  imgname + " \n Green",  imgname + " \n Blue"]
    
    ep.hist(ImgSet.values, 
            colors=colors, 
            title=titles, 
            cols=2)

    plt.savefig(os.path.join(out, imgname + " Histogram.png"), bbox_inches='tight')
