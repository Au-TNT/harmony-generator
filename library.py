# -*- coding: utf-8 -*-

# {'ChordType' : ((notes),bass)}
from tools import *
Tmaj = {'name' : 'Tmaj' , 'type' : 'majorTriad' , 'function' : ['T'] , 'bass' : 0 , 'consist' : (0,4,7) , 'repeatable' : (0,) , 'omitable' : tuple([7]) , 'numberOfNote' : 4}
Smaj = {'name' : 'Smaj' , 'type' : 'majorTriad' , 'function' : ['S'] , 'bass' : 5 , 'consist' : (5,9,0) , 'repeatable' : (5,) , 'omitable' : tuple([0]) , 'numberOfNote' : 4}
Dmaj = {'name' : 'Dmaj' , 'type' : 'majorTriad' , 'function' : ['D'] , 'bass' : 7 , 'consist' : (7,11,2) , 'repeatable' : (7,) , 'omitable' : tuple([2]) , 'numberOfNote' : 4}

chordDictMajor = {'Tmaj' : Tmaj , 'Smaj' : Smaj , 'Dmaj' : Dmaj}
Tmin = {'name' : 'Tmin' , 'type' : 'minorTriad' , 'function' : ['T'] , 'bass' : 0 , 'consist' : (0,3,7) , 'repeatable' : (0,) , 'omitable' : tuple([7]) , 'numberOfNote' : 4}
Smin = {'name' : 'Smin' , 'type' : 'minorTriad' , 'function' : ['S'] , 'bass' : 5 , 'consist' : (5,8,0) , 'repeatable' : (5,) , 'omitable' : tuple([0]) , 'numberOfNote' : 4}
Dmin = {'name' : 'Dmin' , 'type' : 'minorTriad' , 'function' : ['D'] , 'bass' : 7 , 'consist' : (7,10,2) , 'repeatable' : (7,) , 'omitable' : tuple([2]) , 'numberOfNote' : 4}
IIhalfDim7 = {'name' : 'IIhalfDim7', 'type' : 'halfDimSeventh', 'function' : ['S'] , 'bass' : 2, 'consist' : (2,5,8), 'repeatable' : (2,), 'omitable' : (), 'numberOfNote' : 4}
chordDictMinor = {'Tmin' : Tmin , 'Smin' : Smin , 'Dmin' : Dmin, 'IIhalfDim7' : IIhalfDim7}
chordDictAll = {'Tmaj' : Tmaj , 'Smaj' : Smaj , 'Dmaj' : Dmaj, 'Tmin' : Tmin , 'Smin' : Smin , 'Dmin' : Dmin, 'IIhalfDim7' : IIhalfDim7}
MajorScale = [0,2,4,5,7,9,11]
MinorScale = [0,2,3,5,7,8,10]
ModeList = ['Major', 'Minor']
#parallelOctave = ['and', [['for', ['notesInFirst', 'noteOne', ['for', ['notesInFirst', 'noteTwo', ['negate', ['and',['and', [['set', ['noteOnePosition', '=' , 'noteOne', '.', 'position']], ['set', ['noteTwoPosition', '=' , 'noteTwo' '.' , 'posistion']]]]]]]]]]]]
#ConnectionRules = {'parallelOctave' : parallelOctave}
KeyList = ['Cb', 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'E#', 'Fb', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B', 'B#'
           'Cbm', 'Cm', 'C#m', 'Dbm', 'Dm', 'D#m', 'Ebm', 'Em', 'E#m', 'Fbm', 'Fm', 'F#m', 'Gbm', 'Gm', 'G#m', 'Abm', 'Am', 'A#m', 'Bbm', 'Bm', 'B#m']
KeyShiftValueDict = {'C' : 0, 'Am' : 0, 'C#' : 1, 'A#m' : 1, 'Db' : 1, 'Bbm' : 1, 'D' : 2, 'Bm' : 2, 'Cbm' : 2,
                     'D#' : 3, 'B#m' : 3, 'Eb' : 3, 'Cm' : 3, 'E' : 4, 'C#m' : 4, 'Fb' : 4, 'E#' : 5, 'F' : 5, 
                     'F#' : 6, 'Gb' : 6, 'G' : 7, 'G#' : 8, 'Ab' : 8, 'A' : 9, 'A#' : 10, 'Bb' : 10, 'B' : 11, 'Cb' : 11 , 'B#' : 0}
'''
def parallel(diction, interval):
    thisAllNotes = diction.get('this').get('all')
    nextAllNotes = diction.get('next').get('all')
    for noteOne in thisAllNotes:
        for noteTwo in thisAllNotes:
            idOne = noteOne.get('id')
            idTwo = noteTwo.get('id')
            if (idOne != idTwo) and (noteOne.get('position') - noteTwo.get('position') == interval):
                for note in nextAllNotes:
                    if note.get('id') == idOne:
                        matchingPosOne = note.get('position')
                for note in nextAllNotes:
                    if note.get('id') == idTwo:
                        matchingPosTwo = note.get('position')
                if matchingPosOne - matchingPosTwo == interval:
                    return True
    return False
def overlap(diction):
    thisAllNotes = diction.get('this').get('all')
    nextAllNotes = diction.get('next').get('all')
    overlap = False
    for noteOne in thisAllNotes:
        for noteTwo in nextAllNotes:
            idOne = noteOne.get('id')
            idTwo = noteTwo.get('id')
            if idOne < idTwo: #One should be on top of Two
                #compare noteTwo with noteOne
                if noteTwo.get('octave') > noteOne.get('octave'):
                    overlap = True
                elif (noteTwo.get('octave') == noteOne.get('octave')) and (noteTwo.get('position') > noteOne.get('position')):
                    overlap = True
            elif idTwo < idOne: #Two should be on top of one
                if noteOne.get('octave') > noteTwo.get('octave'):
                    overlap = True
                elif (noteOne.get('octave') == noteTwo.get('octave')) and (noteOne.get('position') > noteTwo.get('position')):
                    overlap = True
    return overlap
def superOctave(diction):
    thisAllNotes = diction.get('this').get('all')
    nextAllNotes = diction.get('next').get('all')
    superOctave = False
    for note in thisAllNotes:
        for noteNext in nextAllNotes:
            if note.get('id') == noteNext.get('id'):
                if note.get('octave') > noteNext.get('octave') + 1:
                    superOctave = True
                elif (note.get('octave') > noteNext.get('octave')) and (note.get('position') > noteNext.get('position')):
                    superOctave = True
                elif noteNext.get('octave') > note.get('octave') + 1:
                    superOctave = True
                elif (noteNext.get('octave') > note.get('octave')) and (noteNext.get('position') > note.get('position')):
                    superOctave = True
    return superOctave

def parallelFifth(diction):
    return parallel(diction, 7)
def parallelOctave(diction):
    return parallel(diction, 0)

def Rules_Connection(diction):
    checkList = []
    checkList.append(parallelFifth(diction))
    checkList.append(parallelOctave(diction))
    checkList.append(overlap(diction))
    if overlap(diction) == False:
        print('no overlap')
    checkList.append(superOctave(diction))
    for i in checkList:
        if i == True:
            return False
    print('connection passed')
    return True

def reverseProgression(diction):
    thisFunction = diction.get('this')
    nextFunction = diction.get('next')
    if 'T' not in thisFunction and 'S' not in thisFunction:
        if 'T' not in nextFunction and 'D' not in nextFunction:
            return True
    return False

def Rules_FunctionCheck(diction):
    checkList = []
    checkList.append(reverseProgression(diction))
    for i in checkList:
        if i == True:
            return False
    return True

def Rules_endCheck(diction):
    return True
'''
#---color---

NoteWeight = {'root' : 4, 'char' : 5, 'fifth' : 2, 'tritone7' : 0, 'tritone' : 5, 'root_as_bass' : 4}

Func_MajT = {'name' : 'MajT', 0 : 'root' , 4 : 'char', 7 : 'fifth', 10 : 'tritone7'}
Func_MinT = {'name' : 'MinT', 0 : 'root' , 3 : 'char',  7 : 'fifth'}
Func_MajS = {'name' : 'MajS', 5 : 'root',  9 : 'char',  0 : 'fifth',  3 : 'tritone7'}
Func_MinS = {'name' : 'MinS', 5 : 'root',  8 : 'char',  0 : 'fifth'}
Func_MajD = {'name' : 'MajD', 7 : 'root',  11 : 'char',  2 : 'fifth',  5 : 'tritone7'}
Func_MinD = {'name' : 'MinD', 7 : 'root',  10 : 'char',  2 : 'fifth'}
Func_MajSS = {'name' : 'MajSS', 10 : 'root',  2 : 'char',  5 : 'fifth',  8 : 'tritone7'}
Func_MinSS = {'name' : 'MinSS', 10 : 'root',  1 : 'char',  5 : 'fifth'}
Func_MajDD = {'name' : 'MajDD', 2 : 'root',  6 : 'char',  9 : 'fifth',  0 : 'tritone7'}
Func_MinDD = {'name' : 'MinDD', 2 : 'root',  5 : 'char',  9 : 'fifth'}
Function_group_list = [Func_MajT, Func_MinT, Func_MajS, Func_MinS, Func_MajD, Func_MinD, Func_MajSS, Func_MinSS, Func_MajDD, Func_MinDD]

TensionWeight = {0 : 0, 1 : 3, 2 : 2, 3 : 0, 4 : 0, 5 : 0, 6 : 6, "aug5" : 3, "dim7" : 2} # minor second : 4, major second : 2, etc.

Mood_IntervalWeight = {0 : 0, 1 : -10, 2 : 10, 3 : -50, 4 : 50, 5 : 0, 6 : 0, 7 : 0, 8 : 40, 9 : -40, 10 : -10, 11 : 10} #{interval : value}, calculate from bass
Mood_ToRootWeight = {0 : 0, 1 : -10, 2 : 10, 3 : -50, 4 : 50, 5 : -5, 6 : 0, 7 : 0, 8 : -30, 9 : 30, 10 : -10, 11 : 10}
Mood_TensionDilutionratio = lambda tension : limitRange((3.0/limitRange(tension,50.0,0.1) - 0.005*limitRange(tension,50.0,0.1)),2.0,0.0)

def Mood_TensionDilution(tension:int):
    tension = float(tension)
    if tension == 0:
        ratio = 2.0
    else:
        ratio = 3.0/tension - 0.005*tension
    if ratio < 0.0: #floor = 0%
        ratio = 0.0
    elif ratio > 2.0:
        ratio = 2.0
    return ratio

#---chordtype---

MajorTriad = [0,4,7]
MinorTriad = [0,3,7]
DiminishedTriad = [0,3,6]
AugmentedTriad = [0,4,8]
MajorSeventh = [0,4,7,11]
MinorSeventh = [0,3,7,10]
DominantSeventh = [0,4,7,10]
DiminishedSeventh = [0,3,6,9]
MinorMajorSeventh = [0,3,7,11]
HalfDiminishedSeventh = [0,3,6,10]
Triads = (MajorTriad, MinorTriad, DiminishedTriad, AugmentedTriad)
Sevenths = (MajorSeventh, MinorSeventh, DominantSeventh, DiminishedSeventh, MinorMajorSeventh, HalfDiminishedSeventh)

#skip---

#---skip
DefaultTensionSet = {1,2,3,5,6,8,9}