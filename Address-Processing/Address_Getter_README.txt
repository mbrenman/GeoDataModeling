README for Address_Getter module
Created by Matt Brenman
Summer 2013
----------__________----------__________----------__________----------__________
Purpose:
        This module is used to Organize and format the address information that
     is given in a Banner file. The main stages of this module are data
     collection, data cleaning, data formatting, and printing.

Significant Stages:
--Data Collection
        Data collection is the only time that the Banner file is opened and 
     examined. At runtime, there will be multiple prompts for the user, the first
     of which is whether or not the Banner file follows the company standards for
     field names. If the user says yes, the program continues. Otherwise, the
     user is given the option to change each field name to a different name. It
     should be noted that capitalization does not matter, and a field such as
     'MeterNotes' is the same (according to this script) as 'meternotes'.
--Data Cleaning / Data Formatting:
        After the data is collected and organized, a menu pops up, where the user
     is given the option of printing the addresses to a file, to the interpreter,
     or exiting the program. If the user chooses to print the addresses, the script
     will format the addresses. This is combined with cleaning the data, which is
     done with the Error_Fixer module (see Error_Fixer_README.txt for more info).
        Data formatting consists of fixing the case of all fields, removing 
     unneccessary spacing, and removing puncuation in addresses.
--Printing
        When printing the information to a file, the user will be prompted for a
     file name. If the file already exists, it will be overwritten, so the user
     should take care with not choosing files that they wish to keep.
        When printing, the user will be given the option of limiting the addresses
     that they print. This is useful if they only want to work with a smaller data
     set than an entire banner file. This works with a simple string search of the
     entire address.

Implementation:
--Data Structures:
        The main data structure in this module is the address list. The address list
     is a list of dictionaries, where each is indexed by field names given by
     the banner file. Each list element contains the information of one customer.
     This makes it easy to format each address when needed, since 
     it allows the script to pull out the necessary fields in a way that is easy to
     follow.
--Formatting
        This module does a little bit of error fixing by removing leading zeroes from
     the street number and formatting the zip codes to follow XXXXX-XXXX or XXXXX 
     format
