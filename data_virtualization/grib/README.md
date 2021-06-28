# Virtualization of GRIB files through HDF5

## Description

Shows how to read a GRIB data variable through HDF5.

This example uses ECMWF's [cfgrib](https://github.com/ecmwf/cfgrib)
parser to parse a GRIB file, extract its data variables, and export
one of its data variables as an HDF5 dataset.

## Data preparation

This example uses an [ERA5 on pressure levels sample](
http://download.ecmwf.int/test-data/cfgrib/era5-levels-members.grib)
from ECMWF. The UDF depends on two packages that are easier installed
through Conda:

```
conda install -c conda-forge cfgrib
conda install -c conda-forge xarray
```

Assuming an existing reference HDF5 file named `era5.h5`, the UDF can
be compiled and attached to that HDF5 file with the following command:

```
hdf5-udf era5.h5 udf-grib.py PressureLevels:61x120:float
```

## Data consumption

The UDF dataset can be read with standard GIS tools such as QGIS and SAGA-GIS.
It is also possible to output the data with `h5dump`:

```
h5dump -d /PressureLevels era5.h5
```
