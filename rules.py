import color
from itertools import combinations

CHECK_PARALLEL_FIFTH = True
CHECK_PARALLEL_OCTAVE = True
CHECK_OVERLAP = True
CHECK_TRITONE_RESOLVE = True
CHECK_OVER_AN_OCTAVE = True
CHECK_DOMINANT_TO_SUBDOMINANT = True
CHECK_TONIC_AT_THE_END = True
CHECK_TRITONE_AT_THE_END = True

def ruleReader(ruleBaseName:str, inputDiction:dict): #expected return a returner with True/False and returnCode
    '''
        connection:
        every note is in the form of:
        {'position' : int, 'octave' : int, 'id' : int}
        the whole diction is in the form:
        {'soprano' : soprano, 'middle' : [note,note,note...], 'bass' : bass, 'all' : [note,note,note...]}
        where soprano, note, and bass are all in 'note form'
        and it is constructed in
        {'this' : dict, 'next' : dict} 
        form, where dict is in the form of a 'whole diction'

        functionCheck, endCheck and startCheck all uses the function dict as input,
        where functionCheck is similar, constructed in
        {'this' : dict, 'next' : dict}
        format.

        endCheck have another two inputs, consist and mode.
        constructed in {'function' : dict, 'consist' : int, 'mode' : 'Major'/'Minor'}
        startCheck uses the same diction, constructed in:
        {'function' : dict, 'consist' : int, 'mode' : 'Major'/'Minor'}
        see color.py, function_component_calculator for informations about function dict
    '''
    if ruleBaseName == 'connection':
        return Rules_Connection(inputDiction)
    elif ruleBaseName == 'functionCheck':
        return Rules_FunctionCheck(inputDiction)
    elif ruleBaseName == 'endCheck':
        return Rules_endCheck(inputDiction)
    elif ruleBaseName == 'startCheck':
        #To be finished
        return True

def parallel(diction, interval):
    #Return true when is parallel (not passing)
    thisAllNotes = diction.get('this').get('all')
    nextAllNotes = diction.get('next').get('all')

    thisNoteIntervals = list(combinations(thisAllNotes, 2))
    for intervalNotes in thisNoteIntervals:
        noteOne = 'none'
        noteTwo = 'none'
        #get interval
        if intervalNotes[0].get('id') < intervalNotes[1].get('id'):
            thisInterval = (intervalNotes[0].get('position') - intervalNotes[1].get('position'))%12
        else:
            thisInterval = (intervalNotes[1].get('position') - intervalNotes[0].get('position'))%12
        #search in next chord
        if thisInterval == interval:
            noteOne = 'none'
            for note in nextAllNotes:
                if note.get('id') == intervalNotes[0].get('id'):
                    noteOne = note
            noteTwo = 'none'
            for note in nextAllNotes:
                if note.get('id') == intervalNotes[1].get('id'):
                    noteTwo = note
        #check in next chord
        if thisInterval == interval and noteOne != 'none' and noteTwo != 'none':
            #check if doesn't move
            if noteOne.get('position') == intervalNotes[0].get('position'):
                pass
            else:
                if noteOne.get('id') > noteTwo.get('id'):
                    nextInterval = (noteOne.get('position') - noteTwo.get('position'))%12
                else:
                    nextInterval = (noteOne.get('position') - noteTwo.get('position'))%12
                if nextInterval == interval:
                    #parallel
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

def tritoneResolve(diction) -> bool: 
    '''
    return true if resolved(passed), return false if not resolved(not passed)
    '''
    tritoneTendencyList = []
    tritoneIntervalList = []
    thisAllNotes = diction.get('this').get('all')
    thisConsist = []
    for note in thisAllNotes:
        thisConsist.append(note.get('position'))
    nextAllNotes = diction.get('next').get('all')
    nextConsist = []
    for note in nextAllNotes:
        nextConsist.append(note.get('position'))
    thisInterval = list(combinations(thisConsist, 2))
    nextInterval = list(combinations(nextConsist, 2))
    for interval in thisInterval:
        if (interval[0]-interval[1])%12 == 6:
            tritoneIntervalList.append(list(interval))

    tritoneResolve = True
    for tritoneInterval in tritoneIntervalList:
        tritoneTendencies = color.tritone_tendency(tritoneInterval[0], tritoneInterval[1])
        resolved = False
        maintained = False
        for tritoneSolution in tritoneTendencies:
            for interval in nextInterval:
                if sorted(tritoneSolution) == sorted(interval):
                    resolved = True
        if not resolved:
            maintained = False
            for interval in nextInterval:
                if sorted(tritoneInterval) == sorted(interval):
                    maintained = True
        if not (maintained or resolved):
            tritoneResolve = False
    return tritoneResolve



def Rules_Connection(diction):
    checkList = []
    if CHECK_PARALLEL_FIFTH:
        checkList.append(parallelFifth(diction))
    if CHECK_PARALLEL_OCTAVE:
        checkList.append(parallelOctave(diction))
    if CHECK_OVERLAP:
        checkList.append(overlap(diction))
    if CHECK_OVER_AN_OCTAVE:
        checkList.append(superOctave(diction))
    if CHECK_TRITONE_RESOLVE:
        checkList.append(not tritoneResolve(diction))
    for i in checkList:
        if i == True:
            return False
    #print('connection passed')
    return True


def reverseProgression(diction) -> bool:
    #Functionnal Diction : {'this' : {function_component_diction}, 'next' : {function_componnet_diction}, 'mode' : mode}
    NOTICABLE_SUBDOMINANT_DIFFERENCE = 1
    RESOLVATION_TONIC_DIFFERENCE = 48 #7^2-1
    SIGNIFICANT_DOMINANT_DECREASE = -250
    thisFunction = diction.get('this')
    nextFunction = diction.get('next')
    functionDifference = color.function_square_difference(thisFunction, nextFunction)
    reverseProgression = True
    if functionDifference.get("MajS") ** 2+ functionDifference.get("MinS") ** 2 < NOTICABLE_SUBDOMINANT_DIFFERENCE: #This is to test if a noticable increase of S gorup on either Major or Minor occured
        #notice that it's a reversed check
        #use MajS+MinS is to check the increase of bass of fifth, while avoiding the problem of flat sixth in harmonic major scale
        reverseProgression = False
        #print("stop on S")
    if functionDifference.get("MajT") ** 2 > RESOLVATION_TONIC_DIFFERENCE or functionDifference.get("MinT") > RESOLVATION_TONIC_DIFFERENCE:
        #notice that it's a reversed check
        reverseProgression = False
        #print("stop on T")
    if functionDifference.get("MajD") ** 2> SIGNIFICANT_DOMINANT_DECREASE:
        reverseProgression = False
        #print("stop on D")
    return reverseProgression

def Rules_FunctionCheck(diction):
    checkList = []
    if CHECK_DOMINANT_TO_SUBDOMINANT:
        checkList.append(reverseProgression(diction))
    for i in checkList:
        if i == True:
            #Return "True" if it is against the rule (Ex. it is reverseProgression, reverseProgression is true)
            return False
    return True

def Rules_endCheck(diction):
    checkList = []
    if CHECK_TONIC_AT_THE_END:
        checkList.append(isStableTonic(diction))
    if CHECK_TRITONE_AT_THE_END:
        checkList.append(noTritone(diction))
    for i in checkList:
        if i == False:
            #Retrun "False" if it is againsst the rule
            return False
    return True


def isStableTonic(diction):
    #True when is stable tonic
    tension = color.tension_calculator(color.createIntervalDict(diction.get('consist')))
    stableTonic = True
    functionDict = diction.get('function')
    mainTonic = functionDict.get('MajT') if functionDict.get('MajT') > functionDict.get('MinT') else functionDict.get('MinT')
    mainSubdominant = functionDict.get('MajS') if functionDict.get('MajS') > functionDict.get('MinS') else functionDict.get('MinS')
    mainDominant = functionDict.get('MajD') if functionDict.get('MajD') > functionDict.get('MinD') else functionDict.get('MinD')
    if tension > 9:
        stableTonic = False
    elif mainTonic ** 2 - 2*mainSubdominant ** 2 - mainDominant ** 2 < 90 or mainTonic <= 12:
        stableTonic = False
    elif (functionDict.get('MinT') > functionDict.get('MajT') and diction.get('mode') == 'Major'):#checking major scale only
        stableTonic = False
    return stableTonic

def noTritone(diction):
    #True when no tritone
    consist = diction.get('consist')
    intervalDiction = color.createIntervalDict(consist)
    if intervalDiction.get(6) > 0:
        return False
    else:
        return True

def Rules_startCheck(diction):
    tension = color.tension_calculator(color.createIntervalDict(diction.get('consist')))
    functionDict = diction.get('function')
    mainSS = functionDict.get('MajSS') if functionDict.get('MajSS') > functionDict.get('MinSS') else functionDict.get('MinSS')
    mainDD = functionDict.get('MajDD') if functionDict.get('MajDD') > functionDict.get('MinDD') else functionDict.get('MinDD')
    if mainSS ** 2 + mainDD ** 2 > 70:
        return False
    elif functionDict.get('MinT') >= 11 and diction.get('mode') == 'Major' or functionDict.get('MajT') >= 11 and diction.get('mode') == 'Minor':
        return False
    else:
        return True

def Colored_reverseProgression(diction):
    thisNoteList = diction.get("this").get("noteList")
    thisBass = diction.get("this").get("bass")
    nextNoteList = diction.get("next").get("noteList")
    nextBass = diction.get("next").get("bass")
    print(reverseProgression({"this" : color.function_component_calculator(thisNoteList, thisBass), "next" : color.function_component_calculator(nextNoteList, nextBass)}))

if __name__ == "__main__":
    chord = [7,11,2,5]
    chordTwo = [9,0,4]
    bass = 7
    bassTwo = 9
    diction = {"this" : {"noteList" : chord, "bass" : bass}, "next" : {"noteList" : chordTwo, "bass" : bassTwo}}
    Colored_reverseProgression(diction)
    print(color.function_square_difference(color.function_component_calculator(chord,bass), color.function_component_calculator(chordTwo,bassTwo)))