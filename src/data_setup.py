import numpy as np

# For loading the data into Dataframes
import pandas as pd

# For string literal 
import ast

# import packages related to gdal
from osgeo import gdal
import pyproj

# For time Zone Conversions
import pytz

# for plots
import matplotlib.pyplot as plt


with open('../data_collection/track_data/r2_Queen_of_Nanaimo.json') as f:
	for line in f:
		data = line

# Imported data now is in string format 
# Convert it into list of lists which we know the data structure of imported file.

data = ast.literal_eval(data)

# Covnert into numpy array
np.array(data)

# Assigning datatypes
mt_data = np.array([tuple(x) for x in data], dtype = [('lon', 'f8'), ('lat', 'f8'), ('speed', 'i4'), ('course', 'i4'), ('heading', 'i4'), ('timestamp', 'M8[s]'), ('ut', 'i8'), ('station', 'i8'), ('gap','i4')])

mt_data = pd.DataFrame(mt_data)
mt_data = mt_data.sort_values(by='timestamp')


tz_est = pytz.timezone('UTC')

tz_pst = "US/Pacific"

# Convert timezone of the data to Pacific

mt_data['timestamp'] = mt_data['timestamp'].dt.tz_localize(tz_est).dt.tz_convert(tz_pst)

bc_data = pd.read_pickle('bc_data.pkl')

#lon lat to cord
def proj_transform(df):
    bng = pyproj.Proj(init="epsg:4326")
    wgs84 = pyproj.Proj(init="epsg:3857")
    cart_x = pd.Series()
    cart_y = pd.Series()
    for idx, val in enumerate(df['lon']):
        lon, lat = pyproj.transform(bng,wgs84,df['lon'][idx], df['lat'][idx])
        cart_x.set_value(idx, lat)
        cart_y.set_value(idx, lon)
    df['cart_x'] = cart_y
    df['cart_y'] = cart_x
    return df
mt_data = proj_transform(mt_data)

mt_data['cart_x'] = mt_data['cart_x'].astype(float)
mt_data['cart_y'] = mt_data['cart_y'].astype(float)

# pixels to coordinates conversion funciton can only be applied upon 

def pixels_to_coordinates(bc_row,route_tif,index, **kwargs):
    if ('affine' in kwargs):
        pass
    else:
        # load in the route image
        ds = gdal.Open(route_tif)

        # unravel GDAL affine transform parameters
        c, a, b, f, d, e = ds.GetGeoTransform()
        def pixel2coord(col, row):
            # Returns global coordinates to pixel center using base-0 raster index
            xp = a * col + b * row + a * (-5.5) + b * (-5.5) + c
            yp = d * col + e * row + d * (-5.5) + e * (-5.5) + f
            return xp, yp

        cart_cord = pixel2coord(bc_row['cx'],bc_row['cy'])

        # Converting coordinates from EPSG 3857 to 4326
        inProj = pyproj.Proj(init='epsg:3857')
        outProj = pyproj.Proj(init='epsg:4326')

        coordinates = pyproj.transform(inProj, outProj, cart_cord[0], cart_cord[1])
        local_dict = {'lat': coordinates[1], 'lon': coordinates[0], 'cart_cord_x': cart_cord[0], 'cart_cord_y': cart_cord[1] }
        if index==0:
            return local_dict['lat']
        if index==1:
            return local_dict['lon']
        if index==2:
            return local_dict['cart_cord_x']
        if index==3:
            return local_dict['cart_cord_y']


# Route file location
route_file = "../qgis_approach/route2.tif"

# Filter specific route based on timestamp
mt_data_min_time = mt_data['timestamp'].min()
mt_data_max_time = mt_data['timestamp'].max()

# Localize time_Zone of Bc_Data to Pacific time.

bc_data['Time'] = bc_data['Time'].dt.tz_localize(tz_pst)

# Need to modify it so that can be supplied from input
vessel_name = 'Queen of Nanaimo'
bc_route_data = bc_data[(bc_data['Time'] >= mt_data_min_time) & (bc_data['Time'] <= mt_data_max_time) & (bc_data['Vessel'] == vessel_name)]

bc_route_data['lon'] = bc_route_data.apply(lambda x: pixels_to_coordinates(x,route_file,0), axis = 1)
bc_route_data['lat'] = bc_route_data.apply(lambda x: pixels_to_coordinates(x,route_file,1), axis = 1)
bc_route_data['cart_x'] = bc_route_data.apply(lambda x: pixels_to_coordinates(x,route_file,2), axis = 1)
bc_route_data['cart_y'] = bc_route_data.apply(lambda x: pixels_to_coordinates(x,route_file,3), axis = 1)

bc_route_data['dup_key'] = bc_route_data['cx'] + bc_route_data['cy']
no_dups_bc_route_data = bc_route_data.drop_duplicates('dup_key')


# Plot of all the route data
# plt.plot(mt_data['lon'], mt_data['lat'],'-',linewidth=0.5, color = 'blue')
# plt.plot(bc_route_data['lat'], bc_route_data['lon'],'-',linewidth=0.5, color ='green')

#plt.plot(mt_data['cart_x'][:100], mt_data['cart_y'][:100],'-',linewidth=0.5, color = 'red')
#plt.plot(bc_route_data['cart_x'][:200], bc_route_data['cart_y'][:200],'-',linewidth=0.5, color ='black')
#plt.show()

'''
# determining control points
filter_1 = mt_data[['cart_x', 'cart_y','timestamp','speed']][(mt_data['speed']==0)]
filter_1_ = bc_route_data[['cart_x', 'cart_y','Time', 'Status']][(bc_route_data['Status'] == 'In Port')]
plt.scatter(filter_1['cart_x'], filter_1['cart_y'], color ='blue')
plt.scatter(filter_1_['cart_x'],filter_1_['cart_y'], color = 'green')

plt.show()
'''

'''
Algorithm to solve for affine parameters

def solve_affine(s1,s2,s3,t1,t2,t3):
	Source_S = np.array([[Xs1, Ys1, 1, 0, 0, 0], [Xs2, Ys2, 1, 0, 0, 0], [Xs3, Ys3, 1, 0, 0, 0], [0, 0, 0, Xs1, Ys1, 1], [0, 0, 0, Xs2, Ys2, 1], [0, 0, 0, Xs3, Ys3, 1]])
	Target_T = np.array([Xt1, Xt2, Xt2, Yt1, Yt2, Yt3])
	affine = np.linalg.solve(Source_S,Target_T)
	return affine
'''