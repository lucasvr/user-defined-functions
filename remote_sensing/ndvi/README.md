# Embed the Vegetation Index computation routine on HDF5

## Description

Computes the NDVI (Normalized Difference Vegetation Index) of Landsat scenes.
This UDF takes input from two existing datasets, `NIR` and `RED`, and creates
a dataset named `NDVI` whose contents are produced on-the-fly each time that
dataset is read.

## Data preparation

Assuming a reference HDF5 file named `landsat.h5` that includes two datasets
named `NIR` and `RED`, run the following command to create the user-defined
dataset:

```
hdf5-udf landsat.h5 ndvi.py
```

## Data consumption

The dataset can be read using the standard `h5dump` tool.

```
h5dump -d /NDVI landsat.h5
```
