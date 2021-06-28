# Virtualization of GeoTIFF files through HDF5

## Description

Shows how to read a GeoTIFF data band through HDF5.

## Data preparation

Run the code below to obtain the parameters needed to create the UDF dataset.
The script takes input from a GeoTIFF file named `sample.tif` and outputs a
dataset named `geotiff` to an existing `reference.h5` HDF5 file. The script
depends on two Python packages which you can install with
`pip install tifffile imagecodecs`.

```
from tifffile import TiffFile
import sys

if __name__ == "__main__":
    geotiff_file = "sample.tif"
    hdf5_file = "reference.h5"
    udf_file = "udf-geotiff.py"
    udf_dataset = "geotiff"

    tif = TiffFile(geotiff_file)
    page = tif.pages[0]
    print("hdf5-udf {} {} --overwrite {}:{}:{}".format(
        hdf5_file,
        udf_file,
        udf_dataset,
        "x".join([str(dim) for dim in page.shape]),
        page.dtype))
```

## Data consumption

The UDF dataset can be read with standard GIS tools such as QGIS and SAGA-GIS.
It is also possible to output the data with `h5dump`:

```
h5dump -d /geotiff reference.h5
```
