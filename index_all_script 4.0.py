import glob, os, shutil
import matplotlib.pyplot as plt
import numpy as np
import rioxarray as rxr
import geopandas as gpd
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import matplotlib as mpl
mpl.use('Agg')

folder = ("D:\Embrapa\Gerais")

for file in glob.glob('*.tif'):
    new_dir = file.rsplit('.', 1)[0]
    try:
        os.mkdir(os.path.join(folder, new_dir + "_output"))
    except WindowsError:
    # Handle the case where the target dir already exist.
        pass
    print(file)
    orto = rxr.open_rasterio(file)
    filename = os.path.splitext(file)[0]
    output_path = filename + "_output"
    
    B = orto[0]
    G = orto[1]
    R = orto[2]
    N = orto[3]
    T = orto[5] / 100 - 273.15
    L = 0.5
    
    for name in glob.glob(file):
        orto_ndvi = es.normalized_diff(N, R)

        ep.plot_bands(orto_ndvi,
                      cmap='RdYlGn',
                      scale=False,
                      vmin=0, vmax=1,
                      title="Normalized Difference Vegetation Index(NDVI)\n" + filename)

        plt.savefig(os.path.join(output_path, filename + " NDVI.png"), bbox_inches='tight')
        
        orto_savi = ((N - R) / (N + R + L)) * (1 + L)

        ep.plot_bands(orto_savi,
                      cmap='RdYlGn',
                      scale=False,
                      vmin=0, vmax=1,
                      title="Soil-Adjusted Vegetation Index(SAVI)\n " + filename)

        plt.savefig(os.path.join(output_path, filename + " SAVI.png"), bbox_inches='tight')

        orto_vig = (G - R) / (G + R)

        ep.plot_bands(orto_vig,
                      cmap='RdYlGn',
                      scale=False,
                      vmin=0, vmax=1,
                      title="Vegetation Index Green(VIG)\n " + filename)

        plt.savefig(os.path.join(output_path, filename + " VIG.png"), bbox_inches='tight')

        orto_exg = 2 * G - R - B

        ep.plot_bands(orto_exg,
                      cmap='RdYlGn',
                      scale=False,
                      vmin=0, vmax=1,
                      title="Excess Green Index(ExG)\n " + filename)

        plt.savefig(os.path.join(output_path, filename + " ExG.png"), bbox_inches='tight')

        orto_gli = (2.0 * G - R - B) / (2.0 * G + R + B)

        ep.plot_bands(orto_gli,
                      cmap='RdYlGn',
                      scale=False,
                      vmin=0, vmax=1,
                      title="Green Leaf Index(GLI)\n " + filename)

        plt.savefig(os.path.join(output_path, filename + " GLI.png"), bbox_inches='tight')

        orto_mgrvi = (G ** 2.0 - R ** 2.0) / (G ** 2.0 + R ** 2.0)

        ep.plot_bands(orto_mgrvi,
                      cmap='RdYlGn',
                      scale=False,
                      vmin=0, vmax=1,
                      title="Modified Green Red Vegetation Index(MGRVI)\n " + filename)

        plt.savefig(os.path.join(output_path, filename + " MGRVI.png"), bbox_inches='tight')

        orto_ndwi = (G - N) / (G + N)

        ep.plot_bands(orto_ndwi,
                      cmap='RdYlGn',
                      scale=False,
                      vmin=0, vmax=1,
                      title="Normalized Difference Water Index(NDWI)\n " + filename)

        plt.savefig(os.path.join(output_path, filename + " NDWI.png"), bbox_inches='tight')

        colors = ['b', 'g', 'r', 'k', 'tomato', 'purple']
        titles = [ filename + " \n Blue",  filename + " \n Green",  filename + " \n Red",  filename + " \n Near Infrared",  filename + " \n Red Edge",  filename + " \n Thermal"]

        ep.hist(orto.values, 
                colors=colors, 
                title=titles, 
                cols=2)

        plt.savefig(os.path.join(output_path, filename + " Histogram.png"), bbox_inches='tight')

        ep.plot_bands(T,
                      title=filename + " \n Thermal",
                      cbar=True,
                      cmap='CMRmap',
                      scale=False,
                      vmin=15, vmax=50)

        plt.savefig(os.path.join(output_path, filename + " Thermal.png"), bbox_inches='tight')

        
    
     
        
        