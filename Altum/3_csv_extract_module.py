import glob, csv, os
import numpy as np
from osgeo import gdal

# Image directory
img_dir = (r"path/to/images")

# Name of the dataset 
dataset_name = "dataset_01"

# No data value
no_data = 65535

# Function to calculate statistics for a given file
def get_value(file):
    # Open the file
    ds = gdal.Open(file)

    # Read the first band
    band = ds.GetRasterBand(1)
    data_nm = band.ReadAsArray().copy()  

    # Mask the data using the nodata value
    data = np.ma.masked_array(data_nm, mask=(data_nm == no_data))
    name = os.path.splitext(os.path.basename(file))[0]
    print(name)

    # Calculate various statistics
    mean = np.nanmean(data)
    var = np.nanvar(data)
    std = np.nanstd(data)
    min = np.nanmin(data)
    max = np.nanmax(data)

    return (name, mean, var, std, min, max)

# Get a list of all TIFF files in the image directory
inputs = glob.glob(os.path.join(img_dir, "*.tif"))

# Calculate statistics for each file
results = []
for input in inputs:
    results.append(get_value(input))

# Write the results to a CSV file
output = os.path.join(img_dir, dataset_name + ".csv")
with open(output, 'w') as fp_out:
    writer = csv.writer(fp_out, delimiter=",", lineterminator='\n')
    writer.writerow(["name", "mean", "var", "std", "min", "max",])
    writer.writerows(results)