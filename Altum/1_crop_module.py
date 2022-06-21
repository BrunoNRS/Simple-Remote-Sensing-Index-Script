import glob, os
import fiona
import rasterio
import rasterio.mask
import numpy as np

img = "D:/PARA_PROCESSAR/Testes/20200903_uva_1030_altum_orto_pixel20cm.tif"
shp_path = "D:/PARA_PROCESSAR"
out_path = "D:/PARA_PROCESSAR/Testes"
no_data = 65535

for shapepath in glob.glob(os.path.join(shp_path, "*.shp")):
    # try:
    #     os.mkdir("Crop")
    # except WindowsError:
    # Handle the case where the target dir already exist.
        #pass
    print(shapepath)
    shapefile =  os.path.basename(shapepath)
    # print(shapefile)
    shapename = os.path.splitext(shapefile)[0]
    print(shapename)
   
    # Read Shape file
    with fiona.open(shapepath, "r") as shapepath:
        shapes = [feature["geometry"] for feature in shapepath]

    # Read imagery file
    with rasterio.open(img) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True, nodata = no_data)
        out_meta = src.meta

    # Save clipped imagery
    out_meta.update({"driver": "GTiff",
                      "height": out_image.shape[1],
                      "width": out_image.shape[2],
                      "transform": out_transform})

    with rasterio.open(os.path.join(out_path, shapename + '.tif'), "w", **out_meta) as dest:
        dest.write(out_image)
