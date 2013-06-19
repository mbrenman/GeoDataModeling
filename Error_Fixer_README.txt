README for Error_Fixer module
Created by Matt Brenman
Summer 2013
----------__________----------__________----------__________----------__________
Purpose:
        This module changes addresses that are known to be false with a set of
     given corrections, and returns an updated version of the structure that was
     passed as an arguemnt. The format for the structure is given in the
     documentation of the Address_Getter module.

Usage:
--File/Header Format:
        You must have a file called "Error_file.txt" in the same directory as
     this module when running an application that uses its functions. The format
     of this error file is a header followed by the list of corrections, where
     the standard header is: "State|City|Zip|StreetNumber|StreetName|Pdir|Ssfx"
     The header contains the column names for the vertical bar delimited
     corrections. The names were taken from the Address_Getter module, since that
     is the standard format for address data.
--Changes Format:
        There is only one address change allowed per line, although as many
     fields as needed can be changed in a line. Each column must be separated by
     a vertical bar. If the field is not changed and is not used to identify
     which addresses should be changed, the field should be left blank (although
     there should still be a vertical bar left before and after the field).
        When a field is used to identify which changes should be made (ex.
     Change all addresses in Philadelphia), the field should only contain the
     identifier (...|Philadelphia|...). When a field needs to be updated, the
     format is: identifier[comma]update. For example, if you wanted to change 
     all of the addresses in Philadelphia to be in the city of Boston, you would
     write (...|Philadelpia,Boston|...). Note: Spaces here do matter, and 
     (...|Philadelpia, Boston|...) will make every city have the name " Boston"
     and not "Boston"
        When there is no specific field instance that you need to update, but
     you need all instances of that field updated (limited by the other fields),
     you leave the identifier blank. If you wanted to change every city to 
     Boston, despite what the current city said, you would write 
     (...|,Boston|...). Every address that fit the  other specifications would 
     have the city changed to Boston.
--Examples
     State|City|Zip|StreetNumber|StreetName|Pdir|Ssfx
     PA|Bala,Bala Cynwyd|||||
     PA|West Chester|19382||Pheasant Run||Lane,Rd
     PA|Media|19063||Old baltimore|,E|Pike

         The first changes every city in Pennsylvania that has the name "Bala" to 
     the name "Bala Cynwyd" which is useful for correcting shorthand on forms
         The second is a change from Pheasant Run Lane to Pheasant Run Rd for 
     every instance of Pheasant Run Lane in West Chester, PA 19382.
         The third is adds "E" to Old baltimore Pike when it is in Media, PA
     19063. Since there are multiple instances of Old Baltimore outside of Media
     that are not E Old Baltimore, we have to restrict our search to only those
     within Media, PA 19063.
--Adding Errors
        Errors can be manually typed into the error file, but they can also
     be added with the help of the error fixer. If the error fixer is run alone
     (which will run it as the main program), it will enter "add mode" where it
     assists the user in adding errors to the error file in the correct format.
        To run this, the user can either double click on the .py file from a
     graphical window, or run "python error_fixer.py" from the command line

Notes:
        A call to error_setup() must be performed before calling 
     fix_addresses(...), and the value returned from error_setup must be passed
     into fix addresses along with the address to fix. This is because the error
     fixing module operates on one address at a time and it would be very time
     intensive to reread and recreate the error list every time (the entire 
     PA banner file is ~400,000 records, so if the setup only took .001 seconds,
     it would still add 6 minutes to the routine, which would more than double
     the time).

Implementation:
--Data Structures
        The error fixing module reads the formatted list of known errors into
     a list of dictionaries. Each dictionary maps to one line in the error file,
     where it contains each correction and limiter to the data. The list is the
     collection of all of these dictioanries, and every address passed into the
     module is checked against every error case.
--Cascading Errors
        If an error is found, the correct changes are made, and the revised
     address is then recursively compared (again) against all of the errors. 
     This is done so that multiple changes can be made without overly 
     complicated setup. It also gets rid of the need for repetitive errors.
     For example, there is a string of made-up addresses on 
     "111 grand rd, phila, PA" and there are also many on 
     "222 grand rd, philadelphia, PA". The road should be "grand st, wyndmoor, pa".
     We could make a case for each of these roads, but we could also realize
     that the abbreviation "phila" comes up for "philadelphia" multiple times
     on different addresses, so instead of having multiple errors for each one,
     we can simply have the fix of "phila" to "philadelphia," and then every
     address that needs to be fixed with both "phila" and "philadelphia" and
     another change only needs one line instead of two. This greatly reduces the
     size of the error file, and it also lets the person finding errors not
     worry too much about small details.
        One must be careful, however, since if the change from "phila" to
     "philadelphia" is made, then any error fixing "grand rd, phila, pa" is not
     guaranteed to work. A change to "grand rd, philadelphia, pa" will
     definitely work.
