from . import structures
import library

class Note:
    identifier = 0
    def __init__(self, octave, position, duration=1.0, level=0, sharpFlat='', moodRange=[-100,100], tensionRange=[0,32], functionMin:dict='skip', functionMax:dict='skip', restBeforeNote=0.0, velocity=64, **kwargs):
        if 'endOfMelody' in kwargs.keys():
            self.endOfMelody = kwargs.get('endOfMelody')
            if not isinstance(self.endOfMelody, bool):
                print('error on class Note: wrong type for endOfMelody')
        else:
            self.endOfMelody = False
        self.octave = octave
        self.position = position
        self.level = level
        self.sharpFlat = sharpFlat
        self.duration = duration
        self.moodRange = moodRange
        self.restBeforeNote = restBeforeNote
        self.velocity = velocity
        self.tensionRange = tensionRange
        self.functionMin = functionMin
        self.functionMax = functionMax
        self.identifier = kwargs.get('id') if 'id' in kwargs.keys() else -1
        #for position: 0 means tonic, 1 means one semitone from tonic. Ex. 7 means the fifth of the major/minor scale
    def copy(self):
        newCopy = Note(self.octave, self.position, self.duration, self.level, self.sharpFlat, self.moodRange, self.tensionRange, self.functionMin, self.functionMax, endOfMelody=self.endOfMelody, restBeforeNote=self.restBeforeNote, id=self.identifier, velocity=self.velocity)
        return newCopy
    def placeNote(self, position, octaveGap, **kwarg):
        if 'above' in kwarg.keys():
            above = kwarg.get('above')
        else:
            above = False
        if 'duration' in kwarg.keys():
            duration = kwarg.get('duration')
        else:
            duration = 1.0
        if self.position >= position:
            octaveGap = octaveGap - 1 #move one octave up if the gap is over expected
        if above == False:
            note = Note(self.octave - octaveGap, position, duration, velocity=self.velocity)
        if above == True:
            note = Note(self.octave + octaveGap, position, duration,velocity=self.velocity)
        return note
    def shift(self, semitone, **kwargs):
        if 'upward' in kwargs.keys():
            up = kwargs.get('upward')
        else:
            up = False
        if up == True:
            self.position = self.position + semitone
            if self.position >= 12:
                self.position = self.position - 12
                self.octave = self.octave + 1
        elif up == False:
            self.position = self.position - semitone
            if self.position < 0:
                self.position = self.position + 12
                self.octave = self.octave - 1
    def print(self) -> str:
        string = f'({self.octave}/{self.position})'
        return string
        

        
class MusicSeries(structures.Queue):
    queue = []
    pointer = 0
    key = ''
    mode = ''
    def __init__(self, queue=[], pointer=0, key='C', mode='Major', beatPerMinute=60, timeSignature=(4,4)):
        structures.Queue.__init__(self, queue, pointer)
        self.key = key
        self.mode = mode
        self.beatPerMinute = beatPerMinute
        self.timeSignature = timeSignature
    def copy(self):
        newQueue = []
        for item in self.queue:
            newQueue.append(item.copy())
        return MusicSeries(newQueue,self.pointer,self.key,self.mode,self.beatPerMinute, self.timeSignature)
    
class NoteSeries(MusicSeries):
    def __init__(self, queue=[], pointer=0, key='C', mode='Major', beatPerMinute=60, timeSignature=(4,4)):
        MusicSeries.__init__(self, queue, pointer, key, mode, beatPerMinute, timeSignature)
    def giveId(self):
        pointer = 0
        queueLen = len(self.queue)
        while pointer < queueLen:
            self.queue[pointer].identifier = pointer
            pointer += 1

class ChordSeries(MusicSeries):
    key = ''
    mode = ''
    def __init__(self, queue=[], pointer=0, key='C', mode='Major', beatPerMinute=60, timeSignature=(4,4)):
        MusicSeries.__init__(self, queue, pointer, key, mode, beatPerMinute, timeSignature)

class Chord:
    soprano = Note(0,0,0,'')
    middle = []
    bass = Note(0,0,0,'')
    def __init__(self, noteList, type='', duration=1.0, **kwargs):
        if 'endOfHarmony' in kwargs.keys():
            self.endOfHarmony = kwargs.get('endOfHarmony')
        else:
            self.endOfHarmony = False
        self.noteList = noteList
        self.type = type
        self.duration = duration
        self.identifier = kwargs.get('id') if 'id' in kwargs.keys() else -1
        self.startOfHarmony = kwargs.get('startOfHarmony') if 'startOfHarmony' in kwargs.keys() else False

    def permutate(self):
        i = 0
        noteListLength = len(self.noteList)
        while i < noteListLength:
            self.noteList[i].identifier = i
            if i == 0:
                self.soprano = self.noteList[i]
            elif i == noteListLength - 1:
                self.noteList[i].identifier = 99 #bass: 99
                self.bass = self.noteList[i]
            else:
                self.middle.append(self.noteList[i])
            i = i + 1
        self.middle = self.middle.copy()

    def createConnectionRuleDiction(self):
        '''
        output:
            every note is in the form of:
            {'position' : int, 'octave' : int, 'id' : int}
            the whole diction is in the form:
            {'soprano' : soprano, 'middle' : [note,note,note...], 'bass' : bass, 'all' : [note,note,note...]}
            where soprano, note, and bass are all in 'note form'
        '''
        sopranoDict = {'position' : self.soprano.position , 'octave' : self.soprano.octave, 'id' : self.soprano.identifier}
        bassDict = {'position' : self.bass.position , 'octave' : self.bass.octave, 'id' : self.bass.identifier}
        middleList = []
        noteList = []
        for note in self.middle:
            middleDict = {'position' : note.position, 'octave' : note.octave, 'id' : note.identifier}
            middleList.append(middleDict.copy())
        for note in self.noteList:
            noteDict = {'position' : note.position, 'octave' : note.octave, 'id' : note.identifier}
            noteList.append(noteDict.copy())
        chordDict = {'soprano' : sopranoDict , 'middle' : middleList , 'bass' : bassDict , 'all' : noteList}
        return chordDict
    
    def function_component_calculator(self):
        self.permutate()
        noteList = [note.position for note in self.noteList]
        noteList = list(set(noteList))
        bass = self.bass.position
        weight = library.NoteWeight
        groupList = library.Function_group_list
        chordComponent = {}
        for group in groupList:
            groupName = group.get('name')
            groupValue = 0
            tritoneSeventh = False
            characteristicThird = False
            for note in noteList:
                for key in group.keys():
                    if note == key:
                        groupComponent = group.get(note)
                        groupValue = groupValue + weight.get(groupComponent)
                        if groupComponent == 'tritone7':
                            tritoneSeventh = True
                        elif groupComponent == 'char':
                            characteristicThird = True
                        elif groupComponent == 'root' and note == bass:
                            groupValue = groupValue + weight.get('root_as_bass')

            if tritoneSeventh == True and characteristicThird == True:
                groupValue = groupValue + weight.get('tritone')
            chordComponent[groupName] = groupValue
        #print(chordComponent)
        return chordComponent
    
    def consist(self):
        consist = []
        for note in self.noteList:
            consist.append(note.position)
        return consist

    def print(self):
        noteListStr = ''
        for note in self.noteList:
            noteListStr += note.print()
            noteListStr += ','
        
        string = f"Chord id={self.identifier}:\n    noteList = {noteListStr}"
        return string

    def copy(self):
        newCopy = Chord(self.noteList.copy(), self.type, self.duration, endOfHarmony=self.endOfHarmony, id=self.identifier, startOfHarmony = True)
        newCopy.soprano = self.soprano
        newCopy.middle = self.middle.copy()
        newCopy.bass = self.bass
        return newCopy
    