from osgeo import gdal
import pyproj


def pixels_to_coordinates(route_tif, center_x, center_y):
    # load in the route image
    ds = gdal.Open(route_tif)

    # unravel GDAL affine transform parameters
    c, a, b, f, d, e = ds.GetGeoTransform()

    def pixel2coord(col, row):
        # Returns global coordinates to pixel center using base-0 raster index
        xp = a * col + b * row + a * 0.5 + b * 0.5 + c
        yp = d * col + e * row + d * 0.5 + e * 0.5 + f
        return xp, yp

    cart_cord = pixel2coord(center_x, center_y)

    # Converting coordinates from EPSG 3857 to 4326
    inProj = pyproj.Proj(init='epsg:3857')
    outProj = pyproj.Proj(init='epsg:4326')

    coordinates = pyproj.transform(inProj, outProj, cart_cord[0], cart_cord[1])
    local_dict = {'lat': coordinates[1], 'lon': coordinates[0]}
    return local_dict


route_file = "route4_modified.tif"

pixels_to_coordinates(route_file, 1, 1)




