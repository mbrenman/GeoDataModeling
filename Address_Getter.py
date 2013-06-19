#-------------------------------------------------------------------------------
# Name:        File Examiner
# Purpose:
#
# Author:      Matt Brenman
#
# Created:     28/05/2013
# Copyright:   (c) Joe 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import string #Used to remove punctuation from addresses
import Error_Fixer

def main():
    global State
    data_file, type_list = get_file()
    curState = raw_input("Which US State does this data describe?\n")
    acct_numbers = organize_by_acct_num(type_list, data_file)
    menu(acct_numbers)
    data_file.close()

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

def menu(acct_numbers):
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
                address_list = make_addresses(acct_numbers)
                address_list_made = True
            print_addresses(address_list)
        elif (operation == '2'):
            out_file = raw_input('What is the output file name?\n'
                                 'Caution: Using a file name that already\n'
                                 'exists will overwrite the existing file\n')
            address_file = open(out_file, 'w')
            if (not address_list_made):
                address_list = make_addresses(acct_numbers)
                address_list_made = True
            limit_to_string = raw_input('Would you like to limit the search?\n'
                                        '1: Yes\n2: No\n')
            if (limit_to_string == '1'):
                limit = raw_input('Enter search string\n')
                limit = limit.lower()
                print_addresses_to_file(address_list, address_file, limit)
            else:
                print_addresses_to_file(address_list, address_file, '')
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

def organize_by_acct_num(type_list, client_file):
    """ Puts all client data in a dictionary
        accessed by unique account number """
    acct_numbers = {}
    for line in client_file:
        info = line.split(delimiter) #Raw single-client data
        client_dict = {}
        if (len(type_list) <= len(info)):
            for i in range(len(type_list)):
                client_dict[type_list[i]] = info[i] #Attach each bit of client
                                                    #data to the correct type
                if type_list[i] == 'city_1': #For recoding, arcmap changes
                    client_dict[City] = info[i] #city to city_1
            if good_acct(client_dict):
                #if 'meternotes' exists, check for disqualifiers
                acct_numbers[client_dict[Account]] = client_dict
                #Add client to list of all clients by acct number ('premises')
        else:
            #Catches incomplete client data with fewer fields than necessary
            print "Error with client: ", info
    return acct_numbers

def make_addresses(client_data):
    """ Extracts and formats relevant address data from client data """
    address_list = []
    for client_key in client_data:
        new_address = {}
        client = client_data[client_key]
        new_address[FirstName] = remove_punctuation(client[FirstName])
        new_address[LastName] = remove_punctuation(client[LastName])
        new_address[ServiceType] = remove_punctuation(client[ServiceType])

        client_addr = fix_address(client_data[client_key])
        #Set street information
        new_address[newAddress] = client[StreetNum]
        if client_addr[Direction] != "":
            new_address[newAddress] += " " + fix_case(client_addr[Direction])
        new_address[newAddress] += " " + fix_case(client_addr[StreetName]) +  \
                                 " " + fix_case(client_addr[StreetSuffix])
        new_address[newAddress] = remove_bad_spaces(new_address[newAddress])
        new_address[Zip] = client_addr[Zip]
        new_address[City] = fix_case(client_addr[City])
        new_address[State] = client_addr[State].upper()
        #Keep split up address info for reprocessing after geocoding
        new_address[StreetNum] = remove_punctuation(client_addr[StreetNum])
        new_address[Direction] = remove_punctuation(client_addr[Direction])
        new_address[StreetName] = remove_punctuation(client_addr[StreetName])
        new_address[StreetSuffix] = remove_punctuation(client_addr[StreetSuffix])
        new_address[Account] = remove_punctuation(client_key)

        full_address = format_address(new_address)
        address_list.append(full_address)
    return address_list

def good_acct(client):
    if 'meternotes' in client:
        if "bad acct" in client['meternotes'].lower():
            return False
        if "do not use" in client['meternotes'].lower():
            return False
        if "don't use" in client['meternotes'].lower():
            return False
        if "delete these accts" in client['meternotes'].lower():
            return False
    return True

def fix_address(raw_address):
    """ Calls the error fixing module to resolve known errors in the data """
    edit_address = {}
    edit_address[StreetNum] = remove_leading_zeros(raw_address[StreetNum])
    edit_address[Direction] = raw_address[Direction].lower()
    edit_address[StreetName] = raw_address[StreetName].lower()
    edit_address[StreetSuffix] = raw_address[StreetSuffix].lower()
    edit_address[Zip] = format_zipcodes(raw_address[Zip])
    edit_address[City] = raw_address[City].strip().lower()
    edit_address[State] = curState
    return Error_Fixer.fix_addresses(ERRORS, edit_address)

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

def format_address(new_address):
    """ Joins relevant fields to conform to the standard output format """
    full_address = new_address[FirstName] + ',' +                      \
                   new_address[LastName] + ',' +                       \
                   new_address[ServiceType] + "," +                    \
                   remove_punctuation(new_address[newAddress]) + "," + \
                   new_address[City] + "," +                           \
                   new_address[State] + ',' +                          \
                   new_address[Zip][0]
    if (new_address[Zip][1] != '') and (new_address[Zip][1] != '0000'):
        full_address += '-' + new_address[Zip][1]
    full_address += ',' + new_address[StreetNum] + ',' +               \
                    new_address[Direction] + ',' +                     \
                    new_address[StreetName] + ',' +                    \
                    new_address[StreetSuffix] + ',' +                  \
                    new_address[Account]
    fix_case(full_address)
    return full_address

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
    for punc in string.punctuation:
        line = line.replace(punc, "")
    return line

def too_many_dashes(zipcode):
    """ Checks for more than one '-' in a zip code
        (XXXXX-XXXX or XXXXX) is normal """
    count = 0
    for zipdigit in zipcode:
        if zipdigit == '-': count += 1
    if count > 1: return True
    return False

def print_addresses_to_file(address_list, address_file, limit):
    address_file.write(FirstName + ',' + LastName + ',' + ServiceType + ',' +
                       newAddress + ',' + City + ',' + State + ',' + Zip + ',' +
                       StreetNum + ',' + Direction + ',' + StreetName + ',' +
                       StreetSuffix + ',' + Account + '\n')
                       #Header with column names
    for address in address_list:
        empty_test = address.replace(',','')
        empty_test = empty_test.replace(' ','')
        if empty_test != '':
            if limit != '':
                if limit in address.lower():
                    address_file.write(address + "\n")
            else:
                address_file.write(address + "\n")

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
    curState = "PA"
    newAddress = 'newAddress'
    changeFields = raw_input('Would you like to change any field names? (y/n)')
    if changeFields == 'y': fix_field_names()
    ERRORS = Error_Fixer.error_setup(Zip)
    main()
