import glob,numpy, csv, os
from osgeo import gdal

#Input image directory
img = "/path/to/images"

data_set_name = os.path.basename(img)

nodata = 65535

def getvalue(file):
    ds = gdal.Open(file)
    band = ds.GetRasterBand(1)
    data_nm = band.ReadAsArray()
    data = numpy.ma.masked_array(data_nm, mask=(data_nm== nodata))
    mean = numpy.nanmean(data)
    namee = os.path.basename(file)
    name = os.path.splitext(namee)[0]
    print(name)
    var = numpy.nanvar(data)
    std = numpy.nanstd(data)
    min = numpy.nanmin(data)
    max = numpy.nanmax(data)
    return(name,mean,var,std,min,max)

inputs = glob.glob(os.path.join(img,"*.tif"))

results = []
for input in inputs:
    results.append((input,)+getvalue(input))

output = os.path.join(img, data_set_name + ".csv")# (3) modify output here
with open(output, 'w') as fp_out:
    writer = csv.writer(fp_out, delimiter=",", lineterminator='\n')
    writer.writerow(["filename","name","mean","var","std","min","max"])
    writer.writerows(results)
