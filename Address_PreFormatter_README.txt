README for Address_PreFormatter
Version 1 - Initial commit
Matt Brenman
----------__________----------__________----------__________----------__________
Purpose:
        The Address_PreFormatter is designed to parse addresses into their
     discrete fields, so that they can run on the Address_Getter and Error_Fixer
     modules, which utilize very separated information. This module attempts to
     split any address into the following pieces:
        -Street Number
           -Defined as a series of numbers followed by whitespace. This is the
            definition to avoid complication with streets like 5th street, but
            it does have issues with numbers like 111-a, which do not follow
            the format. This usually ends up with the number being concatenated
            with the street name, which does not cause a geocoding issue, but
            does make the Error_Fixer not as efficient
        -Street Direction
           -Defined as North, South, East, West, N, S, E, W, N., S., E., and W.
        -Street Name
           -Street names are taken after everything else, so that if there were
            fields with street name, they will have been removed and usually only 
            the street name will remain.
        -Street Suffix
           -Defined as lane, road, street, ln, rd, st, etc.
        -City
           -City, like the street name, is also taken as what is left over from
            the field after all else is removed. This is not a problem when the
            city and street name are in different fields, but (as of version 1),
            support for fields where the city and street share a field is not
            supported.
        -State
           -State is removed, since it is reinstated with the Address_Getter
            module. This will be updated in a later version so that bigger
            files spanning multiple states can be run through the entire loop
        -Zip Code
           -As of version 1, a zip code is only a string of 5 digits padded by
            whitespace or the end of the field. Support for 9 digit codes will
            be added.

Intersections:
        ArcMap supports the geocoding of intersections as well as street 
     addresses, so to deal with this, the program scans for repeats of 
     fields like street suffixes and directions, and when it finds multiple
     instances, it does not perform the specified field splitting. The program
     ignores, however, any possibility of intersection for fields like the city
     or zip code, since it is very unlikely that there would be multiple 
     instances of these in the row. It also would help the modules later on in 
     the loop to split them up as much as possible.

Fields containing notes:
        Sometimes the address data contains notes that are helpful to human
     readers but harmful to the success of the artificial reader. These notes
     could be, for example, something like: Allen Lane (by train station). 
     The note is not part of the address, so the geocoder will be confused.
     This is helpful to somebody trying to find use the information, so the
     notes are stored in another column. The default name is the current field
     containing the note with the string 'Notes' appended. If there is any
     conflict, then the program will prompt for another name.
        Notes can be removed in two formats, ones that come between two
     characters, such as street(note), or ones that come after just one
     character, such as street - note

A Note on Delimiters
        The modules in this system are formatted to accept any delimiter, but
     if the delimiter ever comes up in any of the fields, it will throw the 
     system off course. For this reason, I reccommend using a pipe, |, to
     delimit the input files, since it is much less likely to appear in any of
     the fields. If you are sure that a comma (or any other character) does not
     appear in any of the fields, feel free to use it as a delimiter.

From Excel to Pipe Delimited File
        Excel can export their files as CSV (comma delimited) and tab-delimited 
     files easily, but it is possible to export with any other delimiter. The
     steps to do this are outlined here: http://www.howtogeek.com/howto/21456/

To Do List:
     -Support ZIP4 codes
     -Keep state information (and multistate files)
     -Support street numbers with letters as well
     -Implement city/State differentiation
     -Clean up and comment code
