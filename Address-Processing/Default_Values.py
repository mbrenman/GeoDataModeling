#-------------------------------------------------------------------------------
# Name:        Default Fields
# Purpose:     The Default Values modules is used to add in default values to a 
#              column (or all columns) of a delimited text table.
#
# Author:      Matt Brenman
#
# Created:     20/06/2013
#-------------------------------------------------------------------------------

delimiter = '|'

def main():
    global delimiter
    delimiter_change = raw_input('Enter file delimiter or Enter to skip.\n'
                                 'Default is | (pipe)')
    if (delimiter_change != ''): delimiter = delimiter_change
    data_file = get_file('input', 'r')
    type_list = read_header(data_file) #Contains a list of the type of each
                                       #section of data (ex. streetname, city)
    accts = organize(type_list, data_file)
    show_fields(type_list, accts)

def get_file(filetype, use='r', filename=''):
    if filename == '':
        #No name given to function
        filename = raw_input('What is the %s file name?\n' % filetype)
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
    filename = raw_input('Enter output filename')
    writefile = get_file('output', 'w',filename)

    name = ''
    while name.lower() != 'quit':
        name = raw_input("Add default value to which field?\n\
                          Type the field name,\n\
                          Type 'All' for all fields\n\
                          Type 'Refresh' to print all names\n\
                          Type 'Quit' to quit\n")
        if name.lower() == 'refresh':
            for field in type_list:
                print field,
        elif name.lower() != 'quit':
            defaultVal = raw_input("Enter default value:\n")
            if name.lower() == 'all':
                for field in type_list:
                    add_default(accts, field, defaultVal)
            else:
                if name.lower() in type_list:
                    add_default(accts, name.lower(), defaultVal)
                else:
                    print "Field name not in table."
    print_addresses_to_file(accts, writefile, type_list)

def add_default(accts, field, defaultVal):
    for acct in accts:
        if acct[field] == '':
            acct[field] = defaultVal

def print_addresses_to_file(accts, address_file, type_list):
    sorted_keys = sort_keys(type_list)
    print_header(sorted_keys, address_file)
    print_customers(accts, address_file, sorted_keys)

def sort_keys(type_list):
    return sorted(set(type_list))

def print_header(sorted_keys, address_file):
    for i in range(len(sorted_keys)):
        address_file.write(sorted_keys[i])
        if i != len(sorted_keys) - 1:
            address_file.write(',')
        else:
            address_file.write('\n')

def print_customers(accts, address_file, sorted_keys):
    for acct in accts:
        for i in range(len(sorted_keys)):
            field_data = str(acct[sorted_keys[i]])
            address_file.write(field_data)
            if i != len(sorted_keys) - 1:
                address_file.write(',')
            else:
                address_file.write('\n')


if __name__ == '__main__':
    main()
