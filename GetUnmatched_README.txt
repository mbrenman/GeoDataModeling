README for GetUnmatched module
Created by Matt Brenman
Summer 2013
----------__________----------__________----------__________----------__________
Purpose: 
        To convert a geocoded set of points (with a corresponding shapefile
     result table containing all attributes) into a pipe delimited version
     of the unmatched addresses. This is used because it is redundant to
     re-geocode the matched addresses (which are on the scale of hundreds
     of thousands). This saves time in recoding addresses, and it allows us
     to see bigger picture errors in the file instead of limiting ourselves
     to each city (which we can still do if needed)
     Note: This module only keeps the same fields that are in the original
     address file and does not add in the extra fields created by ArcMap
Use:
       This tool should be imported into ArcMap as a tool in the toolbar.
     To do this, you may need to create a tool, and add a script by right
     clicking on the newly created toolbox and clicking - "Add Script".
     When asked for the script location, give the location of GetUnmatched.py,
     and when asked for parameters, put in:
     
             1) Name: GeoResult
                Type: Feature Class
                Description: The geocoding result from which the unmatched
                             addresses will be taken.
             2) Name: Address Text
                Type: Text File
                Description: The text file that was geocoded by ArcMap. This
                             is given so that the script can limit the output
                             to the same fields that were given. This limits
                             the size of the returned text, and also stops ArcMap
                             from adding the same field (with a slightly modified
                             name) each time.
             3) Name: Output Text
                Type: Text File
                Description: The text file into which the script will print the
                             addresses in a format that is compatible as input
                             for the address getting module.
                             
        When geocoding these results after they have been formatted and changed
     through the address getter module, you will likely have the problem that the
     fields for 'city' and 'street or intersection' do not come up with a match.
     You must manually scroll through the table and choose 'newAddress' for the
     'street or intersection' (NOTE: newAddress and newaddress are different, the
     all lowercase version is the previously created address, and will be different
     than newAddress if an error has been added to the error file that changes the 
     address).
        Once geocoded, you will receive a shapefile that can be run with the script
     again, which completes the loop.
