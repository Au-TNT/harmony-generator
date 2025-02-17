import library

class NoteProgression:
    bassProgression = 0
    sopranoProgression = 0
    middleProgressions = []
    disappeared = []
    appeared = []
    def __init__(self, bassProgression, sopranoProgression, middleProgressions, disappeared, appeared):
        self.bass = bassProgression
        self.soprano = sopranoProgression
        self.middles = middleProgressions
        self.disappeared = disappeared #distance to bass, earlier chord
        self.appeared = appeared #distance to bass, later chord

class ChordFactor:
    def __init__(self, position, distanceToRoot, distanceToBass='skip', absPlace='skip', mood=0):
        '''
        position: root/third/fifth/seventh (1,3,5,7)
        distanceToRoot: (note-root)%12
        distanceToBass: (note-bass)%12, skip=distanceToRoot
        absPlace: position in scale
        mood: int, in [-100, 100]
        '''
        self.position = position
        self.distanceToRoot = distanceToRoot
        self.distanceToBass = distanceToBass if distanceToBass != 'skip' else distanceToRoot
        self.absPlace = absPlace
        self.mood = mood
    def determineMood(self, ToRoot=True, moodDiction:dict='skip'):
        #the method both changes and returns the value
        if moodDiction == 'skip':
            if ToRoot:
                moodDiction = library.Mood_ToRootWeight
            else:
                moodDiction = library.Mood_IntervalWeight
        if ToRoot:
            self.mood = moodDiction.get(self.distanceToRoot)
        else:
            self.mood = moodDiction.get(self.distanceToBass)
        return self.mood
    
class RawChord:
    def __init__(self, noteList, root, bass='skip', factorList=[]):
        '''
            noteList: [int,int...], consists
            root: int
            bass: int, the lowest note in chord, =root if skiped
            factorList: [color.ChordComponent, ...]
        '''
        self.noteList = noteList
        self.root = root
        self.bass = bass if bass != 'skip' else root
        self.factorList = factorList
    def factorize(self, sortDiction={1 : [0,1], 3 : [4,3], 5 : [7,6,8], 7 : [11,10], 9 : [2,1,3], 11 : [5,6], 13 : [9,8,10]}):
        '''
        sortDiction: {root -> [0], third -> [first priority -> 4, second priority -> 3], ...}
        a chord can have only one root, one third, one fifth ... one thirteenth.
        If the chord have more than 6 consist, or not all notes can be described as root......thirteenth, go to the start of the diction and do fifteenth, seventeenth...
        '''
        sortedList = []
        sortedDiction = sortedDiction.copy()
        modifyingConsist = self.noteList[:]#.copy
        modifyingConsist = [(note-self.root)%12 for note in modifyingConsist]#intervalize to root
        findPosition = lambda i: 2*i+1
        i, sorted = 0, False
        while not sorted:
            j, passing = 0, False
            positionKey = findPosition(i)%14
            positionConsistList = sortDiction.get(positionKey)
            while j < len(positionConsistList) and not passing:
                if positionConsistList[j] in modifyingConsist: #if the consist have the note in this point at sort Diction
                    note = positionConsistList[j]
                    sortedList.append((ChordFactor(findPosition(i), note, (note+self.root-self.bass)%12, (note+self.root)%12)))
                    tempNoteList = sortDiction.get(positionKey)
                    del tempNoteList[j]
                    sortDiction[positionKey] = tempNoteList
                    modifyingConsist.remove(note)
                    passing = True
                j += 1
            if modifyingConsist == []:
                sorted = True
            i += 1
        self.factorList = sortedList