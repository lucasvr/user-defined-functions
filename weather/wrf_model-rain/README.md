# Aggregation of convective/non-convective precipitation with UDFs

## Description

Given a WRF output file, this UDF aggregates `RAINC` (the cumulative total
cumulus/convective precipitation) and `RAINNC` (cumulative total non-convective
precipitation) into a single `RAIN` dataset that's generated on-the-fly.

## Data preparation

Assuming a WRF output file named `wrfout.h5`, the following command creates
the `RAIN` dataset:

```
hdf5-udf wrfout.h5 rain.lua
```

## Data consumption

The UDF dataset can be read with standard tools such as `h5dump`:

```
h5dump -d /RAIN wrfout.h5
```
