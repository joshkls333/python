

import arcpy, os

Bus_Stops = r"C:\Projects\Week4\MXDs\Data\SanFrancisco.gdb\SanFrancisco\Bus_Stops"
selectedBusStop = r'C:\Projects\Week4\MXDs\Data\SanFrancisco.gdb\Week4Results\SelectedBusStop'
selectedStopBuffer = r'C:\Projects\MXDs\Data\SanFrancisco.gdb\Week4Results\SelectedStopBuffers'
CensusBlocks2010 = r"C:\Projects\Week4\MXDs\Data\SanFrancisco.gdb\SanFrancisco\CensusBlocks2010"
selectedBlock = r'C:\Projects\Week4\MXDs\Data\SanFrancisco.gdb\Week4Results\SelectedCensusBlocks'
pdfFolder = r'C:\Projects\Week4\PDFs\Map_{0}'
bufferDist = 400

sql = "(NAME = '71 IB' AND BUS_SIGNAG = 'Ferry Plaza')"
mxdPath = r'C:\Projects\Week4\MXDs\MapAdjust.mxd'
mxdObject = arcpy.mapping.MapDocument(mxdPath)
dataFrame = arcpy.mapping.ListDataFrames(mxdObject, "Layers")[0]
elements = arcpy.mapping.ListLayoutElements(mxdObject)
for el in elements:
    if el.type =="TEXT_ELEMENT":
        if el.text == 'Title Element':
            titleText = el
        elif el.text == 'Subtitle Element':
            subTitleText = el
arcpy.MakeFeatureLayer_management(CensusBlocks2010, 'blocks_lyr')       
layersList = arcpy.mapping.ListLayers(mxdObject,"",dataFrame)
layerStops = layersList[0]
layerBuffer = layersList[1]
layerBlocks = layersList[2] 
if layerBlocks.dataSource != selectedBlock:
    layerBlocks.replaceDataSource(os.path.dirname(os.path.dirname(layerBlocks.dataSource)),'FILEGDB_WORKSPACE',os.path.basename(selectedBlock))
if layerStops.dataSource != selectedBusStop:
    layerStops.replaceDataSource(os.path.dirname(os.path.dirname(layerStops.dataSource)),'FILEGDB_WORKSPACE',os.path.basename(selectedBusStop))

layerStops.visible = True
layerBuffer.visible = False
with arcpy.da.SearchCursor(Bus_Stops,['SHAPE@','STOPID','NAME','BUS_SIGNAG' ,'OID@','SHAPE@XY'],sql) as cursor:
    for row in cursor:
        stopPointGeometry = row[0]
        stopBuffer = stopPointGeometry.buffer(bufferDist)
        with arcpy.da.UpdateCursor(layerBlocks,['OID@']) as dcursor:
            for drow in dcursor:
                dcursor.deleteRow()
        arcpy.SelectLayerByLocation_management('blocks_lyr', 'intersect', stopBuffer, "", "NEW_SELECTION")
        with arcpy.da.SearchCursor('blocks_lyr',['SHAPE@','POP10','OID@']) as bcursor:
            inCursor = arcpy.da.InsertCursor(selectedBlock,['SHAPE@','POP10'])
            for drow in bcursor:                
                data = drow[0],drow[1]
                inCursor.insertRow(data)
        del inCursor
        with arcpy.da.UpdateCursor(selectedBusStop,['OID@']) as dcursor:
            for drow in dcursor:
                dcursor.deleteRow()
        inBusStopCursor = arcpy.da.InsertCursor(selectedBusStop,['SHAPE@'])
        for drow in bcursor:                
            data = [row[0]]
            inBusStopCursor.insertRow(data)
        del inBusStopCursor
        layerStops.name = "Stop #{0}".format(row[1])
        arcpy.RefreshActiveView()
        dataFrame.extent = arcpy.Extent(row[-1][0]-1200,row[-1][1]-1200,row[-1][0]+1200,row[-1][1]-1200)   
        subTitleText.text = "Route {0}".format(row[2])
        titleText.text = "Bus Stop {0}".format(row[1])
        outPath  = pdfFolder.format( str(row[1])+ "_" + str(row[-2])) + '.pdf'
        print outPath
        arcpy.mapping.ExportToPDF(mxdObject,outPath)
        titleText.text = 'Title Element'
        subTitleText.text = 'Subtitle Element'
        arcpy.RefreshActiveView()
        
