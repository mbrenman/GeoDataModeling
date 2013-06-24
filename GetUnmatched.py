"""
Author: Matt Brenman

Purpose: To convert a geocoded set of points (with a corresponding shapefile
         result table containing all attributes) into a tab delimited version
         of the unmatched addresses. This is used because it is redundant to
         re-geocode the matched addresses (which are on the scale of hundreds
         of thousands). This saves time in recoding addresses, and it allows us
         to see bigger picture errors in the file instead of limiting ourselves
         to each city (which we can still do if needed)

"""

import arcpy
import csv

georesult = arcpy.GetParameterAsText(0)
outfile = arcpy.GetParameterAsText(1)
outfolder = arcpy.GetParameterAsText(2)

print outfolder
arcpy.env.overwriteOutput = True
arcpy.TableToTable_conversion(georesult, outfolder, "unmatchtable", "Status = 'U'")

fields = arcpy.ListFields("unmatchtable")
field_names = [field.name for field in fields]

#Write a comma delimited file
f = open(outfile, "w")
w = csv.writer(f)
w.writerow(field_names)
for row in arcpy.SearchCursor("unmatchtable"):
    field_vals = [row.getValue(field.name) for field in fields]
    w.writerow(field_vals)
del row
f.close() #Finish writing all from buffer, so we can reformat

#Change delimiter from comma to pipe
f = open(outfile, "r+")
lines = [line for line in f]
f.seek(0)
for line in lines:
    line = line.replace(',','|')
    f.write(line)
f.close
