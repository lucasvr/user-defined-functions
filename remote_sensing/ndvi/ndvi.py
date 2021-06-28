def dynamic_dataset():
    nir, red, ndvi = lib.getData("NIR"), lib.getData("RED"), lib.getData("NDVI")
    size = lib.getDims("NIR")
    for i in range(size[0] * size[1]):
        ndvi[i] = (nir[i] - red[i]) / (nir[i] + red[i])
