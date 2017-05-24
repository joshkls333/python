# -*- coding: utf-8 -*-
"""
Created on July 10, 2015

@author: SLALONDE

edits and updates by Josh Klaus
"""
from argparse import ArgumentParser
import collections
import os
import pandas as pd
import pytz
import numpy as np

def csv_to_db(ffile, dfile, odir, idir, sind):

    # Constant Filenames
    LakeD = "LakeData"
    TribD = "TributaryData"
    RiverD = "RiverData"
    PhytoplanktonD = "PhytoplanktonData"
    ZooplanktonD = "ZooplanktonData"

    # read field inclusion and input data files
    ffile = idir + '/' + ffile
    dfile = idir + '/' + dfile

    # read project and site input csv files
    try:
      pfile = idir + '/' + 'Projects.csv'
      projDf = pd.read_csv(pfile, dtype=str)
    except IOError:
       print 'Projects.csv file not found.  Be sure to:'
       print 'run script in root project directory or'
       print 'use fully qualified pathnames for directories'
    sfile = idir + '/' + 'MonitoringLocations.csv'

    siteDf = pd.read_csv(sfile, dtype=str)
    # just reference index values from site input file
    siteCol = list(['UID', 'Id'])
    siteDf = siteDf[siteCol]

    # format output file names
    base = os.path.basename(dfile)
    ofile = os.path.splitext(base)[0]
    actfile = odir + '/' + ofile + 'Activity.csv'
    actprojfile = odir + '/' + ofile + 'ActProj.csv'
    resfile = odir + '/' + ofile + 'Result.csv'

    # get applicable project id based on data file
    proj_id_dict  = collections.OrderedDict({LakeD: projDf.Id[0],
                  TribD: projDf.Id[1],
                  RiverD: projDf.Id[2],
                  PhytoplanktonD: projDf.Id[3],
                  ZooplanktonD: projDf.Id[4]
                })

    proj_uid_dict  = collections.OrderedDict({LakeD: projDf.UID[0],
                    TribD: projDf.UID[1],
                    RiverD: projDf.UID[2],
                    PhytoplanktonD: projDf.UID[3],
                    ZooplanktonD: projDf.UID[4]
                })
    proj_id_sel = proj_id_dict[ofile]
    proj_uid_sel = proj_uid_dict[ofile]

    #get columns in data file where USE is set to TRUE in field definition file
    fieldDf = pd.read_csv(ffile, dtype=str)
    colUse = list(fieldDf.loc[fieldDf['Use'] == 'TRUE','Field'])
    dataDf = pd.read_csv(dfile, dtype=str, mangle_dupe_cols=True)
    #dataDf.rename(columns=lambda x: x.strip(), inplace=True)
    #print dataDf
    origEnt = len(dataDf)
    dataDf = dataDf[colUse]

    #get all valid site identifiers
    site_dict  = {LakeD: "Site #",
                  TribD: "Site #",
                  RiverD: "Site #",
                  PhytoplanktonD: "SITE_ID_CODE",
                  ZooplanktonD: "SITE_ID_CODE"}
    site_sel = site_dict[ofile]
    siteId = list(siteDf['Id'])

    # get data for valid known sites
    missDf = dataDf[~dataDf[site_sel].isin(siteId)]
    siteEnt = len(missDf)
    dataDf = dataDf[dataDf[site_sel].isin(siteId)]

    if not(missDf.empty):
        print "WARNING: The following sites are not recognized and will not be included in output csv file"
        print pd.unique(missDf[site_sel])
        print "This impacts ", siteEnt, "rows from the input csv file"
    dataDf = pd.merge(dataDf, siteDf, left_on=site_sel, right_on='Id', how='left')

    # ACTIVITY DATA FRAME PROCESSING
    #format DATE

    if ofile == PhytoplanktonD or ofile == ZooplanktonD:
        mypartdate = "%m/%d/%Y"
    else:
        mypartdate = "%d-%b-%y"

    dataDf['FDATE'] = pd.to_datetime(dataDf['DATE'],format=mypartdate)
    dataDf['FDATE'] = dataDf['FDATE'].apply(lambda x: x.strftime('%Y%m%d'))

    if 'TIME' in dataDf and dataDf['TIME'].str.contains('\.').any():
       # 0 is an unacceptable time format
       dataDf.TIME[dataDf['TIME'] == '0'] = '0000'
       # remove dot from a few TIME records
       idx_contains_dot = dataDf['TIME'].str.contains('\.')
       dataDf.TIME[idx_contains_dot] = dataDf.TIME[idx_contains_dot].str.replace('\.', '')


    # Remove NaT's from TIME and thus  StartTime

    if 'TIME' in dataDf and dataDf.TIME.isnull().any():
        dataDf['TIME'] = "0000"

    #format TIME
    # modify if do not want to replace NAs with 0000
    if 'TIME' in dataDf:
        dataDf['StartTime'] = dataDf['TIME']
        dataDf['StartTime'] = pd.to_datetime(dataDf['StartTime'], format='%H%M')
        dataDf['StartTime'] = dataDf['StartTime'].apply(lambda x: x.time())
        dataDf['FTIME'] = dataDf['StartTime'].apply(lambda x: x.strftime('%H%M'))
        dataDf['MStartTime'] = dataDf['StartTime'].apply(lambda x: x.strftime('%X'))
    else:
        dataDf['FTIME'] = "0000"
        dataDf['MStartTime'] = "00:00:00"


    #format TIMEZONE
    dataDf['MergeTime'] = pd.to_datetime(dataDf['FDATE'] + dataDf['FTIME'])
    pacific_tz = pytz.timezone('US/Pacific')
    list_local = map(pacific_tz.localize, dataDf['MergeTime'])
    dataDf['ZoneTime'] = pd.DatetimeIndex(list_local)
    dataDf['TimeZoneCode'] = dataDf['ZoneTime'].apply(lambda x: x.strftime('%Z'))

    # format DEPTH and DEPTH UNITS
    if ofile == LakeD:
        dataDf['Id'] = proj_id_sel + '_' + dataDf['UID'] + '_' +  dataDf['Z'] + '_' + dataDf['FDATE'] + '_' + dataDf['FTIME']
        # replace any NaN depth values with '9999'
        dataDf.Z.fillna('9999', inplace=True)
        dataDf['DepthM'] = dataDf['Z']
    else:
        dataDf['Id'] = proj_id_sel + '_' + dataDf['UID'] + '_0_' + dataDf['FDATE'] + '_' + dataDf['FTIME']
        dataDf['DepthM'] = '0'
    dataDf['DepthU'] = 'm'

    # format other activity columns
    dataDf['Type'] = 'Field Msr/Obs'

    if ofile == PhytoplanktonD or ofile == ZooplanktonD:
        dataDf['Media'] = 'Biological'
        dataDf['AssemblageSample'] = 'Phytoplankton/Zooplankton'
    else:
        dataDf['Media'] = 'Water'
        dataDf['AssemblageSample'] = None
    dataDf['StartDate'] = dataDf['DATE']
    dataDf['OrgId'] = 1
    dataDf['Site'] = dataDf[site_sel]

    #remove invalid rows
    missDf = dataDf[dataDf['Id'].isnull()]
    missEnt = len(missDf)
    if not(missDf.empty):
        print "WARNING: The following elements do not have valid activity IDs and will not be included in output csv file"
        print missDf
        print "This impacts ", missEnt, "rows from the input csv file"
    dataDf = dataDf[dataDf['Id'].notnull()]

    dupEnt = 0
    if not (ofile == PhytoplanktonD or ofile == ZooplanktonD):
        counts = dataDf.groupby('Id').size()
        dupDf = pd.DataFrame(counts, columns = ['size'])
        dupDf = dupDf[dupDf['size'] > 1]
        if not(dupDf.empty):
            dupEnt = len(dupDf)
            print "WARNING: The following elements have duplicate activity IDs and will not be included in output csv file"
            print dupDf
            print "This impacts ", dupEnt, "rows from the input csv file"
            dataDf = dataDf.drop_duplicates(subset=['Id'])

     # assign Project ID based on valid rows
    dataDf['Proj'] = proj_uid_sel

    # assign Act ID based on valid rows
    if (ofile == PhytoplanktonD or ofile == ZooplanktonD):
        dataDf['Inc'] = dataDf.groupby(['Id']).cumcount()
        dataDf['CheckInc'] = dataDf.groupby('Inc').cumcount().apply(lambda x: x + 1) - 1
        dataDf['Act'] = dataDf['CheckInc'] + int(sind)
    else:
        dataDf['Inc'] = dataDf.groupby(['Proj']).cumcount()
        dataDf['Act'] = dataDf['Inc'] + int(sind)

    #output Activity file
    actCol = list(['Act', 'Id', 'Type', 'Media', 'AssemblageSample', 'StartDate','MStartTime', 'TimeZoneCode','DepthM', 'DepthU', 'OrgId', 'Site'])
    actDf = dataDf[actCol]
    actDf = actDf.drop_duplicates(subset=['Act'])
    actDf.to_csv(actfile, header=False, index=False)
    actEnt = len(actDf)

    # output Activity Project file
    actprojCol = list(['Proj', 'Act'])
    actprojDf = dataDf[actprojCol]
    actprojDf = actprojDf.drop_duplicates(subset=['Proj','Act'])
    actprojDf.to_csv(actprojfile, header=False, index=False)
    actprojEnt = len(actprojDf)


    # RESULT DATA FRAME PROCESSING
    #combine Date and Time into single field
    if ofile == PhytoplanktonD or ofile == ZooplanktonD:
        myfulldate = "%m/%d/%Y %H%M"
    else:
        myfulldate = "%d-%b-%y %H%M"
    if 'TIME' in dataDf:
        dataDf['TIME'].fillna("0000", inplace=True)
        dataDf['Date'] = pd.to_datetime(dataDf['DATE'] + ' ' + dataDf['TIME'], format=myfulldate)
    else:
        dataDf['Date'] = pd.to_datetime(dataDf['DATE'] + ' 0000', format=myfulldate)

    #remove columns not necessary for result output
    if 'TIME' in dataDf:
        dataDf = dataDf.drop(['DATE', 'TIME', 'FDATE', 'FTIME', 'DepthM', 'DepthU', 'Id', 'Inc', 'Media', 'AssemblageSample', 'MergeTime', 'MStartTime', 'OrgId', 'Proj','Site','StartDate', 'StartTime', 'TimeZoneCode', 'Type', 'UID','ZoneTime'], axis=1)
    else:
        dataDf = dataDf.drop(['DATE', 'FDATE', 'FTIME', 'DepthM', 'DepthU', 'Id', 'Inc', 'Media', 'AssemblageSample', 'MergeTime', 'MStartTime', 'OrgId', 'Proj','Site','StartDate', 'TimeZoneCode', 'Type', 'UID','ZoneTime'], axis=1)
    if 'CheckInc' in dataDf:
        dataDf = dataDf.drop(['CheckInc'], axis=1)

    print dataDf.columns.values

    # rename columns names matching WQX naming convention
    colmap = fieldDf.loc[pd.notnull(fieldDf['CharMap'])]
    map_dict = dict(zip(colmap.Field, colmap.CharMap))
    dataDf.rename(columns=map_dict, inplace=True)

    #transform observations in columns into separate rows
    #ensure duplicate and verfification data is preserved
    targetDf = pd.DataFrame([])
    dataDf['dummyDuplicate'] = None
    dataDf['dummyPassFail'] = None

    # Process Lake, Tributary and River Data to generate CharacteristicMap column (eventually) in Result file
    if ofile == LakeD or ofile == TribD or ofile == RiverD:
        # Remove columns from value variables for melt
        process_cols = dataDf.columns.tolist()
        for col in ['Act', 'Site #', 'Date', 'Notes']:
	    process_cols.remove(col)
        targetDf = pd.melt(dataDf, id_vars = ['Act', 'Notes'], value_vars = process_cols)
        targetDf['Duplicate'] = ''
        targetDf['PassFail'] = ''

    if ofile == ZooplanktonD:
        #x = 67
        x = len(dataDf.columns) - 1
        for i in range(3,63):
            loopDf = pd.melt(dataDf, id_vars=[dataDf.columns[0], dataDf.columns[1], dataDf.columns[2], dataDf.columns[65], dataDf.columns[64], dataDf.columns[66], dataDf.columns[67]], value_vars=dataDf.columns[i])
            loopDf.rename(columns={'dummyDuplicate': 'Duplicate', 'dummyPassFail': 'PassFail'}, inplace=True)
            targetDf = targetDf.append(loopDf)

    if ofile == PhytoplanktonD:
        #x = 67
        x = len(dataDf.columns) - 1
        for i in range(3,140):
            loopDf = pd.melt(dataDf, id_vars=[dataDf.columns[0], dataDf.columns[1], dataDf.columns[2], dataDf.columns[141], dataDf.columns[142], dataDf.columns[143], dataDf.columns[144]], value_vars=dataDf.columns[i])
            loopDf.rename(columns={'dummyDuplicate': 'Duplicate', 'dummyPassFail': 'PassFail'}, inplace=True)
            targetDf = targetDf.append(loopDf)

        # Dictionary/Keys
    Spec1 = "Nitrogen"
    Spec2 = "Ammonia-nitrogen"
    Spec3 = "Nitrite"
    Spec4 = "Phosphorous"
    Spec5 = "Phosphate-phosphorus"
    Spec6 = "Silica"

    Pplank1 = "Biovol Rptd"
    Pplank2 = "Biovol Stnd"
    Pplank3 = "Biovol% Rptd"
    Pplank4 = "Biovol% Stnd"
    Pplank5 = "Dens Cell Stnd"
    Pplank6 = "Dens Cell% Stnd"
    Pplank7 = "Dens NU"
    Pplank8 = "Dens NU%"

    PplankUnit1 = "cells/L"
    PplankUnit2 = "mm3/L"
    PplankUnit3 = "NU/L"
    PplankUnit4 = "Percent"

    Zplank1 = "Abundance"
    Zplank2 = "Abundance%"
    Zplank3 = "Biomass"
    Zplank4 = "Biomass%"

    ZplankUnit1 = "number/L"
    ZplankUnit2 = "Percent"
    ZplankUnit3 = "ug/L"
    ZplankUnit4 = "Percent"

    PplankCharDict = {Pplank1: "Total Sample Weight",
                  Pplank2: "Total Sample Weight",
                  Pplank3: "Count",
                  Pplank4: "Count",
                  Pplank5: "Count",
                  Pplank6: "Count",
                  Pplank7: "Count",
                  Pplank8: "Count"}

    PplankTypeDict = {Pplank1: "Actual",
                  Pplank2: "Actual",
                  Pplank3: "Calculated",
                  Pplank4: "Calculated",
                  Pplank5: "Actual",
                  Pplank6: "Calculated",
                  Pplank7: "Actual",
                  Pplank8: "Calculated"}

    PplankUnitDict = {PplankUnit1: "#/l",
                      PplankUnit2: "mm3/l",
                      PplankUnit3: "CFU",
                      PplankUnit4: "%"}

    ZplankCharDict = {Zplank1: "Count",
                  Zplank2: "Count",
                  Zplank3: "Total Sample Weight",
                  Zplank4: "Count"}

    ZplankTypeDict = {Zplank1: "Actual",
                  Zplank2: "Calculated",
                  Zplank3: "Actual",
                  Zplank4: "Calculated"}

    ZplankUnitDict = {ZplankUnit1: "#/l",
                      ZplankUnit2: "%",
                      ZplankUnit3: "ug/l",
                      ZplankUnit4: "%"}

    MethodSpecDict = {Spec1: "As N",
                      Spec2: "As NH4",
                      Spec3: "As NO2",
                      Spec4: "As P",
                      Spec5: "As PO4",
                      Spec6: "As SiO2"}

    # format all result  fields
    x = len(dataDf.columns) - 1
    # NEED TO MELT HERE!



    targetDf['BI'] = None
    targetDf['TaxName'] = None
    targetDf['TaxUnident'] = None
    targetDf['DataLogger'] = None
    targetDf['MethodSpec'] = targetDf['variable'].map(MethodSpecDict)
    targetDf['DetectCond'] = None
    targetDf['Qualifier'] = None
    targetDf['Status'] = 'Final'
    targetDf['StatBaseCode'] = None
    targetDf['AnalyticalMethodId'] = None
    targetDf['AnalyticalMethodContext'] = None
    targetDf['AnalysisStartDate'] = None


    if ofile == LakeD or ofile == TribD or ofile == RiverD:
        colmap = fieldDf.loc[pd.notnull(fieldDf['UnitMap'])]
        unit_dict = dict(zip(colmap.CharMap, colmap.UnitMap))
        targetDf['Unit'] = targetDf['variable'].map(unit_dict)
        targetDf['Type'] = 'Actual'
        # remove depth Z as already embedded in activity
        targetDf = targetDf[targetDf['variable'] != 'Z']

    if ofile == PhytoplanktonD:
        colmap = fieldDf.loc[pd.notnull(fieldDf['CharMap'])]
        unident_dict = dict(zip(colmap.CharMap, colmap.IdentMap))
        targetDf['BI'] = 'Population Census'
        targetDf['TaxName'] = targetDf['variable']
        targetDf['TaxUnident'] = targetDf['variable'].map(unident_dict)
        targetDf['variable'] = targetDf['PARAMETER'].map(PplankCharDict)
        targetDf['Unit'] = targetDf['UNITS'].map(PplankUnitDict)
        targetDf['Type'] = targetDf['PARAMETER'].map(PplankTypeDict)
        #keep Std values and remove Rptd values for Phytoplankton
        targetDf = targetDf[targetDf['PARAMETER'].str.contains('Rptd') == False]
        targetDf['Notes'] = None

    if ofile == ZooplanktonD:
        colmap = fieldDf.loc[pd.notnull(fieldDf['CharMap'])]
        unident_dict = dict(zip(colmap.CharMap, colmap.IdentMap))
        targetDf['BI'] = 'Population Census'
        targetDf['TaxName'] = targetDf['variable']
        targetDf['TaxUnident'] = targetDf['variable'].map(unident_dict)
        targetDf['variable'] = targetDf['PARAMETER'].map(ZplankCharDict)
        targetDf['Unit'] = targetDf['UNITS'].map(ZplankUnitDict)
        targetDf['Type'] = targetDf['PARAMETER'].map(ZplankTypeDict)
        targetDf = targetDf[targetDf['PARAMETER'].str.contains('Rptd') == False]
        targetDf['Notes'] = None

    # populate Sample Fraction based on characteristic
    targetDf['SampleFraction'] = None
    SampFraction = ['Ammonia-nitrogen', 'Chloride', 'Inorganic nitrogen (nitrate and nitrite)', 'Nitrite', 'Nitrogen', 'Organic phosphorus', 'Pheophytin a', 'Phosphate-phosphorus', 'Phosphorus']
    targetDf.loc[targetDf.variable.isin(SampFraction), 'SampleFraction'] = 'Total'

    #rename columns
    targetDf.rename(columns={site_sel: 'Sitecode', 'variable': 'CharacteristicName', 'value': 'ResultMeasure', 'Notes': 'Comment'}, inplace=True)
    # resultCol = list(['Act', 'BI', 'TaxName', 'TaxUnident', 'CharacteristicName', 'ResultMeasure', 'Unit', 'Type', 'DataLogger', 'MethodSpec', 'DetectCond', 'Qualifier', 'SampleFraction', 'Status', 'StatBaseCode', 'AnalyticalMethodId', 'AnalyticalMethodContext', 'AnalysisStartDate', 'Comment', 'Duplicate', 'PassFail'])
    resultCol = list(['Act', 'BI', 'TaxName', 'TaxUnident', 'CharacteristicName', 'ResultMeasure', 'Unit', 'Type', 'DataLogger', 'MethodSpec', 'DetectCond', 'Qualifier', 'SampleFraction', 'Status', 'StatBaseCode', 'AnalyticalMethodId', 'AnalyticalMethodContext', 'AnalysisStartDate', 'Comment', 'Duplicate', 'PassFail'])
    targetDf = targetDf[resultCol]
    targetDf.to_csv(resfile, header=True, index=False, sep=",")
    #dataDf.loc[dataDf['Measured Parameter'].str.contains("dissolved", case=False), 'resultsampfraction'] = "Dissolved"
    nanDf = targetDf['ResultMeasure'].str.contains("n/a", case=False)
    #print nanDf
    nanEnt = len(nanDf)
    zeroresDf = targetDf[targetDf.ResultMeasure.isnull()]
    zeroEnt = len(zeroresDf)
    targetDf = targetDf[targetDf.ResultMeasure.notnull()]
    resEnt = len(targetDf)

    #output result file
    #targetDf.to_csv(resfile, header=True, index=False, sep=",")

    targetDf.to_csv(resfile, header=True, index=False, sep="|")

    #output summary of processing
    print "\nOriginal spreadsheet dataset:  ", origEnt, " rows"
    print "Invalid site entries:  ", siteEnt, " rows"
    print "Invalid activity ID entries:  ", missEnt, " rows"
    print "Duplicate activity ID entires: ", dupEnt, " rows"
    print "Total valid activity entries:  ", actEnt, " rows"
    print "\nN/A measure result entries:  ", nanEnt, " rows"
    print "\nBlank measure result entries:  ", zeroEnt, "rows"
    print "Total valid result entries: ", resEnt, "rows"




def main():
    usage = "usage: %prog [options] arg1 arg2"
    parser = ArgumentParser(usage)
    parser.add_argument("-dfile", "--datafile", dest="data_file", help="data file intended for database export")
    parser.add_argument("-ffile", "--fieldfile", dest="field_file", help="file with list of columns to include")
    parser.add_argument("-idir", "--input_dir", dest="input_dir", help="input directory name for csv formatted files")
    parser.add_argument("-odir", "--output_dir", dest="output_dir", help="output directory name for csv formatted files")
    parser.add_argument("-sind" , "--startindex", dest="start_index", help="start index for activity ID field")
    args = parser.parse_args()

    # check that file parameters are specified in command line
    mandatories = ['field_file', 'data_file', 'output_dir', 'input_dir', 'start_index']

    for m in mandatories:
        if getattr(args, m) == None:
            parser.error("option -" + m + " is mandatory.")
    f = csv_to_db(args.field_file, args.data_file, args.output_dir, args.input_dir, args.start_index)

if __name__ == '__main__':
     main()
