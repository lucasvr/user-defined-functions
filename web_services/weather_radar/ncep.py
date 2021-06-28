#
# Get real-time weather velocity readings from NCEP
#
# See https://opengeo.ncep.noaa.gov/geoserver/www/index.html for a complete
# list of velocitys and available layers.
#
# The default color palette is available as PNG here:
# https://opengeo.ncep.noaa.gov/geoserver/styles/radial_velocity.png
#

from owslib.wms import WebMapService
import png

def dynamic_dataset():
    # tord: Chicago O'Hare International Airport, bvel: L3 Base Radial Velocity
    wms = WebMapService("https://opengeo.ncep.noaa.gov/geoserver/tord/ows?service=wms", version="1.3.0")
    bbox = wms["tord_bvel"].boundingBoxWGS84

    rdims = lib.getDims("RadialVelocity")
    img = wms.getmap(layers=["tord_bvel"], srs="EPSG:4316", bbox=bbox, size=rdims, format="image/png").read()

    # Create a look-up table to map (r,g,b) to a color index
    lut = {}
    velocity = lib.getData("RadialVelocity")
    rows = png.Reader(bytes=img).read()[2]
    for i, row in enumerate(rows):
        rgba = list(zip(*[row[i::4] for i in range(4)]))
        for j, (r,g,b,a) in enumerate(rgba):
            if not (r,g,b) in lut:
                velocity[i*len(rgba) + j] = lut[(r,g,b)] = len(lut)
            else:
                velocity[i*len(rgba) + j] = lut[(r,g,b)]

    # Export palette
    palette = lib.getData("Palette")
    reverse_lut = sorted([(v,k) for k,v in lut.items()], key=lambda kv: kv[0])
    for (i, rgb) in reverse_lut:
        palette[i*3 : i*3+3] = rgb
