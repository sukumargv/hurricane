# QGIS Approach

## Problem

BCFerries provides live location of the vessels in the form of [static maps] (http://bcferries.applocation.net/routemaps/route4.html) by using [bing maps API] (https://msdn.microsoft.com/en-us/library/ff701724.aspx).

## Role of QGIS

> QGIS version: `2.16.3`
> Operating System: `MacOS sierra`

The following two plugins are ***required*** when performing manual geo-referencing in QGIS.
* [Georeferencer] (https://docs.qgis.org/2.2/en/docs/user_manual/plugins/plugins_georeferencer.html)
* [Open layers] (https://plugins.qgis.org/plugins/openlayers_plugin/)

After installing above plugins, Select `web > OpenLayers plugin > Bing Maps > Bing Aerial with labels` . This will add a bing maps layer under the layers panel on the left bottom side of the QGIS window. Now, try to zoom into the location where the image which needs to be georeferenced is approximately located.

Now, from the `Raster` menu select `> georeferencer > georeferencer...`. 

1. `File > Open raster` to load in the route map obtained from the BCferries website. [link] (http://bcferries.applocation.net/routemaps/route4.html)
2. Use the controls under `Edit` menu to add or remove reference points.
3. Once you think you have enough reference points, select `Transformaiton settings` under `Settings` menu. Set the following transformation settings in order to get a close approximated georeferencing. ([Refer for custom settings] (http://docs.qgis.org/1.8/en/docs/user_manual/plugins/plugins_georeferencer.html#defining-the-transformation-settings))
	* Transformation Type: `Linear`
	* Resampling method: `Nearest neighbour`
	* Target CRS : `Pseudo Mercator EPSG: 3857`
	* Name for Output Raster.
	* Make sure to Check `Load in QGIS when done`.
4. Select `Start Georeferencing` from the `File` menu.

Geo-referenced image will be overlayed onto the map once the referencing is done.

## Converting pixels to longitude and latitude

Dependencies for script.py
* pyproj
	`pip install pyproj` or `easy_install pyproj`
* osgeo/gdal (Procedure?)
	`pip install gdal` or `easy_install gdal` ??

Replace the `ds` variable in the script with the `path` to the geotif file.
