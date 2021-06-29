# Dataset reprojection through User-Defined Functions

## Description

Shows how to reproject a dataset to Lat-Lon (EPSG:4326) using
user-defined functions.

## Data preparation

This example relies on the [rioxarray](https://pypi.org/project/rioxarray/)
Python package, which is best installed using Conda:

```
conda install -c conda-forge rioxarray
```

Because reprojection potentially changes the shape of the original dataset,
the output dataset dimensions need to be identified and provided to HDF5-UDF.
The following piece of code will give you the required command line to produce
the UDF dataset. It is assumed that the input file is named `mosaic.tif`,
containing a dataset in a coordinate reference system other than EPSG:4326,
and that a target HDF5 file named `target.h5` exists.

```
import rioxarray as rxr

mosaic = rxr.open_rasterio("mosaic.tif")
reprojected = mosaic.rio.reproject("EPSG:4326")
dims = "x".join([str(x) for x in reprojected.shape])
print("hdf5-udf target.h5 reproject.py EPSG_4326:{}:uint8".format(dims))
```

## Data consumption

The UDF dataset can be read with standard GIS tools such as QGIS and SAGA-GIS.
It is also possible to output the data with `h5dump`:

```
h5dump -d /EPSG_4326 target.h5
```
