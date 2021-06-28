# Virtualization of GeoTIFF files through HDF5-UDF

from tifffile import TiffFile

def dynamic_dataset():
    output = lib.getData("geotiff")
    input = TiffFile("sample.tif")
    image = input.pages[0].asarray().flatten()
    n = image.shape[0]
    output[0:n] = image[:]
