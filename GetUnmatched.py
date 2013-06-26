"""
Author: Matt Brenman

Purpose: To convert a geocoded set of points (with a corresponding shapefile
         result table containing all attributes) into a pipe delimited version
         of the unmatched addresses. This is used because it is redundant to
         re-geocode the matched addresses (which are on the scale of hundreds
         of thousands). This saves time in recoding addresses, and it allows us
         to see bigger picture errors in the file instead of limiting ourselves
         to each city (which we can still do if needed)
         Note: This module only keeps the same fields that are in the original
         address file and does not add in the extra fields created by ArcMap.

"""

import arcpy

georesult = arcpy.GetParameterAsText(0)
origtext = arcpy.GetParameterAsText(1)
outfile = arcpy.GetParameterAsText(2)

output_file = open(outfile, "w")

#Get header from original address file
desc = arcpy.Describe(origtext)
fields = desc.Fields

#Get field names from address file
field_names = []
for field in fields:
    if ((str)(field.name) == 'city'):
        field_names.append('city_1') #Arcmap changes city to city_1 at entry
    else:
        field_names.append((str)(field.name))

#Get field names from the ArcMap Table
desc2 = arcpy.Describe(georesult)
geofields = []
for f in desc2.Fields:
    geofields.append((str)(f.name))

#Handle differences between the two tables
#Forces the keys of the first arg table to be a subset of keys of the
#second table. Both inputs must be tables.
for f in field_names[:]: #make a copy of the list, so that we are iterating
                         #over a non-changing list
    if not f in geofields:
        field_names.remove(f)

#Write header
for i in range(len(field_names)):
    val = (str)(field_names[i])
    val = val.rstrip()
    output_file.write(val)
    if i < (len(field_names) - 1):
        output_file.write('|')
    else:
        output_file.write('\n')

#Get SearchCursor for all unmapped addresses and pull field_names
cur  = arcpy.da.SearchCursor(georesult, field_names, "Status = 'U'")

#Print all unmatched addresses
for row in cur:
    for i in range(len(row)):
        val =(str)(row[i])
        val = val.rstrip()
        output_file.write(val)
        if i < (len(row) - 1):
            output_file.write('|')
        else:
            output_file.write('\n')

output_file.close()



