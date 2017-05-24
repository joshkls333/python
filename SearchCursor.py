import arcpy

busstops = r'C:\Projects\ArcPy\SanFrancisco.gdb\SanFrancisco\Bus_Stops'

where  = "OBJECTID < 11"

spatialRef = arcpy.SpatialReference(4326)

cursor = arcpy.da.SearchCursor(busstops,
                               ["ROUTEID",  "SHAPE@XY", "X", "Y"],
                               where,spatialRef )

for row in cursor:
    print row

    


