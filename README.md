GeoDataModeling
===============

Summer 2013 - A collection of work done for GeoDataModelers, Inc., the GIS contractor to the Aqua America company Engineering Department in Bryn Mawr, PA.

This series of modules works to format and fix errors in addresses to move from a delimited file to a file that works in the ArcGIS software.

The most significant modules are as follows:

  Address Pre-Formatter:
        The Address_PreFormatter is designed to parse addresses into their
     discrete fields, so that they can run on the Address_Getter and Error_Fixer
     modules, which utilize very separated information. This module attempts to
     split any address into the following pieces:
     
  Address Getter:
        The Address Getter module is used to organize and format the address 
     information that is given in a file. The main stages of this module are data
     collection, data cleaning, data formatting, and printing, which are all 
     explained in more detail in the documentation.
     
  Error Fixer:
       This module changes addresses that are known to be false with a set of
     given corrections, and returns an updated version of the structure that was
     passed as an arguemnt. The format for the structure is given in the
     documentation of the Address_Getter module.
     
  Get Unmatched:
        To convert a geocoded set of points (with a corresponding shapefile
     result table containing all attributes) into a pipe delimited version
     of the unmatched addresses. This is used because it is redundant to
     re-geocode the matched addresses (which are on the scale of hundreds
     of thousands). This saves time in recoding addresses, and it allows us
     to see bigger picture errors in the file instead of limiting ourselves
     to each city (which we can still do if needed)
     
The auxiliary modules are:

  Unique Fields:
        To allow for a user to insert a delimited text table (with any delimiter)
     and to either print out the uniqueness of each field (yes or no) or print 
     out all of the unique values of a each field. All operations can be done on 
     one or all fields, and the results are printed to a file provided by the user.
     
  File Splitter:
        The File_Splitter is used to split a text file that contains a column
     header into multiple text files while keeping all data and formatting and 
     keeping the header in each file.
