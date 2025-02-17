from classes_group.applical import Note, NoteSeries
from classes_group.structures import Returner
from tools import isfloat
from configs import readConfig
import library
import mido



def inputAll():
    choice = input("do you want to input 1:manually, 2:from text file, 3:form midi file?(1/2/3):")
    if choice == '2':
        fileDir = readConfig('inputFileDirectory')
        try:
            open(fileDir, 'r')
        except:
            return returner(-6) #error -6: input file directory does not exist
        with open(fileDir, 'r') as file:
            lines = file.readlines()
        returner = constructMelody(lines[0].replace('\n',''),lines[1].replace('\n',''),lines[2].replace('\n',''))
    if choice == '1':
        strMelody = input("melody:(octave/position/duration)")#octave_position, octave_position
        strKey = input('key:(in capitalize, Ex. C, Cb, G#)')
        strMode = input('mode:(Major/Minor)')
        beatPerMinute = input('BPM(=60 if left blank):')
        timeSignature = input('time signature(=4/4 if left blank, Ex. 3/4, 3/8):')
        strColor = input('input color:')
        returner = constructMelody(strMelody, [strKey,strMode,beatPerMinute,timeSignature], strColor)
    if choice == '3':
        fileDir = input('please input the directory of the midi file:')
        try:
            melodyMid = mido.MidiFile(fileDir)
            returner = inputMelodyFromMidi(melodyMid)
        except:
            returner = Returner(-7) #file does not exist
        if returner.returnCode < 0:
            return returner
        else:
            print('If you want to re-set the key/mode(especially when you inputted a minor melody)/time signature/BPM of the midi file, please enter below.')
            print("If you don't want make changes to any of the following, just press enter.")
            key = input('key(Ex. C, Eb, F#):')
            mode = input('mode(Major/Minor):')
            bpm = input('BPM(ex. 60, 120, 92):')
            timeSignature = input('timeSignature(ex. 4/4, 3/4, 3/8):')
            returner = inputInformations(key, mode, bpm, timeSignature, returner.object)
        if returner.returnCode < 0:
            return returner
        else:
            print("do you want to input color? (see the document for more information about 'color')")
            selection = input('(y/n):')
            if selection == 'y':
                strColor = input('color:')
                returner = inputColor(strColor, returner.object)
        if returner.returnCode < 0:
            return returner
        else:
            return returner
    return returner

'''
def inputAll():
    choice = input("do you want to input 1:manually or 2:from file?(1/2):")
    if choice == '2':
        fileDir = readConfig('inputFileDirectory')
        returner = inputAllFromFile(fileDir)
    if choice == '1':
        strMelody = input("melody:(octave/position/duration)")#octave_position, octave_position
        returner = inputMelody(strMelody)
        returnCode = returner.returnCode
        if returnCode < 0: #Error check
            return returner
        else:
            melody = returner.object
            returner = inputTonality(melody)
        returnCode = returner.returnCode
        if returnCode < 0:
            return returner
        else:
            selection = input('do you want to input color?(y/n):')
            if selection == 'y':
                melody = returner.object
                strColor = input("color:")
                returner = inputColor(strColor)
        if returnCode < 0:
            return returner
    return returner
'''

def constructMelody(strMelody, tonality, strColor):
    if isinstance(tonality, str):
        tonality = tonality.split(',')
    returner = inputMelody(strMelody)
    returnCode = returner.returnCode
    if returnCode < 0: #Error check
        return returner
    else:
        melody = returner.object
        returner = inputInformations(tonality[0],tonality[1],tonality[2],tonality[3],melody)
    returnCode = returner.returnCode
    if returnCode < 0:
        return returner
    else:
        if strColor != '':
            melody = returner.object
            returner = inputColor(strColor, melody)
        return returner

def inputMelody(strMelody):
    strMelody = strMelody.replace(" ","")#delete space
    listMelody = strMelody.split(",")#split by ,
    melody = NoteSeries([], 1)#set pointer=1 so that getcurrent reads 0
    note = Note(0, 0)
    error = False
    returnCode = 0
    rest = 0
    # Input Check #
    for i in listMelody:#split the octave and the position, then load it into the noteSeries
        rawNote = i.split("/")
        if len(rawNote) == 2 and rawNote[0] == 'rest':
            if isfloat(rawNote[1]):
                rest = float(rawNote[1])
            else:
                error = True
                returnCode = -1
        elif len(rawNote) == 3 and rawNote[0].isdigit() and rawNote[1].isdigit() and isfloat(rawNote[2]):
            note.octave = int(rawNote[0])
            note.position = int(rawNote[1])
            note.duration = float(rawNote[2])
            note.restBeforeNote = rest
            melody.queue.append(note.copy())
            rest = 0
        else:
            error = True
            returnCode = -1
    melody.queue.append(Note(0,0,endOfMelody=True))
    #Change string to int
    if returnCode < 0:
        return Returner(returnCode)
    else:
        return Returner(0, melody)
    
def inputInformations(key, mode, beatPerMinute, timeSignature, melody:NoteSeries):
    #key = input('key:(in capitalize, Ex. C, Cb, G#)')
    #mode = input('mode:(Major/Minor)')
    #beatPerMinute = input('BPM(=60 if left blank):')
    #timeSignature = input('time signature(=4/4 if left blank, Ex. 3/4, 3/8):')
    if key == '':
        key = melody.key

    if mode == '':
        mode = melody.mode
    if mode == 'major':
        mode = 'Major'
    elif mode == 'minor':
        mode = 'Minor'

    if beatPerMinute == '':
        beatPerMinute = melody.beatPerMinute

    if timeSignature == '':
        timeSignature = melody.timeSignature
    else:
        try:
            timeSignature = (int(timeSignature.split("/")[0]),
                                  int(timeSignature.split("/")[1])
                                  )
        except:
            error = True
            returnCode = -3
            return Returner(returnCode)
        
    if key in library.KeyList and mode in library.ModeList and isfloat(beatPerMinute):
        melody.key = key
        melody.mode = mode
        melody.beatPerMinute = int(beatPerMinute)
        melody.timeSignature = timeSignature
    else:
        error = True
        returnCode = -3
        return Returner(returnCode)
    
    for note in melody.queue:
        shiftSemitone = library.KeyShiftValueDict.get(melody.key)
        note.shift(shiftSemitone, upward=False)
    return Returner(0, melody)

'''
def singleStrInputTonality(strTonality:str, melody:NoteSeries):
    """
    string format:
        key,mode,BPM,time signature
        Ex. F#,Minor,112,6/8
    """
    stringList = strTonality.split(',')
    key = stringList[0]
    mode = stringList[1]
    beatPerMinute = stringList[2]
    timeSignature = stringList[3]
    if key == '':
        key = 'C'

    if mode == '':
        mode = 'Major'

    if beatPerMinute == '':
        beatPerMinute = '60'

    if timeSignature == '':
        timeSignature = (4,4)
    else:
        try:
            timeSignature = tuple(timeSignature.split("/"))
        except:
            error = True
            returnCode = -3
            return Returner(returnCode)
        
    if key in library.KeyList and mode in library.ModeList and beatPerMinute.isdigit():
        melody.key = key
        melody.mode = mode
        melody.timeSignature = timeSignature
    else:
        error = True
        returnCode = -3
        return Returner(returnCode)
    
    for note in melody.queue:
        shiftSemitone = library.KeyShiftValueDict.get(melody.key)
        note.shift(shiftSemitone, upward=False)
    return Returner(0, melody)
'''
def inputColor(str:str, melody:NoteSeries):
    '''
    input format:
        note one args > note two args > note three args...
    note args format:
        moodMin#moodMax_tensionMin#tensionMax_functionDictMin#functionDictMax
        mood:int/float, tension:int
    functionDict format:
        {function : value, function : value}
        functions: MajT, MinT, MajS, MinS...
    example:
        -10#50_0#5_'skip'#{MajS : 5, MinS : 5} > -20#40_0#8_{MajT : 15, MinT : 8}#{MajD : 5, MinD : 5}
    '''
    str = str.replace(" ","")#delete space
    listStr = str.split(">")#split by >
    i=0
    while i < len(listStr):
        itemList = listStr[i].split("_")
        moodRange = itemList[0].split("#")
        if isfloat(moodRange[0]) and isfloat(moodRange[1]) and len(moodRange) == 2:
            moodRange[0] = float(moodRange[0])
            moodRange[1] = float(moodRange[1])
            melody.queue[i].moodRange = moodRange
        else:
            return Returner(-5)
        tensionRange = itemList[1].split("#")
        if tensionRange[0].isdigit() and tensionRange[1].isdigit() and len(tensionRange) == 2:
            tensionRange[0] = int(tensionRange[0])
            tensionRange[1] = int(tensionRange[1])
            melody.queue[i].tensionRange = tensionRange
        else:
            return Returner(-6)
        '''
        functionRange = itemList[2].split("#")
        melody.queue[i].functionMax = functionRangeDictionAnalysis(functionRange[0])
        melody.queue[i].functionMin = functionRangeDictionAnalysis(functionRange[1])
        def functionRangeDictionAnalysis(dictStr):
            diction = {}
            if dictStr != 'skip':
                dictStr.replace("{","")
                dictStr.replace("}", "")#delete{}from both side
                dictStr.replace('"', '')#delete "
                dictStrList = dictStr.split(",")
                for tempKeyItem in dictStrList:
                    tempKeyItem = tempKeyItem.split(":")
                    tempKeyItem[1] = int(tempKeyItem[1])
                    diction[tempKeyItem[0]] = tempKeyItem[1]
            return diction
        '''
        i+=1
    return Returner(0, melody)

def inputMelodyFromMidi(midifile:mido.MidiFile):
    tracks = []
    TICKS_PER_BEAT = midifile.ticks_per_beat
    C0 = 12
    tempo = 500000
    beatPerMinute = 60
    timeSignature = (4,4)
    key = 'C'
    mode = 'Major'
    for track in midifile.tracks:
        tracks.append([msg.dict() for msg in track])

    tempoMsg = findMsg(tracks, 'set_tempo')
    if tempoMsg != 'no msg':
        tempo = tempoMsg.get('tempo')
        
    timeSignatureMsg = findMsg(tracks, 'time_signature')
    if timeSignatureMsg != 'no msg':
        timeSignature = (timeSignatureMsg.get('numerator'),timeSignatureMsg.get('denominator'))
    beatPerMinute = mido.tempo2bpm(tempo, timeSignature)    
    keyMsg = findMsg(tracks, 'key_signature')
    if keyMsg != 'no msg':
        key = keyMsg.get('key')
    if key[-1] == 'm':
        mode = 'Minor'
        del key[-1]
    else:
        mode = 'Major'
    
    #---note parsing---
    notes = []
    for track in tracks:
        trackNotes = []
        abs_time = 0
        #change to absolute timing
        for msg in track:
            note_diction = {}
            abs_time += msg.get('time')
            if msg.get('type') == 'note_on' or msg.get('type') == 'note_off':
                note_diction['note'] = msg.get('note')
                note_diction['type'] = msg.get('type')
                note_diction['velocity'] = msg.get('velocity') if 'velocity' in msg.keys() else 0
                note_diction['abs_time'] = abs_time
                trackNotes.append(note_diction)
        #change velocity=0 to note_off
        for note in trackNotes:
            if note['type'] == 'note_on' and note['velocity'] == 0:
                note['type'] = 'note_off'
        #pair note on with note off
        i=0
        pairedNotes = []
        while i<len(trackNotes):
            if trackNotes[i]['type'] == 'note_on':
                j=i+1
                finded = False
                #find the nearest 'note_off'
                while j<len(trackNotes) and not finded:
                    if trackNotes[j]['note'] == trackNotes[i]['note'] and trackNotes[j]['type'] == 'note_off':
                        pairedNotes.append(
                            {'note' : trackNotes[i]['note'],
                            'startTime' : trackNotes[i]['abs_time'],
                            'endTime' : trackNotes[j]['abs_time'],
                            'velocity' : trackNotes[i]['velocity']
                            }
                            )
                        del trackNotes[j]
                        finded = True
                    j+=1
            i+=1
        notes.extend(pairedNotes)
    #sort using time
    notes.sort(key=lambda note : note['startTime'])
    #remove simutaneous notes
    i=0
    while i<len(notes)-1:
        if notes[i]['startTime'] == notes[i+1]['startTime']:
            if notes[i]['endTime'] > notes[i+1]['endTime']:
                del notes[i+1]
            else:
                del notes[i]
        else:
            i+=1
    i=0
    #remove overlap
    while i<len(notes)-1:
        if notes[i]['endTime'] > notes[i+1]['startTime']:
            notes[i]['endTime'] = notes[i+1]['startTime']
        i+=1
    #add 'rest before'
    i=0
    while i<len(notes)-1:
        notes[i+1]['restBefore'] = notes[i+1]['startTime']-notes[i]['endTime']
        i+=1
    notes[0]['restBefore'] = notes[0]['startTime']
    '''
    #shift note
    for note in notes:
        note['note'] += library.KeyShiftValueDict.get(key)
    '''
    #positionalize
    for note in notes:
        abs_position = note['note']
        note['octave'] = (abs_position-12)//12#floor
        note['position'] = (abs_position-12)%12
    #use relevant duration
    for note in notes:
        duration = note['endTime']-note['startTime']
        note['duration'] = round((duration/TICKS_PER_BEAT)*16)/16 #quantitize to 32/64/128th
        restBefore = note['restBefore']
        note['restBefore'] = round((restBefore/TICKS_PER_BEAT)*16)/16

    #---build NoteSeries object---
    melody = NoteSeries([],0,key,mode,beatPerMinute,timeSignature)
    for note in notes:
        objectlizedNote = Note(note['octave'], note['position'], note['duration'], restBeforeNote=note['restBefore'], velocity=note['velocity'])
        melody.queue.append(objectlizedNote)
    melody.queue.append(Note(0,0,0.0,endOfMelody=True))
    return Returner(0, melody)

def findMsg(tracks:list, type:str):
        setted = False
        i=0
        j=0
        while not setted and i < len(tracks):
            track = tracks[i]
            while not setted and j < len(track):
                msg = track[j]
                if msg.get('type') == type:
                    infoMsg = msg
                    setted = True
                j+=1
            i+=1
        if setted:
            return msg
        else:
            return 'no msg'