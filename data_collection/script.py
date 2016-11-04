from bs4 import BeautifulSoup
import re
import math
import json
import gdal
import pyproj
import urllib2


# convert pixels to coordinates


def pixels_to_coordinates(route_no, center_x, center_y):
    ds = gdal.Open(route_no)

    # unravel GDAL affine transform parameters
    c, a, b, f, d, e = ds.GetGeoTransform()

    def pixel2coord(col, row):
        """Returns global coordinates to pixel center using base-0 raster index"""
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


soup = BeautifulSoup(urllib2.urlopen('http://bcferries.applocation.net/routemaps/route1.html').read(),
                     'html.parser')

# load in the html file

# soup = BeautifulSoup(open("./data/r00-2016-09-21_17-09-32.html"), 'html.parser')

# grab the content in the script section
script_content = soup.find('script')

if len(re.findall('<td>.*', script_content.string, re.MULTILINE)) is 0:
    print '.'
else:
    # container for data extracted from script part of html file
    final_boundaries_fragment = []
    # extract the content of pixel boundaries
    pixel_boundary_string = re.findall('if\s\(x.*', script_content.string, re.MULTILINE)

    # operating on the string obtained via regular expression to format the data into dictionary
    for x in pixel_boundary_string:
        local = []
        dict_local = {}
        split_text = x.split()
        dict_local['x1'] = int(split_text[3])
        dict_local['y1'] = int(split_text[7])
        dict_local['x2'] = int(split_text[11])
        dict_local['y2'] = int(re.sub('\)', '', split_text[15]))
        bottom_edge_width = dict_local['x2'] - dict_local['x1']
        left_edge_width = dict_local['y2'] - dict_local['y1']
        dict_local['cx'] = int(dict_local['x1'] + math.floor(bottom_edge_width / 2))
        dict_local['cy'] = int(dict_local['y1'] + math.floor(left_edge_width) / 2)
        final_boundaries_fragment.append(dict_local)

    # container for rest of the vessel data from the script portion
    js_data = []
    # extract the rest of the original vessel data in the script portion
    grabbed_content = re.findall('<td>.*', script_content.string, re.MULTILINE)

    # operating on rest of vessel data and cleaning up and structuring
    for x in grabbed_content:
        local = []
        dict_local = {}
        replace_td = re.compile('<td>')
        x = replace_td.sub(' ', x)
        replace_b = re.compile('<b>')
        x = replace_b.sub(' ', x)
        x = x.strip()[:-11]
        if ':' in x:
            x = x.split(':')
            # converting unicode to string
            dict_local[str(x[0])] = str((x[1]).strip())
        else:
            # Vessel name does not have any prefix
            dict_local['Vessel'] = str(x)
        js_data.append(dict_local)
    # grouping data by vessel
    js_grouped_by_vessel = [js_data[x:x + 4] for x in range(0, len(js_data), 4)]

    # Final formatted data for the js fragment
    final_js_fragment = []
    for i in js_grouped_by_vessel:
        final_js_fragment.append(i)

    page_data = []
    # extracting html data
    rows = soup.find_all('td')[:-2]
    # container for tds
    list_of_tds = []

    for el in soup.find_all('td')[:-2]:
        x = el.get_text()
        # converting unicode to string
        list_of_tds.append(str(el.get_text()))
    # grouping data by row
    grouped_tds = [list_of_tds[x:x + 4] for x in range(0, len(list_of_tds), 4)]
    # first rows of the table which need to be seen as keys
    keys_html = grouped_tds[0]
    # later part of the table which are values for the keys
    data_html = grouped_tds[1:]

    # making dictionary by looping over the
    for i in data_html:
        dict_local = {}

        for j in i:
            dict_local[keys_html[i.index(j)]] = j

        dict_local['Boundaries'] = final_boundaries_fragment[len(page_data)]
        dict_local['Heading'] = final_js_fragment[len(page_data)][2]['Heading']
        dict_local['Speed'] = final_js_fragment[len(page_data)][3]['Speed']
        # cx, cy = final_boundaries_fragment[len(page_data)]['cx'], final_boundaries_fragment[len(page_data)]['cx']

        # function call to convert center pixel to geographic lon and lat
        # dict_local['location'] = pixels_to_coordinates('../tiff_routes/route4_modified_1.tif', cx, cy)

        page_data.append(dict_local)

#    print json.dumps(page_data, indent=2, sort_keys=True, separators=(',', ':'))

    with open('result.json', 'w') as fp:
        json.dump(page_data, fp, indent=2, sort_keys=True, separators=(',', ':'))
