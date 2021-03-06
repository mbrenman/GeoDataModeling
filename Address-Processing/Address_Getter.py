#-------------------------------------------------------------------------------
# Name:        File Examiner
# Purpose:     To extract and format customer files that follow a certain
#              format (which is lenient), and also to facilitate the fixing of
#              errors using the Error_Fixer.py module. This project was created
#              for GeoDataModelers, Inc., the GIS contractor for the Aqua
#              America Engineering Department in Bryn Mawr, PA location.
#
# Author:      Matt Brenman
#
# Created:     28/05/2013
#-------------------------------------------------------------------------------

import string #Used to remove punctuation from addresses
import Error_Fixer

#Global Variables -- Can be overwritten if a file with different
#headers is given (Will be prompted at runtime)
delimiter = '|'
StreetNum = "streetnumb"
Direction = "pdir"
StreetName = "streetname"
StreetSuffix = "ssfx"
City = "city"
Zip = "zip"
Account = "premises"
State = "state"
FirstName = "firstname"
LastName = "lastname"
ServiceType = "servicetyp"
newAddress = 'newAddress'

def main():
    Errors = setup()
    data_file, type_list = get_file()
    accts = organize_by_acct(type_list, data_file)
    menu(accts, type_list, Errors)
    data_file.close()

def setup():
    changeFields = raw_input('Would you like to change any field names? (y/n)')
    if changeFields == 'y': fix_field_names()
    return Error_Fixer.error_setup([State, City, Zip, StreetNum, StreetName, Direction, StreetSuffix], Zip)

def fix_field_names():
    global StreetNum, Direction, StreetName, StreetSuffix, City, Zip, Account, \
           State, FirstName, LastName, ServiceType, delimiter
    StreetNum = prompt_global_change(StreetNum, "Street Number")
    Direction = prompt_global_change(Direction, "Direction")
    StreetName = prompt_global_change(StreetName, "Street Name")
    StreetSuffix = prompt_global_change(StreetSuffix, "Street Suffix")
    City = prompt_global_change(City, "City")
    Zip = prompt_global_change(Zip, "Zip")
    Account = prompt_global_change(Account, "Account")
    FirstName = prompt_global_change(FirstName, "First Name")
    LastName = prompt_global_change(LastName, "Last Name")
    ServiceType = prompt_global_change(ServiceType, "Service Type")
    delimiter = prompt_global_change(delimiter, "Delimiter")

def prompt_global_change(field, name):
    change = raw_input('Change %s from %s? (y/n)\n' % (name, field))
    if change.lower() == 'y':
        newName = raw_input('Enter new Name for %s\n' % name)
        return newName.lower()
    return field

def get_file():
    filename = raw_input("What is the address file name?\n")
    try:
        data_file = open(filename, "r")
        type_list = read_header(data_file) #Contains a list of the type of each
                                      #section of data (ex. streetname, city)
    except IOError:
        print 'Address file cannot be found.',
        if not '.txt' in filename: print 'Did you forget the extension?',
        print 'Please try again'
        return get_file()
    else:
        return data_file, type_list

def menu(accts, type_list, Errors):
    """ A menu that allows the user to choose which operation to perform """
    address_list = []
    address_list_made = False #Allows address list to only be made once

    operation = '0'
    while operation != '3':
        operation = raw_input('What would you like to do? (Enter number) \n'
                              '1: Print all addresses\n'
                              '2: Print addresses to file\n'
                              '3: Exit\n')
        if (operation == '1'):
            if (not address_list_made):
                make_addresses(accts, Errors)
                address_list_made = True
            print_addresses(accts)
        elif (operation == '2'):
            out_file = raw_input('What is the output file name?\n'
                                 'Caution: Using a file name that already\n'
                                 'exists will overwrite the existing file\n')
            address_file = open(out_file, 'w')
            if (not address_list_made):
                make_addresses(accts, Errors)
                address_list_made = True
            limit_to_string = raw_input('Would you like to limit '
                                        'the search to a city?\n'
                                        '1: Yes\n2: No\n')
            if (limit_to_string == '1'):
                limit = raw_input('Enter city name\n')
                limit = limit.lower()
                print_addresses_to_file(accts, address_file, type_list, limit)
            else:
                print_addresses_to_file(accts, address_file, type_list, '')
            address_file.close()

def read_header(data_file):
    """ Extracts the header information (column names) from the raw data """
    type_line = (data_file.readline()).strip()
    #All column names are forced to lowercase to avoid case errors
    type_line = type_line.lower()
    type_list = type_line.split(delimiter)
    #Shorten each to 10 characters for compatability with other modules
    for i in range(len(type_list)):
        if len(type_list[i]) > 10:
            type_list[i] = type_list[i][:10]
    return type_list

def organize_by_acct(type_list, client_file):
    """ Puts all client data in a list by acct"""
    accts = []
    for line in client_file:
        info = line.split(delimiter) #Raw single-client data
        client_dict = {}
        if (len(type_list) <= len(info)):
            for i in range(len(type_list)):
                client_dict[type_list[i]] = info[i] #Attach each bit of client
                                                    #data to the correct type
                if type_list[i] == 'city_1': #For recoding, arcmap changes
                    client_dict[City] = info[i] #city to city_1
            accts.append(client_dict)
            #Add client to list of all clients by acct number ('premises')
        else:
            #Catches incomplete client data with fewer fields than necessary
            print "Error with client: ", info
    return accts

def make_addresses(accts, Errors):
    """ Extracts and formats relevant address data from client data """
    for client in accts:
        client_addr = fix_address(client, Errors)
        #Set street information
        client[newAddress] = combine_addr_data(client_addr)
        #Keep split up address info for reprocessing after geocoding
        for key in client_addr:
            if key != Zip:
                client[key] = client_addr[key]
        for field in client:
            #Remove newlines from all fields, including zipcode
            client[field] = client[field].rstrip('\n')
            if field != Zip: #Don't want to remove '-' from zipcodes
                client[field] = remove_punctuation(client[field])

def combine_addr_data(client_addr):
    new_addr = client_addr[StreetNum]
    if client_addr[Direction] != "":
        new_addr += " " + client_addr[Direction]
    new_addr += " " + client_addr[StreetName] + " " + client_addr[StreetSuffix]
    new_addr = fix_case(new_addr)
    return remove_bad_spaces(new_addr)

def fix_address(raw_address, Errors):
    """ Calls the error fixing module to resolve known errors in the data """
    edit_address = {}
    edit_address[StreetNum] = remove_leading_zeros(raw_address[StreetNum])
    edit_address[Direction] = raw_address[Direction].lower()
    edit_address[StreetName] = raw_address[StreetName].lower()
    edit_address[StreetSuffix] = raw_address[StreetSuffix].lower()
    edit_address[Zip] = format_zipcodes(raw_address[Zip])
    edit_address[City] = raw_address[City].strip().lower()
    edit_address[State] = raw_address[State]
    return Error_Fixer.fix_addresses(Errors, edit_address)

def format_zipcodes(zipcode):
    """ Separates zipcodes into a list of ['xxxxx','xxxx'] where
        the fields are the 5 digit code and the 4 digit code, if available """
    zip_list = []
    if too_many_dashes(zipcode):
        if (len(zipcode) > 5):
            zip_list = [zipcode[:5], ""]
        else:
            zip_list = ["", ""]
    else:
        zip_list = zipcode.split('-') #(XXXXX-XXXX or XXXXX)
        if (len(zip_list) == 1):
            zip_list.append("")
    return zip_list

def zip_to_string(zipcode):
    zip_string = zipcode[0]
    if zipcode[1] != '':
        zip_string += '-' + zipcode[1]
    return zip_string

def fix_case(words):
    """ Puts words in mixed case, where only first letter is capitalized """
    fixed_list = []
    new_word = ''
    for word in words.split():
        if len(word) == 1:
            new_word = word[0].upper()
        else:
            new_word = word[0].upper() + word[1:]
        fixed_list.append(new_word)
    space_delimiter = ' '
    return space_delimiter.join(fixed_list)

def remove_punctuation(line):
    for punc in [',', '\"', '\'']:
        line = line.replace(punc,'')
    return line

def too_many_dashes(zipcode):
    """ Checks for more than one '-' in a zip code
        (XXXXX-XXXX or XXXXX) is normal """
    count = 0
    for zipdigit in zipcode:
        if zipdigit == '-': count += 1
    if count > 1: return True
    return False

def print_addresses_to_file(accts, address_file, type_list, limit):
    sorted_keys = sort_keys(type_list)
    print_header(sorted_keys, address_file)
    print_customers(accts, address_file, sorted_keys, limit)

def sort_keys(type_list):
    sorted_keys = []
    for key in type_list:
        sorted_keys.append(key)
    sorted_keys.append(newAddress)
    return sorted(sorted_keys)

def print_header(sorted_keys, address_file):
    for i in range(len(sorted_keys)):
        address_file.write(remove_punctuation(sorted_keys[i]))
        if i != len(sorted_keys) - 1:
            address_file.write(',')
        else:
            address_file.write('\n')

def print_customers(accts, address_file, sorted_keys, limit):
    for acct in accts:
        if limit in acct[City]:
            for i in range(len(sorted_keys)):
                field_data = str(acct[sorted_keys[i]])
                if len(field_data) < 253:
                    address_file.write(field_data)
                if i != len(sorted_keys) - 1:
                    address_file.write(',')
                else:
                    address_file.write('\n')

def print_addresses(address_list):
    print "street,city,state,zip" #Header with column names
    for address in address_list:
        print address

def remove_leading_zeros(number):
    non_zero = False
    zeros_removed = ''
    for digit in number:
        if (digit != '0'):
            non_zero = True
        if non_zero == True:
            zeros_removed += digit
    return zeros_removed

def remove_bad_spaces(address):
    address = address.replace('  ', ' ') #Removing double spaces
    length = len(address)
    if len != 0:
        #Removing leading spaces
        while len(address) > 1 and address[0] == ' ':
            address = address[1:]
        #Removing ending spaces
        while len(address) > 1 and address[len(address) - 1] == ' ':
            address = address[:len(address) - 1]
    return address

if __name__ == '__main__':
    main()
