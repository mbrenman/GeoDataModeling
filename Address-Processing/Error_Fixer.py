#-------------------------------------------------------------------------------
# Name:        Error Fixer
# Purpose:     To correct address data against a formatted set of known errors
#              that follows a standard documented in the README when run from
#              another program. When run as the main script, it allows for the
#              addition of errors to the known error databank.
#
# Author:      Matt Brenman
#
# Created:     28/05/2013
#-------------------------------------------------------------------------------

#Global varibles
DELIMITER = '|'
ZIP = 'zip' #Placeholder for zip

def error_setup(header, Zip):
    error_file = get_error_file('r')
    header_list = header
    errors = organize(header_list, error_file)
    error_file.close()
    ZIP = Zip #Zip needs to be singled out because of formatting differences
    return errors

def get_error_file(usage, filename='Error_file.txt'):
    try:
        error_file = open(filename, usage)
    except IOError:
        errMsg = '%s not found.' % filename
        if not '.txt' in filename: errMsg += ' Did you forget the extension?'
        print errMsg
        newName = raw_input('Please enter a different error file filename\n')
        return get_error_file(usage, newName)
    else:
        return error_file

def fix_addresses(errors, address):
    find_matches(errors, address)
    return address

def organize(header_list, error_file):
    errors = []
    for line in error_file:
        info = line.split(DELIMITER) #Raw single-client data
        error_dict = {}
        if (len(header_list) <= len(info)):
            for i in range(len(header_list)):
                error_data = info[i].strip("\n").lower()
                error_dict[header_list[i]] = error_data.split(',')
                #Attach each bit of data to the correct type
            errors.append(format_error_zips(error_dict))
        else:
            #Catches incomplete client data with fewer fields than necessary
            print "Error with format: ", info
    return errors

def format_error_zips(error_dict):
    if ZIP in error_dict:
        for i in range(len(error_dict[ZIP])):
            zipcode = error_dict[ZIP][i]
            zip_list = []
            if too_many_zip_dashes(zipcode):
                if (len(zipcode) > 5):
                    zip_list = [zipcode[:5], ""]
                else:
                    zip_list = ["", ""]
            else:
                zip_list = zipcode.split('-') #(XXXXX-XXXX or XXXXX)
                if (len(zip_list) == 1):
                    zip_list.append("")
            error_dict[ZIP][i] = zip_list
    return error_dict

def too_many_zip_dashes(zipcode):
    count = 0
    for zipdigit in zipcode:
        if zipdigit == '-': count += 1
    if count > 1: return True
    return False

def find_matches(errors, address):
    for error in errors:
        if error_match(error, address):
            old_address = create_record(address)
            correct(error, address)
            if old_address != address:
               find_matches(errors, address) #Recursive call to see if the new
                                             #format has any more changes
                                             #but only if a change has been made

def create_record(unchanged_address):
    old_address = {}
    for key in unchanged_address:
        old_address[key] = unchanged_address[key]
    return old_address

def error_match(error, address):
    for key in error:
        if (error[key][0] != '') and key in address:
            if key == ZIP:
                #ZIP is singled out since it is a list not a string
                if error[key][0][1] != '': #Format XXXXX-XXXX
                    if address[key][1] != error[key][0][1]:
                        return False
                if error[key][0][0] != '':
                    if address[key][0] != error[key][0][0]: #Either format
                            return False
            elif address[key].lower() != error[key][0].lower():
                return False
    return True

def correct(error, address):
    for key in error:
        if (len(error[key]) == 2):
            if key == ZIP:
                address[key][0] = error[key][1][0]
                address[key][1] = error[key][1][1]
            else:
                address[key] = error[key][1]

def add_error():
    #Purpose: Adding errors to a file in the standard format
    error_file = get_error_file('a+')
    toFix = ['State', 'City', 'Zip', 'Street Number', 'Street Name', 'Direction', 'Suffix']
    finished ='n'
    while finished.lower() != 'y':
        error_file.write('\n')
        for fix in toFix:
            old = raw_input('Which %s to fix? (Space for all, Enter to skip)' % fix)
            if old != ' ':
                error_file.write(old)
            if old != '':
                new = raw_input('What is the correction? (Hit Enter for no correction, Space to clear all instances of %s)' % old)
                if new != '':
                    error_file.write(',%s' % new)
            if fix != 'Suffix':
            #There is no pipe to separate the last field
                error_file.write('|')
        finished = raw_input('Quit? (y/n)')
    error_file.close()

if __name__ == '__main__':
    add_error()
