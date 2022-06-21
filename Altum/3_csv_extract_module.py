import glob,numpy, csv, os
from osgeo import gdal

data_set_name = "65-Orthomosaic-Uva de suco_rgb_20170515"
img = "D:/Karine/Processar python/20170515_0.4"

def getvalue(file):
    ds = gdal.Open(file)
    band = ds.GetRasterBand(1)
    data = band.ReadAsArray()
    nodata = band.GetNoDataValue()
    # if nodata is not None:
    #     data = numpy.ma.masked_equal(data,nodata,numpy.isnan(data))
    mean = numpy.nanmean(data)
    namee = os.path.basename(file)
    name = os.path.splitext(namee)[0]
    print(name)
    var = numpy.nanvar(data)
    std = numpy.nanstd(data)
    min = numpy.nanmin(data)
    max = numpy.nanmax(data)
    return(name,mean,var,std,min,max)

# # Define inputs folder
# root = Tkinter.Tk()
# inputs = tkFileDialog.askdirectory()    
# root.destroy()
# print(inputs+" selecionado.")

# if (inputs == None): 
# 	sair = raw_input('Pasta de entrada nao selecionada.\nPressione enter para sair.\n')
# 	sys.exit()

inputs = glob.glob(os.path.join(img,"*.tif"))

results = []
for input in inputs:
    results.append((input,)+getvalue(input))

output = os.path.join(img, data_set_name + ".csv")# (3) modify output here
with open(output, 'w') as fp_out:
    writer = csv.writer(fp_out, delimiter=",", lineterminator='\n')
    writer.writerow(["filename","name","mean","var","std","min","max"])
    writer.writerows(results)