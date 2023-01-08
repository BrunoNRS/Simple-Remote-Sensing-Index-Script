import os, rasterio, rasterio.mask
import rasterio.mask
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Image directory before processing
img_dir = (r"path/to/img")

# Output directory
out_dir = (r"output/directory")

# Specify output projection system
dst_crs = 'EPSG:32324'
crs_name = dst_crs.replace('EPSG:',"")

# Iterate through all images in the input folder
for img_file in os.listdir(img_dir):
    # Skip files that are not TIF images
    if not img_file.endswith('.tif'):
        continue
    img_name = os.path.splitext(os.path.basename(img_file))[0]
    print(img_name)

    # Save output imagery file name after reprojection
    repro_img_file = os.path.join(out_dir, f"{img_name}_{crs_name}.tif")
    print(repro_img_file)

    # Image reprojection process
    with rasterio.open(os.path.join(img_dir, img_file)) as img:
        transform, width, height = calculate_default_transform(img.crs, dst_crs, img.width, img.height, *img.bounds)
        kwargs = img.meta.copy()
        kwargs.update({'crs': dst_crs, 'transform': transform, 'width': width, 'height': height})
        with rasterio.open(repro_img_file, 'w', **kwargs) as dst:
            for i in range(1, img.count + 1):
                reproject(
                    source=rasterio.band(img, i),
                    destination=rasterio.band(dst, i),
                    src_transform=img.transform,
                    src_crs=img.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)