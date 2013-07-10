#-------------------------------------------------------------------------------
# Name:        Address PreFormatter
# Purpose:     to parse addresses into their discrete fields, so that they can
#              run on the Address_Getter and Error_Fixermodules, which utilize
#              very separated information.
#
# Author:      Matt Brenman
#
# Created:     09/07/2013
#-------------------------------------------------------------------------------

import string

#Global Variables -- Can be overwritten if a file with different
#headers is given (Will be prompted at runtime)
delimiter = '|'
NON_FIELD = 'NONFIELD' #Field names are only lowercase in the system, so there
                  #is no chance of conflict with this name

def main():
    dataFile = get_file('input')
    set_delimiter()
    typeList = read_header(dataFile)
    accts = organize(typeList, dataFile)
    remove_notes(typeList, accts)
    get_street_numbers(typeList, accts)
    get_zip_codes(typeList, accts)
    get_direction(typeList, accts)
    get_suffixes(typeList, accts)
    get_cities(typeList, accts)
    get_street_names(typeList, accts)
    print_file(typeList, accts)

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

def set_delimiter():
    global delimiter
    change = raw_input('Change delimiter from \'%c\'? (y/n)' % delimiter)
    if (change.lower == 'y'):
        delimiter = raw_input('Enter new delimiter: ')
    elif (change.lower() != 'n'):
        #'n' returns, a non y/n answer prompts question again
        set_delimiter()

def read_header(dataFile):
    """ Extracts the header information (column names) from the raw data """
    typeLine = (dataFile.readline()).strip()
    #All column names are forced to lowercase to avoid case errors
    typeLine = typeLine.lower()
    typeList = typeLine.split(delimiter)
    return typeList

def organize(typeList, dataFile):
    """ Puts all client data in a list by acct"""
    accts = []
    for line in dataFile:
        info = line.split(delimiter) #Raw single-client data
        clientDict = {}
        if (len(typeList) <= len(info)):
            for i in range(len(typeList)):
                clientDict[typeList[i]] = info[i] #Attach each bit of client
                                                    #data to the correct type
            accts.append(clientDict)
        else:
            #Catches incomplete client data with fewer fields than necessary
            print "Error with client: ", info
    return accts

def get_street_numbers(typeList, accts):
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    streetField = get_valid_field_name(typeList, 'Street Number')
    newField = find_replacement_name('streetnumb', 'Street Number', typeList)
    typeList.append(newField)
    if streetField != NON_FIELD:
        for acct in accts:
            whitespace = False
            streetNum = ''
            for char in acct[streetField]:
                if char in digits:
                    streetNum += char
                elif char == ' ':
                    whitespace = True
                    break
                else:
                    #Avoids problems with streets like 5th street with no number
                    #or intersections with numbered streets
                    streetNum = ''
                    break
            acct[newField] = streetNum
            acct[streetField] = acct[streetField][len(streetNum):]
            if whitespace:
                #Whitespace field is needed in case a field already
                #contains just the number (out of bounds issue)
                acct[streetField] = acct[streetField][1:]

def get_direction(typeList, accts):
    dirs = [' north ', ' south ', ' east ', ' west ',
            ' n ', ' s ', ' e ', ' w ',
            ' n. ', ' s. ', ' e. ', ' w. ']
    dirField = get_valid_field_name(typeList, 'Direction')
    newField = find_replacement_name('pdir', 'Direction', typeList)
    typeList.append(newField)
    if dirField != NON_FIELD:
        for acct in accts:
            dirCount = 0
            direction = ''
            addrCheck = ' ' + acct[dirField].lower() + ' '
            for dir in dirs:
                if dir in addrCheck:
                    direction = dir
                    dirCount += 1
            if dirCount == 1:
                acct[newField] = direction
                acct[dirField] = addrCheck.replace(direction, '')
            else:
                acct[newField] = ''

def get_suffixes(typeList, accts):
    suffixes = [' street ', ' road ', ' drive ', ' pike ', ' lane ',
                ' avenue ', ' way ', ' circle ', ' terrace ', ' boulevard ',
                ' st ', ' rd ', ' dr ', ' pk ', ' ln ', ' ave ', ' cir ',
                ' ter ', ' blvd ']
    suffixField = get_valid_field_name(typeList, 'Street Suffix')
    newField = find_replacement_name('ssfx', 'Street Suffix', typeList)
    typeList.append(newField)
    if suffixField != NON_FIELD:
        for acct in accts:
            suffixCount = 0
            ssfx = ''
            addrCheck = ' ' + acct[suffixField].lower() + ' '
            for suffix in suffixes:
                if suffix in addrCheck:
                    ssfx = suffix
                    suffixCount += 1
            if suffixCount == 1:
                acct[newField] = ssfx
                acct[suffixField] = addrCheck.replace(ssfx, '')
            else:
                acct[newField] = ''

def get_zip_codes(typeList, accts):
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    zipField = get_valid_field_name(typeList, 'Zip Code')
    newField = find_replacement_name('zip', 'Zip Code', typeList)
    typeList.append(newField)
    if zipField != NON_FIELD:
        for acct in accts:
            zipcode = ''
            for char in acct[zipField]:
                if char in digits:
                    zipcode += char
                else:
                    zipcode = ''
                if len(zipcode) == 5:
                    break
            acct[newField] = zipcode
            acct[zipField] = acct[zipField].replace(zipcode, '')

def get_cities(typeList, accts):
    cityField = get_valid_field_name(typeList, 'City')
    newField = find_replacement_name('city', 'City', typeList)
    typeList.append(newField)
    if cityField != NON_FIELD:
        setup = get_city_setup()
        if setup == '1':
            no_street_cities(typeList, accts, cityField, newField)
        elif setup == '2':
            state = raw_input('What state does this data describe?\n'
                              '(Please enter as written in data)\n')
            no_street_cities(typeList, accts, cityField, newField, state)
        else:
            print 'Sorry. We do not yet have support for that setup.'

def get_city_setup():
    setup = raw_input('Which describes this field best:\n'
                      '(Ignoring street numbers, street driections,\n'
                      ' street suffixes, and zipcodes)\n'
                      '1: Contains only the city\n'
                      '2: Contains city and state\n'
                      '3: Contains street name and city\n'
                      '4: Contains street name, city, and state\n'
                      '5: Other\n')
    return setup

def no_street_cities(typeList, accts, cityField, newField, state=''):
    for acct in accts:
        cityContents = acct[cityField]
        city = cityContents.replace(state, '')
        acct[newField] = city
        acct[cityField] = acct[cityField].replace(city, '')

def get_street_names(typeList, accts):
    snameField = get_valid_field_name(typeList, 'Street Name')
    newField = find_replacement_name('streetname', 'Street Name', typeList)
    typeList.append(newField)
    if snameField != NON_FIELD:
        for acct in accts:
            acct[newField] = acct[snameField]

def remove_notes(typeList, accts, repeated='n'):
    if repeated == 'n':
        notesExist = raw_input('Are there any notes in any field that you would'
                               ' like to remove? (y/n)\n')
    else: notesExist = 'y'
    if notesExist.lower() == 'y':
        notesField = get_valid_field_name(typeList, 'Notes')
        newNotes = find_replacement_name('notes', notesField+'Notes', typeList)
        typeList.append(newNotes)
        noteSplit = '-1'
        while not noteSplit in ['1', '2']:
            noteSplit = raw_input('Are the notes between characters or\n'
                                  'after a character? (Enter Number)\n'
                                  '1: Between   Ex: streetinfo (note)\n'
                                  '2: After     Ex: streetinfo - note\n')
        newString = ''
        notes = ''
        if noteSplit == '1':
            end, start = get_splitters(2, 'two characters')
            for acct in accts:
                notesString = acct[notesField]
                acct[newNotes] = ''
                if start in notesString and end in notesString:
                    lindex = string.find(notesString, start)
                    rindex = string.rfind(notesString, end) + 1
                    if rindex > lindex:
                        newString = notesString[:lindex]
                        newString += notesString[rindex:]
                        notes = notesString[lindex:rindex]
                        acct[notesField] = newString
                        acct[newNotes] = notes
        elif noteSplit == '2':
            start = get_splitters(1, 'one character')
            for acct in accts:
                notesString = acct[notesField]
                acct[newNotes] = ''
                if start in notesString:
                    lindex = string.find(notesString, start)
                    newString = notesString[:start]
                    notes = notesString[start:]
                    acct[notesField] = newString
                    acct[newNotes] = notes
        repeat = raw_input('Are there more notes to remove? (y/n)\n')
        if repeat.lower() == 'y': remove_notes(typeList, accts, repeat)

def get_splitters(num, thing):
    splitters = ''
    while len(splitters) != num:
        splitters = raw_input('Enter the %s with no spaces or commas.' % thing)
    return {s for s in splitters}

def get_valid_field_name(typeList, fieldInfo):
    index = raw_input(make_column_question(typeList, fieldInfo))
    if valid_num(index):
        i = int(index)
        if i in range(1, len(typeList) + 1):
            return typeList[i - 1]
        elif i == len(typeList) + 1:
            return NON_FIELD
    #If not number or not in range
    print ('%s not a valid index.' % index)
    return get_valid_field_name(typeList, fieldInfo)

def valid_num(index):
    try:
        i = int(index)
        return True
    except ValueError:
        return False

def make_column_question(typeList, fieldInfo):
    question = ('Which field contains %s?\n' % fieldInfo)
    index = 1
    for col in typeList:
        question += ('%d: %s\n' % (index, col))
        index += 1
    question += ('%d: %s not in any field\n' % (index, fieldInfo))
    return question

def find_replacement_name(name, fieldInfo, typeList):
    name = name.lower()
    if name in typeList:
        name = raw_input('Enter fieldname to for added %s field' % fieldInfo)
        return find_replacement_name(name, fieldInfo, typeList)
    else:
        return name

def print_file(typeList, accts):
    addressFile = get_file('output', 'w')
    #Print header
    for i in range(0, len(typeList)):
        col = format_for_printing(typeList[i])
        if (i != len(typeList) - 1):
            addressFile.write(col + delimiter)
        else:
            addressFile.write(col + '\n')
    #Print body
    for acct in accts:
        for i in range(0, len(typeList)):
            col = typeList[i]
            info = format_for_printing(acct[col])
            if (i != len(typeList) - 1):
                addressFile.write(info + delimiter)
            else:
                addressFile.write(info + '\n')

def format_for_printing(data):
    data = data.replace(',', '')
    data = data.replace('|', '')
    return string.capwords(data)

if __name__ == '__main__':
    main()
