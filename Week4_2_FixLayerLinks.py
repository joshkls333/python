# ---------------------------------------------------------------------------
# Chapter8_2_FixLayerLinks.py
# Created by Silas Toms
# 2014 08 23
# ---------------------------------------------------------------------------


import arcpy, os

layerDic = {'Bus_Stops': [r'C:\Projects\Week4\MXDs\Data',r'C:\Projects\MXDs\NewData'],
    'Inbound71_400ft_buffer': [r'C:\Projects\Week4\MXDs\Data',r'C:\Projects\MXDs\NewData'],
    'stclines_streets': [r'C:\Projects\Week4\MXDs\Data',r'C:\Projects\MXDs\NewData'],
    'planning_openspaces': [r'C:\Projects\Week4\MXDs\Data',r'C:\Projects\MXDs\NewData'],
    'Realtor_Neighborhoods': [r'C:\Projects\Week4\MXDs\Data',r'C:\Projects\MXDs\NewData'],
    'SanFrancisco': [r'C:\Projects\Week4\MXDs\Data',r'C:\Projects\MXDs\NewData']
    }
mxdPath = 'C:\Projects\MXDs\Week4\BrokenLinks.mxd'
mxdObject = arcpy.mapping.MapDocument(mxdPath)
brokenLinks = arcpy.mapping.ListBrokenDataSources(mxdObject)
for layer in brokenLinks:
    oldPath, newPath = layerDic[layer.name]
    layer.findAndReplaceWorkspacePath(oldPath, newPath )
    
    print oldPath,newPath
mxdObject.save()

