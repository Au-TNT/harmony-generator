def readConfig(parameter):

    config = open("config.cfg", "r")
    lines = config.readlines()
    i=0
    while i < len(lines):
        lines[i] = lines[i].replace("\n", "")
        i+=1
    allowedChordTypes = set(lines[0].split(","))
    if allowedChordTypes == {"none"}:
        allowedChordTypes = {}

    isDiatonic = lines[1]
    if lines[1] == 'diatonic':
        isDiatonic = True
    else:
        isDiatonic = False

    noteNumberRange = lines[2].split(",")
    noteNumberRange = [int(n) for n in noteNumberRange]

    if lines[3] != 'none':
        tensionUse = set(lines[3].split(","))
        tensionUse = {int(note) for note in tensionUse}
    else:
        tensionUse = {}
    if lines[4] != 'none':
        omitUse = set(lines[4].split(","))
        omitUse = {int(note) for note in omitUse}
    else:
        omitUse = {}
    if lines[5] == 'none':
        avoidingInterval = {'modify' : {}, 'repeat' : {}, 'bassRepeat' : {}, 'bass' : {}}
    elif lines[5] == 'default':
        avoidingInterval = {'modify' : {6}, 'repeat' : {1,2,6}, 'bassRepeat' : {6}, 'bass' : {}}
    else:
        lines[5] = lines[5].rstrip()
        avoidingIntervalRawList = lines[5].split("_")
        avoidingIntervalList = []
        for item in avoidingIntervalRawList:
            item = item.split(',')
            if item == ['']:
                item = {}
            else:
                item = {int(note) for note in item}
            avoidingIntervalList.append(item)
        avoidingInterval = {'modify' : avoidingIntervalList[0], 'repeat' : avoidingIntervalList[1], 'bassRepeat' : avoidingIntervalList[2], 'bass' : avoidingIntervalList[3]}
    
    if lines[6] == 'default':
        minorScale = [0,2,3,5,7,8,10]
    elif lines[6] == 'harmonic minor':
        minorScale = [0,2,3,5,7,8,11]
    elif lines[6] == 'melodic minor':
        minorScale = [0,2,3,5,7,9,11]
    elif lines[6] == 'natrual minor':
        minorScale = [0,2,3,5,7,8,10]
    else:
        minorScale = [int(note) for note in lines[6].split(',')]
    
    inputFileDirectory = lines[7]

    maximumOutputFiles = int(lines[8])
    if maximumOutputFiles == -1:
        maximumOutputFiles = 9223372036854775807
    
    
    maxConnectionOnNode = int(lines[10])
    if maxConnectionOnNode == -1:
        maxConnectionOnNode = 9223372036854775807

    if parameter == 'allowedChordTypes' or parameter == 1 or parameter == '1':
        return allowedChordTypes
    elif parameter == 'isDiatonic' or parameter == 2 or parameter == '2':
        return isDiatonic
    elif parameter == 'noteNumberRange' or parameter == 3 or parameter == '3':
        return noteNumberRange
    elif parameter == 'tensionUse' or parameter == 4 or parameter == '4':
        return tensionUse
    elif parameter == 'omitUse' or parameter == 5 or parameter == '5':
        return omitUse
    elif parameter == 'avoidingInterval' or parameter == 6 or parameter == '6':
        return avoidingInterval
    elif parameter == 'minorScale' or parameter == 7 or parameter == '7':
        return minorScale
    elif parameter == 'inputFileDirectory' or parameter == 8 or parameter == '8':
        return inputFileDirectory
    elif parameter == 'maximumOutputFiles' or parameter == 9 or parameter == '9':
        return maximumOutputFiles
    elif parameter == 'minimumOutputFiles' or parameter == 10 or parameter == '10':
        minimumOutputFiles = int(lines[9])
        return minimumOutputFiles
    elif parameter == 'maximumSuccessiveConnectionForNode' or parameter == 11 or parameter == '11':
        return maxConnectionOnNode
    elif parameter == 'maximumTime' or parameter == 12 or parameter == '12':
        maximumTimeInSecond = int(lines[11])
        return maximumTimeInSecond
    elif parameter == 'all':
        return (allowedChordTypes, isDiatonic, tensionUse, omitUse, avoidingInterval)
    
def writeConfig():
    config = open("config.cfg", "r+")
    configlines = config.readlines()
    print("""---configuration change---\n1. allowed chord types, 2. diatonic/chromatic, 3. number of note in a chord, 4. tension usage, 5. omit notes, 6. avoiding interval in chords, 
          7. type of minor scale used, 8. directory for text input file, 9. maximum output files, 10. minimum output files, 11. maximum connection for any node, 12. maximum program running time""")
    selection = input("select one of the option, or press 'x' to exit:")
    if selection == 'x':
        return 0
    print(f"you selected{selection}\ncurrent data:{configlines[int(selection)-1]}, correspond as {readConfig(int(selection))}")
    if input("do you want to change it?(y/n):") != 'y':
        return 0
    else:
        newline = input("input new configuration:")
        configlines[int(selection)-1] = newline+'\n'
        config.close()
        config = open("config.cfg", "w+")
        config.writelines(configlines)
        config.close()

if __name__ == '__main__':
    print(readConfig("isDiatonic"))
    writeConfig()