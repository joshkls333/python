# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Chapter3Model1.py
# Created on: 2014-04-22 21:59:31.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# Adjusted by Silas Toms
# 2014 04 23
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import csv


# Local variables:
Bus_Stops = r"C:\Projects\SanFrancisco.gdb\SanFrancisco\Bus_Stops"
CensusBlocks2010 = r"C:\Projects\SanFrancisco.gdb\SanFrancisco\CensusBlocks2010"
Bus_Stop_Select = r"C:\Projects\SanFrancisco.gdb\Chapter3Results\Bus_Stop_Select"
Bus_Stop_Buffer = r"C:\Projects\SanFrancisco.gdb\Chapter3Results\Bus_Stop_Buffer"
Bus_Stop_Intersect = r"C:\Projects\SanFrancisco.gdb\Chapter3Results\Bus_Stop_Intersect"

# Process: Select
arcpy.Select_analysis(Bus_Stops, 
                      Bus_Stop_Select, 
                      "NAME = '71 IB' AND BUS_SIGNAG = 'Ferry Plaza'")
 
# Process: Buffer
arcpy.Buffer_analysis(Bus_Stop_Select, 
                      Bus_Stop_Buffer, 
                      "400 Feet", "FULL", "ROUND", "NONE", "")
 
# Process: Intersect
arcpy.Intersect_analysis("{0} #;{1} #".format(Bus_Stop_Buffer,CensusBlocks2010), 
                         Bus_Stop_Intersect, "ALL", "", "INPUT")

dataDictionary = {}

with arcpy.da.SearchCursor(Bus_Stop_Intersect, ["STOPID","POP10"]) as cursor:
    for row in cursor:
        busStopID = row[0]
        pop10 = row[1]
        if busStopID not in dataDictionary.keys():
            dataDictionary[busStopID] = [pop10]
        else:
            dataDictionary[busStopID].append(pop10)


with open(r'C:\Projects\Output\Averages.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for busStopID in dataDictionary.keys():
        popList = dataDictionary[busStopID]
        averagePop = sum(popList)/len(popList)
        data = [busStopID, averagePop]
        csvwriter.writerow(data)

print "Data Analysis Complete"