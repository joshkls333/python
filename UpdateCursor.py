import arcpy

busstops = r'C:\Projects\ArcPy\SanFrancisco.gdb\SanFrancisco\Bus_Stops'

where  = "OBJECTID < 11"

spatialRef = arcpy.SpatialReference(4326)

cursor = arcpy.da.UpdateCursor(busstops,
                               ["ROUTEID",  "SHAPE@XY", "X", "Y"],
                               where,spatialRef )

for row in cursor:

    longitude = row[1][0]
    latitude = row[1][1]
    row[2] = longitude
    row[3] = latitude
    cursor.updateRow(row)



