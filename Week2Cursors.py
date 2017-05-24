# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Week2Cursors.py
# Created by Silas Toms
# 2014 05 23
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import csv


arcpy.env.overwriteOutput =True

Bus_Stops = r"C:\Projects\ArcPy\SanFrancisco.gdb\SanFrancisco\Bus_Stops"

dataList = []
spatialReference = arcpy.SpatialReference(4326)
with arcpy.da.SearchCursor(Bus_Stops, ['NAME','STOPID','SHAPE@XY'], sql,spatialReference) as cursor:
    for row in cursor:
        linename = row[0]
        stopid = row[1]
        locationX = row[2][0]
        locationY = row[2][1]
        data = linename, stopid, locationX, locationY
        if data not in dataList:
            dataList.append(data)

csvname = "C:\Projects\ArcPy\Output\StationLocations.csv"
headers = 'Bus Line Name','Bus Stop ID', 'X','Y'
with open(csvname, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(headers)
    for datarow in dataList:
        csvwriter.writerow(datarow)
         
 
 
 
 
