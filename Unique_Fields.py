#-------------------------------------------------------------------------------
# Name:        Unique Fields
# Purpose:     To allow for a user to insert a delimited text table (with
#              any delimiter) and to either print out the uniqueness of each
#              field (yes or no) or print out all of the unique values of
#              a each field.
#              All operations can be done on one or all fields, and the results
#              are printed to a file provided by the user.
#
# Author:      Matt Brenman
#
# Created:     20/06/2013
#-------------------------------------------------------------------------------

delimiter = '|'

def main():
    global delimiter
    delimiter_change = raw_input("Enter file delimiter or Enter to skip.\n\
                                  Default is '|'.")
    if (delimiter_change != ''): delimiter = delimiter_change
    data_file = get_file('address', 'r')
    type_list = read_header(data_file) #Contains a list of the type of each
                                       #section of data (ex. streetname, city)
    accts = organize(type_list, data_file)
    show_fields(type_list, accts)

def get_file(filetype, use='r', filename=''):
    if filename == '':
        #No name given to function
        filename = raw_input("What is the %s file name?\n" % filetype)
    try:
        data_file = open(filename, use)
    except IOError:
        print '%s file cannot be found.' % filetype,
        if not '.txt' in filename: print 'Did you forget the extension?',
        print 'Please try again'
        return get_file(filetype, use)
    else:
        return data_file

def read_header(data_file):
    """ Extracts the header information (column names) from the raw data """
    type_line = (data_file.readline()).strip()
    #All column names are forced to lowercase to avoid case errors
    type_line = type_line.lower()
    type_list = type_line.split(delimiter)
    return type_list

def organize(type_list, client_file):
    """ Puts all client data in a dictionary
        accessed by unique account number """
    accts = []
    for line in client_file:
        info = line.split(delimiter) #Raw single-client data
        client_dict = {}
        if (len(type_list) <= len(info)):
            for i in range(len(type_list)):
                client_dict[type_list[i]] = info[i].strip('\n') #Attach each bit of client
                                                    #data to the correct type
            accts.append(client_dict) #Add client to list of all clients
        else:
            #Catches incomplete client data with fewer fields than necessary
            print "Error with client: ", info
    return accts

def show_fields(type_list, accts):
    filename = raw_input('Enter output filename, ' +
                         'or hit Enter to use the default (Unique.txt)')
    if filename == '': filename = 'Unique.txt'
    writefile = get_file('output', 'w',filename)

    unique_vals = {}
    name = ''
    while name.lower() != 'quit':
        name = raw_input("Which field would you like to analyze?\n\
                          Type the field name,\n\
                          Type 'All' for all fields\n\
                          Type 'Refresh' to print all names\n\
                          Type 'Quit' to quit\n")
        if name.lower() == 'refresh':
            for field in type_list:
                print field,
        elif name.lower() != 'quit':
            analysis = raw_input('Would you like to:\n\
                              1) Print all values and frequencies\n\
                              2) Print if field is unique\n')
            if name.lower() == 'all':
                for field in type_list:
                    if analysis == '1': write_unique_to_file(writefile, accts, field)
                    elif analysis == '2': is_unique(writefile, accts, field)
            else:
                if name.lower() in type_list:
                    if analysis == '1': write_unique_to_file(writefile, accts, name.lower())
                    elif analysis == '2': is_unique(writefile, accts, name.lower())
                else:
                    print "Field name not in table."

def write_unique_to_file(writefile, accts, field):
    unique_vals = {}
    writefile.write("Unique instances of: %s\n" % field)
    for acct in accts:
        if acct[field] not in unique_vals:
            unique_vals[acct[field]] = 1
        else:
            unique_vals[acct[field]] += 1
    sorted_keys = {key for key in unique_vals}
    sorted_keys = sorted(sorted_keys)
    for key in sorted_keys:
        writefile.write("   %s : %s\n" % (key, unique_vals[key]))

def is_unique(writefile, accts, field):
    unique_vals = {}
    writefile.write("%s has repeats: " % field)
    for acct in accts:
        if acct[field] not in unique_vals:
            unique_vals[acct[field]] = 1
        else:
            writefile.write("Yes\n")
            return False
    writefile.write("No\n")
    return True

if __name__ == '__main__':
    main()
