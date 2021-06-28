# Retrieve remote files using plain HTTP GET through HDF5

## Description

Retrieves an image (in PPM format) from a server on the internet by calling
a plain HTTP GET command. The image is converted into an HDF5 dataset; valid
pixels of the original image are converted into `1`s and transparent pixels
are converted into `0`s.

## Data preparation

Assuming a reference HDF5 file named `sample.h5`, please run the following
command to create the user-defined dataset:

```
hdf5-udf sample.h5 http_get.cpp Tux:60x80:int32
```

## Data consumption

The dataset can be read using the standard `h5dump` tool or the
[readh5 utility](https://github.com/lucasvr/hdf5-udf/blob/default/examples/readh5.cpp)
that comes with the HDF5-UDF distribution.

```
xterm -fa 'Monospace' -fs 4 -geometry 120x80 -e 'readh5 sample.h5 Tux; read'
```

![](screenshot.png)
