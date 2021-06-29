# Post-processing of WRF model files with UDFs

## Description

Given a WRF output file, this UDF produces, on-the-fly, (1) the wind chill,
(2) heat index, and (3) wind speed.

## Data preparation

Assuming a WRF output file named `wrfout.h5`, the following command creates
three UDF datasets named `wind_chill`, `heat_index`, and `wind_speed`:

```
hdf5-udf wrfout.h5 wind_chill.lua \
  wind_speed:1x99x99:float \
  wind_chill:1x99x99:float \
  heat_index:1x99x99:float
```

Note that three different datasets are created using a single Lua script.

## Data consumption

The UDF dataset can be read with standard tools such as `h5dump`:

```
h5dump -d /wind_speed wrfout.h5
h5dump -d /wind_chill wrfout.h5
h5dump -d /heat_index wrfout.h5
```

## Acknowledgements

The original code, written in Fortran, has been written and contributed by
Campbell Watson (@camelstation). Translation to Lua by Thiago Silva das
Mercês (@Thiago-SMerces).
