#-------------------------------------------------------------------------------
# Name:        File_Splitter
# Purpose:     To split a file with a header into multiple files, spreading the
#              data between them, but maintaining the header on every single
#              file.
#
# Author:      Matt Brenman
#-------------------------------------------------------------------------------

def main():
    fileToSplit = get_file('input')
    numFiles = get_num_files()
    newFiles = get_new_files(numFiles)
    print_files(fileToSplit, newFiles, numFiles)

def get_num_files():
    numFiles = raw_input('Into how many files should your file be split?\n'
                         'Please enter a number (4) not a word (four)\n')
    try:
        number = int(numFiles)
    except ValueError:
        print 'Value not understood. Please try again.'
        get_num_files()
    else:
        return number

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

def get_new_files(numFiles):
    openedFiles = []
    for i in range(numFiles):
        name = 'new file %d' % i
        f = get_file(name, 'w')
        openedFiles.append(f)
    return openedFiles

def print_files(fileToSplit, newFiles, numFiles):
    header = fileToSplit.readline()
    for f in newFiles:
        f.write(header)
    fileNum = 0
    for line in fileToSplit:
        newFiles[fileNum].write(line)
        fileNum += 1
        if fileNum == numFiles: fileNum = 0
    close_files(fileToSplit, newFiles)

def close_files(fileToSplit, newFiles):
    fileToSplit.close()
    for f in newFiles:
        f.close()

if __name__ == '__main__':
    main()
