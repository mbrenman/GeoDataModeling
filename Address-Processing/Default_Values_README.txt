README for Default_Values
Matt Brenman
----------__________----------__________----------__________----------__________
Purpose:
        The Default Values modules is used to add in default values to a column
     (or all columns) of a delimited text table. This module is useful in 
     geocoding with ArcMap when using numeric fields, since ArcMap can cause
     issues with the data. ArcMap will sometimes create new columns when the
     data is loaded, which is usually fine, but when the base column (the
     column from which other columns are created) has an empty value, the data
     to the right of the base column are shifted to the left, which makes the 
     data much less useable and corrupts the data. 
        We have put in impossible values when making the default values. This
     way ArcMap does not destroy the data, and anybody looking at the data at a
     later point will be able to tell that the values are not to be taken as
     anything other than placeholders.

Use:
        The module requires a text input file (where the path can be a full path
     or the relative path from where the script resides). The user then should
     follow the prompts, adding default values until quitting, which writes to
     the new file.
        It should be noted, however, that the user cannot overwrite default
     values that were put in during a session. For example, if a column has an
     empty field and the user puts in, for example, the number 7 as the default
     for that column, the empty field will be filled. Any subsequent attempts to
     add a default value for that column will not make any changes, since the
     values in the field are no longer empty.
