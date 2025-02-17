if __name__ != "__main__":
    from classes_group.applical import *
    from classes_group.structures import Tree, Stack
    import rules
    import configs
    import datetime
    import time
    from procession.print_harmony import printHarmony
    from caches import caches_voicing

global threadNumber
threadNumber = 0

def TreeBasedConstructHarmony(melody:NoteSeries, harmonyTree:Tree=Tree(0)):
    global threadNumber
    valid = False
    avaliableChordList = []
    subTree = Tree()
    if melody.checkOutOfBounce():
        harmonyTree.isEnd = True
        return harmonyTree
    # for a note, create a list of avaliable chords
    start=datetime.datetime.now()
    avaliableChordList = createAvaliableChords(melody)
    with open("runtime_log.txt", "a") as log:
        print(f"process createAvaliableChords spent{datetime.datetime.now()-start}", file=log)
    # recursive Backtracking
    for chord in avaliableChordList: #traversal
        subTree.branch = []
        start=datetime.datetime.now()
        if harmonyTree.isRoot == True:
            valid = True
        elif checkValidity(harmonyTree.node, chord):
            valid = True
        else:
            valid = False
        with open("runtime_log.txt", "a") as log:
            print(f"process checkValidity spent{datetime.datetime.now()-start}", file=log)
        if valid: #check
            subTree.node = chord
            melody.pointer = melody.pointer + 1
            subTree = TreeBasedConstructHarmony(melody, subTree)#dig in
            melody.pointer = melody.pointer - 1
            if subTree.isEmpty == False:
                harmonyTree.branch.append(subTree)
                start=datetime.datetime.now()
                harmonyTree = harmonyTree.copy()
                with open("runtime_log.txt", "a") as log:
                    print(f"process harmonyTree.deepcopy spent{datetime.datetime.now()-start}", file=log)
            else:
                with open("runtime_log.txt", "a") as log:
                    print('recieved empty on node=%s with branch node=%s' % (harmonyTree.node, melody.getCurrent().position), file=log)

        valid = False
    if harmonyTree.branch == []:
        harmonyTree.isEmpty = True
    else:
        harmonyTree.isEmpty = False
        with open("runtime_log.txt", "a") as log:
            print(f'set empty on thread number {threadNumber}, the {melody.pointer}th note of the melody', file=log)
    threadNumber += 1
    return harmonyTree

def StackBasedConstructHarmony(melody:NoteSeries):
    mainStartTime = time.time()
    harmonyList = []
    stack = Stack([], 0)
    stack.add(Chord([], startOfHarmony=True, id=88888888))
    voicingListPointer = 0
    voicingList = caches_voicing.voicingDict.get(melody.pointer)
    voicingListPointerRecord = [0]*len(melody.queue)
    voicingListRecord = [[]]*(len(melody.queue))
    passedNodeRecord = [0]*len(melody.queue)
    MAX_HARMONY = configs.readConfig('maximumOutputFiles')
    MIN_HARMONY = configs.readConfig('minimumOutputFiles')
    MAX_NODE_CONNECTION = configs.readConfig('maximumSuccessiveConnectionForNode')
    MAX_TIME = configs.readConfig('maximumTime')
    passedHarmonyCount = 0
    backtrack = False
    loop = True
    while loop:
        if voicingListPointer >= len(voicingList) or backtrack or passedNodeRecord[melody.pointer] >= MAX_NODE_CONNECTION:
            if stack.stack[stack.pointer-2].startOfHarmony: #access the potential 'start of melody'
                if passedNodeRecord[melody.pointer] >= MAX_NODE_CONNECTION and passedHarmonyCount < MIN_HARMONY:
                    MAX_HARMONY = MIN_HARMONY
                    MAX_NODE_CONNECTION = 9999999999
                    voicingListPointer = 0
                else:
                    loop = False
            else:
                stack.pop()
                #backtrack
                passedNodeRecord[melody.pointer] = 0
                melody.pointer -= 1
                voicingList = caches_voicing.voicingDict.get(melody.pointer)
                #recover the pointer
                voicingListPointer = voicingListPointerRecord[melody.pointer]
                #recover the list
                voicingList = voicingListRecord[melody.pointer]
            backtrack = False
        elif checkValidity(stack.get(), voicingList[voicingListPointer], melody.mode):
            #stack, move to next, record current pointer
            startTime = datetime.datetime.now()
            stack.add(voicingList[voicingListPointer])
            with open('runtime_log.txt', 'a') as file:
                print(f'operation stack.add took {datetime.datetime.now()-startTime}', file=file)
            #every stack is a record, every backtrack is a recover. If it backtracked then step again, do not recover the pointer.
            if stack.get().endOfHarmony:
                harmony = stack.print(1, -2)
                harmonyList.append(ChordSeries(
                harmony, pointer=0, 
                key=melody.key, mode=melody.mode, 
                beatPerMinute=melody.beatPerMinute, timeSignature=melody.timeSignature
                ))
                stack.pop()
                backtrack = True
                passedHarmonyCount += 1
                if passedHarmonyCount >= MAX_HARMONY:
                    loop = False
            else:
                #step in
                #record
                voicingListRecord[melody.pointer] = moveBackChords(voicingList, voicingList[voicingListPointer])
                voicingListPointerRecord[melody.pointer] = voicingListPointer+1 #move one to avoid infinite loop
                passedNodeRecord[melody.pointer] += 1
                voicingListPointer = 0
                melody.pointer += 1
                voicingList = caches_voicing.voicingDict.get(melody.pointer)
        else:
            voicingListPointer += 1
        if time.time()-mainStartTime > MAX_TIME:
            loop = False
    return harmonyList


def createAvaliableChords(melody:NoteSeries):
    note = melody.getCurrent()
    if note.endOfMelody == True:
        voicingList = [Chord([], 'End', endOfHarmony=True, id=99999999)]
    else:
        voicingList = caches_voicing.voicingDict.get(note.identifier)
    return voicingList

def checkValidity(previousChord:Chord, thisChord:Chord, mode='Major'):
    validity = False
    if (previousChord.identifier, thisChord.identifier) in caches_voicing.blockedConnection:
        validity = False
    elif (previousChord.identifier, thisChord.identifier) in caches_voicing.passedConnection:
        validity = True
    elif thisChord.endOfHarmony == True:
        endChordDict = {'function' : previousChord.function_component_calculator(), 'consist' : previousChord.consist(), 'mode' : mode}
        validity =  rules.ruleReader('endCheck', endChordDict)
        if validity:
            global threadNumber
            with open('runtime_log.txt', 'a') as file:
                print(f"passed endCheck on thread{threadNumber}", file=file)
            print(f"passed endCheck on thread{threadNumber}")
        else:
            with open('runtime_log.txt', 'a') as file:
                print(f"blocked endCheck on thread{threadNumber}", file=file)
            #print(f"blocked endCheck on thread{threadNumber}")
    elif previousChord.startOfHarmony:
        startChordDict = {'function' : thisChord.function_component_calculator(), 'consist' : thisChord.consist(), 'mode' : mode}
        validity = rules.ruleReader('startCheck', startChordDict)
    elif rules.ruleReader('functionCheck', {'this' : previousChord.function_component_calculator(), 'next' : thisChord.function_component_calculator()}):
        thisChord.permutate()
        previousChord.permutate()
        thisChordDict = thisChord.createConnectionRuleDiction()
        previousChordDict = previousChord.createConnectionRuleDiction()
        ruleDiction = {'this' : previousChordDict, 'next' : thisChordDict}
        if rules.ruleReader('connection', ruleDiction):
            validity = True
        else:
            validity = False
    else:
        validity = False

    if validity:
        caches_voicing.passedConnection.append((previousChord.identifier, thisChord.identifier))
    else:
        caches_voicing.blockedConnection.append((previousChord.identifier, thisChord.identifier))
    return validity

def buildHarmony(melody:NoteSeries):
    #melody.pointer = 1
    #melody.giveId()
    #harmony = ChordSeries([], 0, melody.key, melody.mode, melody.beatPerMinute)
    #harmonyList = []
    '''
    tree = TreeBasedConstructHarmony(melody, structures.Tree('root', [], isRoot=True))
    harmonyListUnclassed = tree.traversal()
    for harmonyUnclassed in harmonyListUnclassed:
        for chord in harmonyUnclassed:
            if chord != 'root':#Virtual Root
                harmony.add(chord)
        harmonyList.append(harmony.copy())
        harmony.resetQueue()
    '''

    melody.pointer=0
    melody.giveId()
    harmonyList = StackBasedConstructHarmony(melody)
    return harmonyList

def moveBackChords(chordList, passedChord:Chord):
    lenChordList = len(chordList)
    i=0
    chordList.append('end')
    loop = True
    while loop:
        if chordList[i] == 'end':
            del chordList[i]
            loop = False
        elif chordList[i].type == passedChord.type:
            movingBackChord = chordList[i]
            del chordList[i]
            chordList.append(movingBackChord)
        else:
            i += 1
    return chordList
'''
def getAvaliableChord(melody:NoteSeries):
    avaliableChordList = generateChord.generateChords(melody.getCurrent().position, melody.mode, 
                                 configs.readConfig('allowedChordTypes'), 
                                 configs.readConfig('noteNumberRange')[0], configs.readConfig('noteNumberRange')[1],
                                 configs.readConfig('isDiatonic'), 
                                 tensionUse = configs.readConfig('tensionUse'), omitsUse = configs.readConfig('omitUse'),
                                 functionDictMin=melody.getCurrent().functionMin, functionDictMax=melody.getCurrent().functionMax, 
                                 moodMin=melody.getCurrent().moodRange[0], moodMax=melody.getCurrent().moodRange[1], 
                                 tensionMin=melody.getCurrent().tensionRange[0], tensionMax=melody.getCurrent().tensionRange[1]
                                 )
    return avaliableChordList
'''
'''
def generateChordVoicing(soprano:Note, avaliableChordList):
    noteUsed = [soprano.position]
    voicingList = []
    for chordDict in avaliableChordList:
        tree = Tree(soprano, [], 0)
        numberOfNote = chordDict.get('numberOfNote')
        tree = getNote(tree, chordDict, noteUsed, numberOfNote-1, soprano.duration)
        voicingListUnclassed = tree.traversal()
        voicingListUnclassed = checkNecessaryNotesExist(voicingListUnclassed, chordDict)
        ACCEPTABLE_GAP_BETWEEN_SOPRANO_AND_BASS = 28
        voicingListUnclassed = checkGap(voicingListUnclassed, ACCEPTABLE_GAP_BETWEEN_SOPRANO_AND_BASS)
        for item in voicingListUnclassed: 
            voicingList.append(Chord(item, chordDict.get('name'), soprano.duration))  #Later, use this name to get the chord information from the dicctionary
        #debug_PrintChords(voicingList)
    return voicingList
'''
'''
def getNote(tree, chordDict, noteUsed, remainingNumberOfNote, duration=1.0):
    previousNote = tree.node
    #occupied = noteUsed - chordDict.get('repeatable')
    usable = (set(chordDict.get('consist')) - set(noteUsed)) | set(chordDict.get('repeatable'))
    i = 0

    /.
    for note in noteUsed:
        if note not in chordDict.get('repeatable'):
            occupied.append(note)

    for note in chordDict.get('consist'):
        if note not in occupied:
            usable.append(note)
    ./

    if remainingNumberOfNote == 0: #end
        return tree
    elif remainingNumberOfNote == 1: #bass
        note = previousNote.placeNote(chordDict.get('bass'), 1, duration=duration) #'1' means 0-1 octave under
        tree.addBranch(note)
        note = previousNote.placeNote(chordDict.get('bass'), 2, duration=duration)
        tree.addBranch(note)
    else: #alto/tenor/any middle notes
        for position in usable:
            note = previousNote.placeNote(position, 1, duration=duration)
            tree.addBranch(note)
    remainingNumberOfNote = remainingNumberOfNote - 1
    while i < len(tree.branch):
        sendInNoteUsed = noteUsed.copy()
        sendInNoteUsed.append(tree.branch[i].node.position)
        tree.branch[i] = getNote(tree.branch[i], chordDict, sendInNoteUsed, remainingNumberOfNote, duration)
        i = i + 1
    /.
    for branch in tree.branch: #recursing
        noteUsed.append(branch.node.position)
        branch = getNote(branch, chordDict, noteUsed, remainingNumberOfNote)
        #tree.replaceBranch(branch.seriesNum, branch) #use finished branch to replace empty branch
    ./
    return tree
    '''
'''
def placeNote(previousNote:Note, position, octaveUnder, **kwarg):
    if 'duration' in kwarg.keys():
        duration = kwarg.get('duration')
    else:
        duration = 1.0
    if previousNote.position >= position:
        octaveUnder = octaveUnder - 1 #move one octave down if it will cause overlap
    note = Note(previousNote.octave - octaveUnder, position, duration)
    return note

def checkNecessaryNotesExist(voicingListUnclassed:list, chordDict:dict):
    voicingListReturn = []
    necessaryNotes = set(chordDict.get('consist')) - set(chordDict.get('omitable'))
    for item in voicingListUnclassed:
        noteUsed = []
        for note in item:
            noteUsed.append(note.position)
        if necessaryNotes.issubset(set(noteUsed)):
            voicingListReturn.append(item)
    return voicingListReturn

def checkGap(voicingListUnclassed:list, gap):
    voicingListReturn = []
    for item in voicingListUnclassed:
        if (item[0].octave-item[-1].octave)*12+(item[0].position-item[-1].position) <= gap:
            voicingListReturn.append(item)
    return voicingListReturn
'''