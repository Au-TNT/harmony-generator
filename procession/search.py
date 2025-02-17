from generateChord import generateChords
from classes_group.applical import *
from classes_group.structures import Tree
from configs import readConfig
import ast
import random
from caches import caches_voicing

def generateChordsForMelody(melody:NoteSeries, filename='./caches/chords.txt'):
    file = open(filename, 'w')
    melody.pointer = 0
    chordList = []

    while not melody.checkLastInQueue():
        note = melody.queue[melody.pointer]
        chordList = generateChords(
             note.position, 
             melody.mode, 
             readConfig('allowedChordTypes'), 
             readConfig('noteNumberRange')[0], 
             readConfig('noteNumberRange')[1],
             readConfig('isDiatonic'), 
             tensionUse = readConfig('tensionUse'), 
             omitsUse = readConfig('omitUse'),
             functionDictMin=melody.getCurrent().functionMin, 
             functionDictMax=melody.getCurrent().functionMax, 
             moodMin=melody.getCurrent().moodRange[0], 
             moodMax=melody.getCurrent().moodRange[1], 
             tensionMin=melody.getCurrent().tensionRange[0], 
             tensionMax=melody.getCurrent().tensionRange[1],
             id=melody.pointer
        )
        for chord in chordList:
            print(chord, file=file, end='\n')
        melody.pointer += 1
    file.close()
    return chordList

def readChords(id:int, filename):
    chordList = []
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        line.rstrip('\n')
        chordDict = ast.literal_eval(line)
        if chordDict.get('belonging') == id:
            chordList.append(chordDict)
    return chordList

def generateChordVoicing(soprano:Note, avaliableChordList):
    noteUsed = [soprano.position]
    voicingList = []
    for chordDict in avaliableChordList:
        tree = Tree(soprano, [], 0)
        numberOfNote = chordDict.get('numberOfNote')
        tree = getNote(tree, chordDict, noteUsed, numberOfNote-1, soprano.duration)
        voicingListUnclassed = tree.traversal()
        voicingListUnclassed = checkNecessaryNotesExist(voicingListUnclassed, chordDict)
        ACCEPTABLE_GAP_BETWEEN_SOPRANO_AND_BASS = 24
        voicingListUnclassed = checkGap(voicingListUnclassed, ACCEPTABLE_GAP_BETWEEN_SOPRANO_AND_BASS)
        for item in voicingListUnclassed:
            voicingList.append(Chord(item, chordDict.get('name'), soprano.duration))  #Later, use this name to get the chord information from the dicctionary
        #debug_PrintChords(voicingList)
    subId = 0
    for voicing in voicingList:
        voicing.identifier = int((soprano.identifier+1)*10000000+subId)
        subId += 1
    return voicingList

def getNote(tree, chordDict, noteUsed, remainingNumberOfNote, duration=1.0):
    previousNote = tree.node
    #occupied = noteUsed - chordDict.get('repeatable')
    usable = (set(chordDict.get('consist')) - set(noteUsed)) | set(chordDict.get('repeatable'))
    i = 0
    '''
    for note in noteUsed:
        if note not in chordDict.get('repeatable'):
            occupied.append(note)

    for note in chordDict.get('consist'):
        if note not in occupied:
            usable.append(note)
    '''
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
    '''
    for branch in tree.branch: #recursing
        noteUsed.append(branch.node.position)
        branch = getNote(branch, chordDict, noteUsed, remainingNumberOfNote)
        #tree.replaceBranch(branch.seriesNum, branch) #use finished branch to replace empty branch
    '''
    return tree

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

def generateVoicingToCache(melody:NoteSeries):
    melody.pointer=0
    melody.giveId()
    while len(melody.queue)-melody.pointer > 1:
        note = melody.queue[melody.pointer]
        chordList = generateChords(
             note.position, 
             melody.mode, 
             readConfig('allowedChordTypes'), 
             readConfig('noteNumberRange')[0], 
             readConfig('noteNumberRange')[1],
             readConfig('isDiatonic'), 
             tensionUse = readConfig('tensionUse'), 
             omitsUse = readConfig('omitUse'),
             functionDictMin=melody.getCurrent().functionMin, 
             functionDictMax=melody.getCurrent().functionMax, 
             moodMin=melody.getCurrent().moodRange[0], 
             moodMax=melody.getCurrent().moodRange[1], 
             tensionMin=melody.getCurrent().tensionRange[0], 
             tensionMax=melody.getCurrent().tensionRange[1],
             id=melody.pointer
        )
        voicingList = generateChordVoicing(melody.queue[melody.pointer], chordList)
        with open('runtime_log.txt', 'a') as file:
            for chord in voicingList:
                string = chord.print()
                print(string, file=file)
        
        caches_voicing.voicingDict[melody.pointer] = random.sample(voicingList, len(voicingList))
        melody.pointer += 1
    #put an 'endOfHarmony' chord
    caches_voicing.voicingDict[melody.pointer] = [Chord([], endOfHarmony=True, id=99999999)]