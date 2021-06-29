def dynamic_dataset():
    import rioxarray as rxr
    data, dims = lib.getData("EPSG_4326"), lib.getDims("EPSG_4326")
    reference = rxr.open_rasterio("mosaic.tif")
    reprojected = reference.rio.reproject("EPSG:4326").data.flatten()
    data[0:dims[0]*dims[1]*dims[2]] = reprojected
