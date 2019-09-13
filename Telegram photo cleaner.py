helpDescription = '''
This is a Python script designed to clean up Telegram photo imports, or \
any other normal photo import, from thumbnails and duplicate files.

Not only do imported Telegram data sets come with additional unnecessary \
folders such as stickers, the images that are imported also all come \
with duplicate thumbnails. This script thus cleans up all non-photo folders \
except for messages, and removes all thumbnail copies of the photos. In \
addition, this script removes all duplicate photos, as identified by the \
signifiers '(1)' etc behind each duplicate photo.

To use, place this script in the same folder as the imported Telegram photo \
folders. That is, 'root/Telegram photo cleaner.py' and 'root/Telegram Folder 1/photos' \
should be valid files/folders. This can be repeated for as many Telegram \
import folders as desired. Take note that for this script to work, the actual \
photos must exist in a folder within a folder in the same directory as this \
script. For instance, 'root/folder/Photo 1.jpg' will not work, but \
'root/folder/photos/Photo 1.jpg' will work. Additionally, this script \
recognizes a Telegram export purely by the existence of a folder named \
'root/<any name>/photos', so do not rename the nested folder 'photos' prior \
to running this script.

After clicking on the script, two modes will be prompted: 'VERBOSE' and \
'DELETE'. 'VERBOSE' simply provides additional printed information during \
the process, and 'DELETE' actually runs the deletion process. That is, if \
a dry run is desired, do not include 'DELETE' in the command. For instance, \
'VERBOSE' will print out information on the files that would be deleted, \
but will not actually delete them. Similarly, 'DELETE' will actually delete \
any thumbnails and duplicate files, but will not provide as much feedback \
while doing so. Take note that some duplicate feedback may be given when \
executing 'verbose' due to overlaps between the deletion methods of thumbnails \
and duplicate files. This issue should not occur when executing 'verbose delete'.
\n\n
'''

import os, re, shutil

def executeShutilDelete(folderPath, folderName, folderOrigin):
    global verboseMode, deleteMode
    if verboseMode:
        print("Folder removed: < " + folderName + " > in origin folder: < " + folderOrigin + " >")
    if deleteMode:
        shutil.rmtree(folderPath)


def executeOSDelete(filePath, fileName, fileOrigin, isThumbnail):
    global verboseMode, deleteMode
    if verboseMode:
        if isThumbnail:
            print("Thumbnail removed: < " + fileName + " > in folder: < " + fileOrigin + " >")
        else:
            print("Duplicate file removed: < " + fileName + " > in folder: < " + fileOrigin + " >")
    if deleteMode:
        os.remove(filePath)

def runTelegramPhotoCleaner():
    global totalPhotoDuplicates, totalFolderDuplicates
    for folder in os.listdir(os.getcwd()):
        if os.path.isdir(folder) == True:
            for subFolder in os.listdir(folder):
                filePath = folder + '\\' + subFolder
                fileName = os.path.basename(subFolder)
                removeCounter = 0
                
                if re.search('contacts|css|images|js|stickers', fileName) != None:
                    executeShutilDelete(os.getcwd() + '\\' + filePath, subFolder, folder)                    
                    totalFolderDuplicates += 1
                    continue
                
                if os.path.isdir(filePath):
                    if re.search('photos', fileName) != None:
                        for File in os.listdir(filePath):
                            if re.search('_thumb',os.path.basename(File)) != None:
                                executeOSDelete(os.getcwd() + '\\' + filePath + '\\' + File, File, subFolder, True)
                                removeCounter += 1
                    
                    for File in os.listdir(filePath):
                        if re.search('\(\d\)',os.path.basename(File)) != None:
                            executeOSDelete(os.getcwd() + '\\' + filePath + '\\' + File, File, subFolder, False)
                            removeCounter += 1
                            
                    totalPhotoDuplicates += removeCounter
                    print('Removed ' + str(removeCounter) + ' files in ' + folder + '.')

deleteMode = False ## false if dry run, true if actual deletion run
verboseMode = False ## provides more verbose feedback to the deletion process
totalPhotoDuplicates = 0
totalFolderDuplicates = 0

startingInstructions = '''If performing a dry run, press Enter.
If performing a dry run with verbose feedback, type "VERBOSE".
If performing an actual delete, type "DELETE".
If performing an actual delete with verbose feedback, type "VERBOSE DELETE".
If more information on this script is needed, type "HELP".'''

print(startingInstructions)
while True:
    modeSelected = input()
    if modeSelected == "HELP":
        print(helpDescription)
        print(startingInstructions)
    elif modeSelected == "":
        print('\n**EXECUTING DRY RUN**\n')
        break
    elif modeSelected == "VERBOSE":
        verboseMode = True
        print('\n**EXECUTING DRY RUN WITH VERBOSE FEEDBACK**\n')
        break
    elif modeSelected == "DELETE":
        deleteMode = True
        print('\n**EXECUTING DELETION OF FILES**\n')
        break
    elif modeSelected == "VERBOSE DELETE":
        verboseMode = True
        deleteMode = True
        print('\n**EXECUTING DELETION OF FILES WITH VERBOSE FEEDBACK**\n')
        break
    else:
        print('Please enter a valid command.')
    
runTelegramPhotoCleaner()

print('\nRemoved a total of ' + str(totalPhotoDuplicates) + ' duplicate files and ' +
      str(totalFolderDuplicates) + ' duplicate folders.')
print('Press ENTER to close.')
buffer = input();

