import os, glob
from osgeo import gdal
import numpy as np
import earthpy.plot as ep
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('Agg')

in_path = "D:\PARA_PROCESSAR\Testes"
out_path = "D:\PARA_PROCESSAR\Testes\out"

def normalize(array):
    array_min, array_max = array.min(), array.max()
    return (array - array_min) / (array_max - array_min)

def write_to_file(array, name):
        rows, cols = array.shape
        driver = gdal.GetDriverByName("GTiff")
        out_file = os.path.join(out_path, name+".tif")
        if os.path.exists(out_file):
            os.remove(out_file)
        outdata = driver.Create(out_file, cols, rows, 1, gdal.GDT_Float32)
        outdata.SetGeoTransform(img.GetGeoTransform())
        outdata.SetProjection(img.GetProjection())
        outdata.GetRasterBand(1).WriteArray(array)
        outdata.GetRasterBand(1).SetNoDataValue(nodata)

        info = outdata.GetGeoTransform()
        part = [i for i in outdata.GetProjection().split(",") if 'UNIT' in i]
        part = ",".join(part)
        if "metre" in part:
            info = info + ('m',)
        elif "degree" in part:
            info = info + ('d',)

        outdata.FlushCache()
        outdata = None

nodata = (65535)

for imgpath in glob.glob(os.path.join(in_path, '*.tif')):
    imgfile =  os.path.basename(imgpath)
    imgname = os.path.splitext(imgfile)[0]

    img = gdal.Open (imgpath)

    Bnm = np.array(img.GetRasterBand(1).ReadAsArray())
    Gnm = np.array(img.GetRasterBand(2).ReadAsArray())
    Rnm = np.array(img.GetRasterBand(3).ReadAsArray())
    Nnm = np.array(img.GetRasterBand(4).ReadAsArray())
    T = np.array(img.GetRasterBand(6).ReadAsArray())/ 100 -  273.15

    Bm = np.ma.masked_array(Bnm, mask=(Bnm== nodata))
    Gm = np.ma.masked_array(Gnm, mask=(Gnm== nodata))
    Rm = np.ma.masked_array(Rnm, mask=(Rnm== nodata)) 
    Nm = np.ma.masked_array(Nnm, mask=(Nnm== nodata)) 

    B = normalize(Bm)
    G = normalize(Gm)
    R = normalize(Rm)
    N = normalize(Nm)

    L = 0.5

    NDVI = (N - R)/(N + R)

    ep.hist(NDVI,
            figsize=(12, 6),
            title="Normalized Difference Vegetation Index(NDVI) Histogram\n " + imgname)

    plt.savefig(os.path.join(out_path, imgname + " NDVI Histogram.png"), bbox_inches='tight')

    write_to_file(NDVI, imgname + " NDVI")
    print("NDVI OK")


    SAVI = ((N - R) / (N + R + L)) * (1 + L)

    ep.hist(SAVI,
            figsize=(12, 6),
            title="Soil-Adjusted Vegetation Index(SAVI) Histogram\n " + imgname)

    plt.savefig(os.path.join(out_path, imgname + " SAVI Histogram.png"), bbox_inches='tight')

    write_to_file(SAVI, imgname + " SAVI")
    print("SAVI OK")

    VIG = (G - R) / (G + R)

    ep.hist(VIG,
            figsize=(12, 6),
            title="Vegetation Index Green(VIG) Histogram\n " + imgname)

    plt.savefig(os.path.join(out_path, imgname + " VIG Histogram.png"), bbox_inches='tight')

    write_to_file(VIG, imgname + " VIG")
    print("VIG OK")

    EXG = 2 * G - R - B

    ep.hist(EXG,
            figsize=(12, 6),
            title="Excess Green Index(ExG) Histogram\n " + imgname)

    plt.savefig(os.path.join(out_path, imgname + " ExG Histogram.png"), bbox_inches='tight')

    write_to_file(EXG, imgname + " EXG")
    print("EXG OK")

    GLI = (2.0 * G - R - B) / (2.0 * G + R + B)

    ep.hist(GLI,
            figsize=(12, 6),
            title="Green Leaf Index(GLI) Histogram\n " + imgname)

    plt.savefig(os.path.join(out_path, imgname + " GLI Histogram.png"), bbox_inches='tight')

    write_to_file(GLI, imgname + " GLI")
    print("GLI OK")

    MGRVI= (G ** 2.0 - R ** 2.0) / (G ** 2.0 + R ** 2.0)

    ep.hist(MGRVI,
            figsize=(12, 6),
            title="Modified Green Red Vegetation Index(MGRVI) Histogram\n " + imgname)

    plt.savefig(os.path.join(out_path, imgname + " MGRVI Histogram.png"), bbox_inches='tight')

    write_to_file(MGRVI, imgname + " MGRVI")
    print("MGVRI OK")

    NDWI = (G - N) / (G + N)

    ep.hist(NDWI,
            figsize=(12, 6),
            title="Normalized Difference Water Index(NDWI) Histogram\n " + imgname)

    plt.savefig(os.path.join(out_path, imgname + " NDWI Histogram.png"), bbox_inches='tight')

    write_to_file(NDWI, imgname + " NDWI")
    print("NDWI OK")
