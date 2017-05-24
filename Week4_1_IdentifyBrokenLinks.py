# ---------------------------------------------------------------------------
# Chapter8_1_IdentifyBrokenLinks.py
# Created by Silas Toms
# 2014 04 23
# ---------------------------------------------------------------------------


import arcpy, os

mxdPath = r'C:\Projects\Week4\MXDs\BrokenLinks.mxd'
mxdObject = arcpy.mapping.MapDocument(mxdPath)
brokenLinks = arcpy.mapping.ListBrokenDataSources(mxdObject)
print brokenLinks
for link in brokenLinks:
    print link.name, link.dataSource

oldPath = r'C:\Projects\Week4\MXDs\Data'
newPath = r'C:\Projects\Week4\MXDs\NewData'
mxdObject.findAndReplaceWorkspacePaths(oldPath,newPath)
mxdObject.save()


