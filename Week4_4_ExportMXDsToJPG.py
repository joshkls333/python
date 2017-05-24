# ---------------------------------------------------------------------------
# Chapter8_4_ExportMXDsToPDF.py
# Created by Silas Toms
# 2014 08 23
# ---------------------------------------------------------------------------


import arcpy, glob, os
mxdFolder = r'C:\Projects\MXDs\Week4'
pdfFolder = r'C:\Projects\PDFs\Week4'
mxdPathList = glob.glob(os.path.join(mxdFolder, '*.mxd'))
for mxdPath in mxdPathList:
    mxdObject = arcpy.mapping.MapDocument(mxdPath)
    arcpy.mapping.ExportToPJPEG(mxdObject,
                              os.path.join(
                                           pdfFolder,
                                               os.path.basename(
                                                                mxdPath.replace('mxd','jpg')
                                                                )
                                           )
                              )
