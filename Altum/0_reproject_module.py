import os
import rasterio
import rasterio.mask
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Specify output projection system
dst_crs = 'EPSG:32324'

# Input image file name before transformation
input_img_file = "path/to/sample_file.tif"


crsnumb =  dst_crs.replace('EPSG:',"")

imgfile =  os.path.basename(input_img_file)
imgname = os.path.splitext(imgfile)[0]

# Save output imagery file name after transformation
transformed_img_file = os.path.join(imgname + "_" + crsnumb + ".tif")

# Image reprojection process
with rasterio.open(input_img_file) as img:
    transform, width, height = calculate_default_transform(img.crs, dst_crs, img.width, img.height, *img.bounds)
    kwargs = img.meta.copy()
    kwargs.update({'crs': dst_crs, 'transform': transform, 'width': width, 'height': height})
    with rasterio.open(transformed_img_file, 'w', **kwargs) as dst:
        for i in range(1, img.count + 1):
            reproject(
                source=rasterio.band(img, i),
                destination=rasterio.band(dst, i),
                src_transform=img.transform,
                src_crs=img.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest)

