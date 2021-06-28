#!/usr/bin/env python3

import xarray as xr

def dynamic_dataset():
    data = lib.getData("PressureLevels")
    dims = lib.getDims("PressureLevels")

    ds = xr.open_dataset("era5-levels-members.grib", engine="cfgrib")
    data[0:dims[0] * dims[1]] = ds["z"][-1,-1,-1].values.flatten()