GeoDataModeling
===============

Troubleshooting:

    Problem: When geocoding a large number of addresses, ArcMap quits with the 
             error "Create Feature Class: There was an error trying to process 
             this table."
        Solution: Break up the large address file into two files, but make sure
                  to copy the header onto both. This problem seems to arise due
                  to server limitations or a problem with the ArcGIS software
                  that cannot deal with the size of the files. This problem
                  first appeared when adding in all of the extra fields from the
                  banner file, so it is not the number of addresses, but more
                  the amount of data in the table. It can then be combined after
                  both sets are geocoded

    Problem: ArcMap doesn't know which field to use for "Street or Intersection"
        Solution: The standard field name that is added with the fixed address
                  is called "newAddress", so that should be used for geocoding
                  the addresses. When looping with the Get_Unmatched tool, there
                  is no need to worry about overwriting this field, since it will
                  either be filled with the same information or more updated 
                  information.
                  
    Problem: ArcMap doesn't know which field to use for "City"
        Solution: The standard field name that is used for the city (from the
                  banner files) is 'city', which is usually what the answer is.
                  The field name will change, however, if the GetUnmatched tool
                  is used. ArcMap does not allow a user's field name to be city,
                  so upon geocoding (which is necessary to use the GetUnmatched
                  tool in the first place), ArcMap changes the name to 'city_1'.
                  
    Problem: ArcMap doesn't know which field to use, and the above didn't help.
        Solution: If none of the suspected field names are in the pull-down menu,
                  you should either check the text file, or run the unique fields
                  module and find the name under which the information in question
                  is listed.
                  
