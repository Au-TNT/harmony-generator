import library
import tools
import color
from classes_group.analytics import *
        
def generateBasslessBasicChord(melody:int, chordLibrary, scale='majorScale', **kwargs) -> list:
    diatonicOnly = kwargs.get('diatonicOnly') if 'diatonicOnly' in kwargs.keys() else True
    melodyPlace = kwargs.get('melodyPlace') if 'melodyPlace' in kwargs.keys() else [0,1,2,3,4,5,6]
    customizeScale = kwargs.get('customizeScale') if 'customizeScale' in kwargs.keys() else False
    #default triadOnly false and diatonicOnly true 

    chordList = []
    #if customizeScale, use the input in 'scale' variable as the scale
    if customizeScale:
        pass
    elif scale == 'majorScale':
        scale = library.MajorScale
    elif scale == 'minorScale':
        scale = library.MinorScale

    chord = []
    for chordType in chordLibrary:
        i=0
        while i < len(chordType):
            if i in melodyPlace:
                root = melody - chordType[i]
                chord = [(root+note)%12 for note in chordType]
                if not diatonicOnly or set(chord) <= set(scale): #if all notes are in scale
                    chordList.append(chord.copy())
            i += 1
    return chordList

def modifyBasicChord(chord:list, root=0, tensions={2,5,8,9}, omit={3,4,7}, avoidingInterval={6}, maximumNotes=6, minimumNotes=1) -> list:
    '''
    inputs:
    chord: the component notes of the chord, list
    tensions: the notes to add, set
    omit: the notes to omit, set
    avoidingInterval: when adding tensions, avoid the interval. 1=11, 2=10, 3=9, set
    maximumNotes, int
    minimunNotes, int
    '''
    chord = set(chord)
    if tensions == 'none':
        tensions = {}
    elif tensions == 'all':
        tensions = {1,2,3,4,5,6,7,8,9,10,11}
    if omit == 'none':
        omit = {}
    elif omit == 'all':
        omit = {3,4,7}
    omit = chord & {root+note for note in omit}
    tensions = {root+note for note in tensions} - chord

    modifiedChordList = []
    i=0
    j=0
    modifiedChordPrev = set()
    #omit, then add tension. noteNumber = chordNoteNumber-omit+tensions < maximumNotes
    while i <= len(omit):
        modifiedChordPrev = set()
        omitListList = tools.DeleteIdenticals(tools.MultiTraversal(list(omit), i), ordered=False)#combination
        for omitList in omitListList:
            modifiedChordPrev = chord - set(omitList)
            j=0
            while j <= len(tensions) and len(chord) - i + j <= maximumNotes:#noteNumber = chordNoteNumber-omit+tensions < maximumNotes
                tensionsListList = tools.DeleteIdenticals(tools.MultiTraversal(list(tensions), j), ordered=False)#combination
                for tensionsList in tensionsListList:
                    modifiedChord = modifiedChordPrev | set(tensionsList)
                    #intervalCheck
                    intervalList = tools.DeleteIdenticals(tools.MultiTraversal(list(modifiedChord), 2), False)#combination
                    discard = False
                    for interval in intervalList: 
                        if not chord > set(interval): #if not all notes are original
                            if abs(interval[0] - interval[1]) in avoidingInterval:
                                discard = True
                    if(
                    #len(modifiedChord) >= minimumNotes and 
                    not discard):
                        modifiedChordList.append(chordSort(root, list(modifiedChord)))
                j += 1
        i += 1
    return modifiedChordList

def chordSort(root:int, consist:list, sortDiction:list = [[0,1], [4,3], [7,6,8], [11,10], [2,1,3], [5,6], [9,8,10]]) -> list:
    '''
    sortDiction: {root -> [0], third -> [first priority -> 4, second priority -> 3], ...}
    a chord can have only one root, one third, one fifth ... one thirteenth.
    If the chord have more than 6 consist, or not all notes can be described as root......thirteenth, go to the start of the diction and do fifteenth, seventeenth...
    '''
    sortDiction = [row[:] for row in sortDiction]
    sortedList = []
    modifyingConsist = consist[:]
    i, sorted = 0, False
    while not sorted:
        j, passing = 0, False
        while j < len(sortDiction[i]) and not passing:
            if sortDiction[i][j] in [(note-root)%12 for note in modifyingConsist]: #if the consist have the note in this point at sort Diction
                note = (root+sortDiction[i][j])%12
                sortedList.append((note))
                passing = True
                del sortDiction[i][j]
                modifyingConsist.remove(note)
            j += 1
        if set(consist) == set(sortedList):
            sorted = True
        i = i+1 if i+1 < len(sortDiction) else 0
    return sortedList

def generateRepeatable(chord:list, bass:int, avoidingInterval={6}, avoidingRepeatNote={3,4,8,9,10,11}, bassAvoid='same') -> list:
    '''
    avoidingRepeatNote is in scale
    chord is after modified and placed in melody
    '''

    if bassAvoid == 'same':
        bassAvoid = avoidingInterval
    repeatable = set()
    for repeatNote in chord:
        valid = True
        for note in chord: #reverse check
            if note == bass:
                if (repeatNote - note + 12)%12 in bassAvoid:
                    valid = False
            elif (repeatNote - note + 12)%12 in avoidingInterval:
                valid = False
        if valid:
            repeatable.add(repeatNote)
    repeatable.difference_update(avoidingRepeatNote)
    return repeatable

def generateBass(root:int, consist:list, inversions={0,1,2,3}, avoidingInterval={}, **kwargs) -> list:
    IntervalChordConstructIn = kwargs.get('intervalChordConstructIn') if 'intervalChordConstructIn' in kwargs.keys() else [{0},{3,4},{6,7},{10,11},{1,2},{5,6},{8,9}]#normal chords
    #for chords that's not constructed in thirds, a specialized IntervalChordConstructIn will be needed
    #We consider diminished seventh as the first inversion of itself
    bassList = []
    for inversion in inversions:
        for note in consist:
            if (note-root+12)%12 in IntervalChordConstructIn[inversion]: #this is saying, if there's a note in consist matches the given inversion's normal place counting in third(normally)
                valid=True
                for noteTwo in consist:
                    if abs(noteTwo-note) in avoidingInterval:
                        valid=False
                if valid:
                    bassList.append(note)
    return bassList

def generateChords(melody:int, mode:str='major', chordTypes={'triad', 'seventh'}, minimumNotes=4, maximumNotes=4, diatonicOnly=True, functionDictMin='skip', functionDictMax='skip', tensionMin=0, tensionMax=24, moodMin=-100.0, moodMax=100.0, **kwargs) -> list:
    '''
    melody: chromatic value, int, [0,12]
    mode: Major/Minor, str
    chordType: triad/seventh, {str,str...}
    maximumNotes, minimumNotes: #ofNotes in chord, int, [1,inf)
    diatonicOnly: bool
    --color--
    functionDictMin: the minimum value of each function component. Ex: {'MajD':16}, will skip those that didn't show up, dict
    functionDictMax, the maximum value of each function component, dict
    tensionMin/tensionMax: the min/max value of tension, int, [0,inf)
    colorMin/colorMax: the min/max value of color, float, [-100,100]

    other variables (**kwargs):
    identification:
        get an identical name for the chord dictions
        id = id, int, default 0
    scale:
        use customized scale. If do not use this input, the scale will be based on the inputted mode
    using complex equations for function components:
        useEquationForFunctionComponent = True, functionComponentEquation = 'str', (Ex. functionDict.get(MajT)+functionDict.get(MajS) > 0), a expression that returns True or False
    tensionsUse:
        tensionsUse = {int,int,int...}, in chromatic
    omitsUse:
        omitsUse = {int,int,int...}, in chromatic, default {3,4,7}
    noteUse:
        diatonicOnly -> True, mode -> any, scale = [int,int,int...], list, Ex. [0,1,3,5,7,8,11](double harmonic minor)
    inversion:
        inversions = {int,int,int...} (in 0,1,2,3,4,5,6), default {0,1,2,3}
    melodyPlace:
        melodyPlaces = {int,int,int...} (in 0,1,2,3,4,5,6), default {0,1,2,3.4}
    avoidingInterval:
        avoidingInterval = {'modify' : {int,int...}, 'repeat' : {int,int...}, 'bassRepeat' : {int,int,int...}, 'bass' : {int,int...}}, default {6},{1,2,6},{6}, {}, dict
    avoidingRepeatingNotes:
        avoidingRepeatingNotes = {int,int.int...}, in [0 to 12], default {8,9,10,11}

    output:

    '''
    topIdentification = kwargs.get("id") if "id" in kwargs.keys() else 0
    useEquationForFunctionComponent = kwargs.get("useEquationForFunctionComponent") if "useEquationForFunctionComponent" in kwargs.keys() else False
    if useEquationForFunctionComponent:
        functionComponentEquation = kwargs.get("functionComponentEquation") if "functionComponentEquation" in kwargs.keys() else '1'
    tensionUse = kwargs.get("tensionUse") if "tensionUse" in kwargs.keys() else library.DefaultTensionSet
    omitsUse = kwargs.get("omitsUse") if "omitsUse" in kwargs.keys() else {3,4,7}
    scale = kwargs.get("scale") if "scale" in kwargs.keys() else library.MajorScale if mode=='Major' or mode=='major' else library.MinorScale
    inversions = kwargs.get("inversions") if "inversions" in kwargs.keys() else {0,1,2,3}
    melodyPlaces = kwargs.get("melodyPlaces") if "melodyPlaces" in kwargs.keys() else {0,1,2,3,4}
    avoidingIntervals = kwargs.get("avoiodingIntervals") if "avoidingIntervals" in kwargs.keys() else {'modify' : {6}, 'repeat' : {1,2,6}, 'bassRepeat' : {6}, 'bass' : {}}
    avoidingRepeatingNotes = kwargs.get("avoidingRepeatingNotes") if "avoidingRepeatingNotes" in kwargs.keys() else {8,9,10,11}

    chordDictionList = []
    subIdentification = 0

    mainChordLibrary = []
    chordList = []
    if 'triad' in chordTypes:
        mainChordLibrary.extend(library.Triads)
    if 'seventh' in chordTypes:
        mainChordLibrary.extend(library.Sevenths)
    for chord in mainChordLibrary:
        chordLibrary = modifyBasicChord(chord, 0, tensionUse, omitsUse, avoidingIntervals.get('modify'), maximumNotes, minimumNotes)
        #print("chordLibrary", chordLibrary)
        processedChords = generateBasslessBasicChord(melody, chordLibrary, scale, customizeScale = True, melodyPlace = melodyPlaces, diatonicOnly = diatonicOnly)
        #print("generated:" , processedChords)
        processedChords = tools.DeleteIdenticals(processedChords, False, sort=False)
        temperaryList_chordList = [item[:] for item in processedChords]#deepCopy
        i=0
        while i < len(processedChords):
            if processedChords[i] in chordList:
                del processedChords[i]
            else:
                i += 1
        
        #tension check
        temperaryList_tension = []
        for basslessChord in processedChords:
            tension = color.tension_calculator(color.createIntervalDict(basslessChord))
            if tensionMin <= tension and tension <= tensionMax:
                temperaryList_tension.append(basslessChord.copy())
        processedChords = [item[:] for item in temperaryList_tension]#deepCopy

        #print("tensionProcessed:", processedChords)
        for basslessChord in processedChords:
            root = basslessChord[0]
            bassList = generateBass(root, basslessChord, inversions, avoidingIntervals.get('bass'))

            temperaryList_function = []
            for bass in bassList: #functionnal check
                functionDict = color.function_component_calculator(basslessChord, bass)
                if useEquationForFunctionComponent:
                    valid = eval(functionComponentEquation)
                else:
                    #functionMin
                    minValid = True
                    if functionDictMin == 'skip':
                        pass
                    else:
                        for key,value in functionDict.items():
                            if key in functionDictMin.keys() and functionDictMin.get(key) > value:
                                minValid = False
                    #functionMax
                    maxValid = True
                    if functionDictMax == 'skip':
                        pass
                    else:
                        for key,value in functionDict.items():
                            if key in functionDictMax.keys() and functionDictMax.get(key) < value:
                                maxValid = False
                    valid = minValid and maxValid
                if valid:
                    temperaryList_function.append(bass)
            bassList = temperaryList_function.copy()
            
            temperaryList_mood = []
            for bass in bassList: #color check
                mood = color.mood_calculator(basslessChord, bass, color.tension_calculator(color.createIntervalDict(basslessChord)))
                if moodMin <= mood and mood <= moodMax:
                    temperaryList_mood.append(bass)
            bassList = temperaryList_mood.copy()
            
            for bass in bassList: #createDiction
                repeatable = generateRepeatable(basslessChord, bass, avoidingIntervals.get('repeat'), avoidingRepeatingNotes, avoidingIntervals.get('bassRepeat'))
                for n in range(len(basslessChord), maximumNotes+1):
                    if n >= minimumNotes:
                        chordDictionList.append({'name' : str(topIdentification)+'-'+str(subIdentification), 'belonging' : topIdentification,'bass' : bass, 'consist' : basslessChord, 'repeatable' : tuple(repeatable), 'numberOfNote' : n, 'omitable' : {}})
                subIdentification += 1
        chordList.extend(temperaryList_chordList)

    with open("chord_list_log.txt", 'a') as file:
        for chordDiction in chordDictionList:
            print(str(chordDiction)+'\n', file=file)
    return chordDictionList

if __name__ == '__main__':
    print(modifyBasicChord([1,5,8,11], 1, {1,2,3,4,5,6,8,9}, {3,4,7}, {6,1}, 6, 1))
    chordDict = generateChords(11, 'major', {'triad', 'seventh'}, 3, 4, True, 'skip', 'skip', 0, 32, -100, 100, melodyPlaces = {0,1,2,3}, omitsUse = {})
    file = open('chord_list_log.txt', 'w')
    for chord in chordDict:
        file.write(str(chord)+'\n')
        print(chord)
    file.close()
    #print(generateBasslessBasicChord(0,modifyBasicChord([0,4,7], 0), 'majorScale'))