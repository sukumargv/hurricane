from osgeo import gdal
import pyproj

ds = gdal.Open('route4_modified_1.tif')

# unravel GDAL affine transform parameters
c, a, b, f, d, e = ds.GetGeoTransform()


def pixel2coord(col, row):
    """Returns global coordinates to pixel center using base-0 raster index"""
    xp = a * col + b * row + a * 0.5 + b * 0.5 + c
    yp = d * col + e * row + d * 0.5 + e * 0.5 + f
    return xp, yp

cart_cord = pixel2coord(0, 0)
print cart_cord

# Converting coordinates from EPSG 4326 to 3857
inProj = pyproj.Proj(init='epsg:3857')
outProj = pyproj.Proj(init='epsg:4326')

lat, lon = pyproj.transform(inProj, outProj, cart_cord[0], cart_cord[1])
print lon, lat

