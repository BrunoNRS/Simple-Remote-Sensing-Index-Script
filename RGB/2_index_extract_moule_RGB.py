import os, glob
from osgeo import gdal
import numpy as np
import earthpy.plot as ep
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('Agg')

# Images directory
img_dir = (r"path\to\images")

# Output directory
out_dir = (r"output\path")

# Nodata value for border
no_data = 255


def normalize(array):
    array_min, array_max = array.min(), array.max()
    return (array - array_min) / (array_max - array_min)

for img_path in glob.glob(os.path.join(img_dir, '*.tif')):
    img_name = os.path.splitext(os.path.basename(img_path))[0]
    print(img_name)
    
    def gen_hist(array, name, graph_title):
        ep.hist(array,
                figsize=(12, 6),
                title= graph_title + "\n " + img_name)
        plt.savefig(os.path.join(out_dir, name + " Histogram.png"), bbox_inches='tight')
        plt.clf()
    
    def gen_map(array, name, color_map, v_min, v_max, graph_title):
        ep.plot_bands(array,
                cmap=color_map,
                scale=False,
                vmin=v_min, vmax=v_max,
                title=graph_title + "\n" + img_name,)
        plt.savefig(os.path.join(out_dir, name+".png"), bbox_inches='tight')
        plt.clf()
    
    def write_to_file(array, name):
            rows, cols = array.shape
            driver = gdal.GetDriverByName("GTiff")
            out_file = os.path.join(out_dir, name+".tif")
            if os.path.exists(out_file):
                os.remove(out_file)
            outdata = driver.Create(out_file, cols, rows, 1, gdal.GDT_Float32)
            outdata.SetGeoTransform(img.GetGeoTransform())
            outdata.SetProjection(img.GetProjection())
            outdata.GetRasterBand(1).WriteArray(array)
            outdata.GetRasterBand(1).SetNoDataValue(no_data)

            info = outdata.GetGeoTransform()
            part = [i for i in outdata.GetProjection().split(",") if 'UNIT' in i]
            part = ",".join(part)
            if "metre" in part:
                info = info + ('m',)
            elif "degree" in part:
                info = info + ('d',)

            outdata.FlushCache()
            outdata = None
    
    img = gdal.Open (img_path)
    
    bands = [img.GetRasterBand(i).ReadAsArray() for i in range(1, img.RasterCount+1)]
    band = np.ma.masked_array(bands, mask=(bands == no_data))
    bands.append(band)
    
    normalized_bands = [normalize(band) for band in bands[:3]]
    R, G, B = normalized_bands
   
    N = normalize((bands[1] - 360.6) / 1.1941)
    
    L = 0.5
    
    #-------        
    NDVI = (N - R)/(N + R)
    ndvi_ttl = "Normalized Difference Vegetation Index"
    ndvi_abbr = "NDVI"
    
    gen_map(NDVI, img_name + "_" + ndvi_abbr, 'RdYlGn', -1, 1, ndvi_ttl + " - " + ndvi_abbr)
    gen_hist(NDVI, img_name + "_" + ndvi_abbr, ndvi_ttl + " - " + ndvi_abbr)
    write_to_file(NDVI, img_name + "_" + ndvi_abbr)
    print(ndvi_abbr + " OK!")
    #-------
    LAI_NDVI = 4.9 * (NDVI ** 2) + 0.1
    lai_ndvi_ttl = "Leaf Area Index"
    lai_ndvi_abbr = "LAI (NDVI)"
    
    gen_map(LAI_NDVI, img_name + "_" +  lai_ndvi_abbr, 'RdYlGn', -1, 1,  lai_ndvi_ttl + " - " +  lai_ndvi_abbr)
    gen_hist(LAI_NDVI, img_name + "_" +  lai_ndvi_abbr,  lai_ndvi_ttl + " - " +  lai_ndvi_abbr)
    write_to_file(LAI_NDVI, img_name + "_" +  lai_ndvi_abbr)
    print(lai_ndvi_abbr + " OK!")
    
    PAI_NDVI = 5 * (NDVI ** 2) + 1.3
    pai_ndvi_ttl = "Plant Area Index"
    pai_ndvi_abbr = "PAI NDVI"
    
    gen_map(PAI_NDVI, img_name + "_" +  pai_ndvi_abbr, 'RdYlGn', -1, 1,  pai_ndvi_ttl + " - " +  pai_ndvi_abbr)
    gen_hist(PAI_NDVI, img_name + "_" +  pai_ndvi_abbr,  pai_ndvi_ttl + " - " +  pai_ndvi_abbr)
    write_to_file(PAI_NDVI, img_name + "_" +  pai_ndvi_abbr)
    print(pai_ndvi_abbr + " OK!")
    
    SAVI = ((N - R) / (N + R + L)) * (1 + L)
    savi_ttl = "Soil-Adjusted Vegetation Index"
    savi_abbr = "SAVI"
    
    gen_map(SAVI, img_name + "_" + savi_abbr, 'RdYlGn', -1, 1, savi_ttl + " - " + savi_abbr)
    gen_hist(SAVI, img_name + "_" + savi_abbr, savi_ttl + " - " + savi_abbr)
    write_to_file(SAVI, img_name + "_" + savi_abbr)
    print(savi_abbr + " OK!")
    #-------
    VIG = (G - R) / (G + R)
    vig_ttl = "Vegetation Index Green"
    vig_abbr = "VIG"
    
    gen_map(VIG, img_name + "_" + vig_abbr, 'RdYlGn', -1, 1, vig_ttl + " - " + vig_abbr)
    gen_hist(VIG, img_name + "_" + vig_abbr, vig_ttl + " - " + vig_abbr)
    write_to_file(VIG, img_name + "_" + vig_abbr)
    print(vig_abbr + " OK!")
    #--------
    EXG = 2 * G - R - B
    exg_ttl = "Excess Green Index"
    exg_abbr = "ExG"
    
    gen_map(EXG, img_name + "_" + exg_abbr, 'RdYlGn', -1, 1, exg_ttl + " - " + exg_abbr)
    gen_hist(EXG, img_name + "_" + exg_abbr, exg_ttl + " - " + exg_abbr)
    write_to_file(EXG, img_name + "_" + exg_abbr)
    print(exg_abbr + " OK!")
    #-------
    GLI = (2.0 * G - R - B) / (2.0 * G + R + B)
    gli_ttl = "Green Leaf Index"
    gli_abbr = "GLI"
    
    gen_map(GLI, img_name + "_" + gli_abbr, 'RdYlGn', -1, 1, gli_ttl + " - " + gli_abbr)
    gen_hist(GLI, img_name + "_" + gli_abbr, gli_ttl + " - " + gli_abbr)
    write_to_file(GLI, img_name + "_" + gli_abbr)
    print(gli_abbr + " OK!")
    #-------
    MGRVI= (G ** 2.0 - R ** 2.0) / (G ** 2.0 + R ** 2.0)
    mgrvi_ttl = "Modified Green Red Vegetation Index"
    mgrvi_abbr = "MGRVI"
    
    gen_map(MGRVI, img_name + "_" + mgrvi_abbr, 'RdYlGn', -1, 1, mgrvi_ttl + " - " + mgrvi_abbr)
    gen_hist(MGRVI, img_name + "_" + mgrvi_abbr, mgrvi_ttl + " - " + mgrvi_abbr)
    write_to_file(MGRVI, img_name + "_" + mgrvi_abbr)
    print(mgrvi_abbr + " OK!")
    #-------
    NDWI = (G - N) / (G + N)
    ndwi_ttl = "Normalized Difference Water Index"
    ndwi_abbr = "NDWI"
    
    gen_map(NDWI, img_name + "_" + ndwi_abbr, 'RdYlGn', -1, 1, ndwi_ttl + " - " + ndwi_abbr)
    gen_hist(NDWI, img_name + "_" + ndwi_abbr, ndwi_ttl + " - " + ndwi_abbr)
    write_to_file(NDWI, img_name + "_" + ndwi_abbr)
    print(ndwi_abbr + " OK!")
    #-------