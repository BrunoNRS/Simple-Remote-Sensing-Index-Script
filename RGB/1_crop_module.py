import glob, os, fiona, rasterio,rasterio.mask

# Image and shapefile directories
img_dir = (r"path/to/img")
shp_dir = (r"path/to/shp")

# Output directory
out_dir = (r"out/path")

# Nodata value for border
no_data = 255

# Iterate through shapefiles
for shp_path in glob.glob(os.path.join(shp_dir, "*.shp")):
    # Get shapefile name
    shp_name = os.path.splitext(os.path.basename(shp_path))[0]
    print(shp_name)

    # Read shapefile and extract geometry data
    with fiona.open(shp_path, "r") as shp:
        shapes = [feature["geometry"] for feature in shp]
    # Iterate through images
    for img_path in glob.glob(os.path.join(img_dir, "*.tif")):
        # Get image name
        img_name = os.path.splitext(os.path.basename(img_path))[0]
        print(img_name)
        
        # Read image and mask using shape geometry and nodata value
        with rasterio.open(img_path) as src:
            out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True, nodata=no_data)
            out_meta = src.meta
        
        # Update metadata for output image
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})
        
        # Save masked image
        out_path = os.path.join(out_dir, f"{img_name}_{shp_name}.tif")
        with rasterio.open(out_path, "w", **out_meta) as dest:
            dest.write(out_image)