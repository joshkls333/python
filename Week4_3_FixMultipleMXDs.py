# ---------------------------------------------------------------------------
# Chapter8_3_FixMultipleMXDs.py
# Created by Silas Toms
# 2014 08 23
# ---------------------------------------------------------------------------


import arcpy, glob, os
oldPath = r'C:\Projects\Week4\MXDs\NewData'
newPath = r'C:\Projects\Week4\MXDs\Data'
folderPath = r'C:\Projects\Week4\MXDs'
mxdPathList = glob.glob(os.path.join(folderPath, '*.mxd'))
for path in mxdPathList:   
    mxdObject = arcpy.mapping.MapDocument(path)
    mxdObject.findAndReplaceWorkspacePaths(oldPath,newPath)
    mxdObject.save()


