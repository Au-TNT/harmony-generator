from classes_group.applical import *
from tools import KeyShift
import mido
import os

def printHarmony(chordSeries:ChordSeries, **kwarg):
    if 'serialNumber' in kwarg.keys():
        serialNumber = kwarg.get("serialNumber")
    else:
        serialNumber = 1
    constant_BPM = 60
    constant_ticks_per_beat = 480
    constant_C0 = 12
    constant_note_length_ratio = 1
    constant_velocity = 64
    key_shift = KeyShift(chordSeries.key, library.KeyShiftValueDict)
    i = 0
    noteLength = 0

    midiFile = mido.MidiFile(type=0)
    track = mido.MidiTrack()
    track.append(mido.MetaMessage('key_signature', key=chordSeries.key))
    track.append(mido.MetaMessage('time_signature', numerator=chordSeries.timeSignature[0], denominator=chordSeries.timeSignature[1]))
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(chordSeries.beatPerMinute, chordSeries.timeSignature)))
    track.append(mido.Message('program_change', program=0, time=0))
    for chord in chordSeries.queue:
        if chord.endOfHarmony == True:
            end = True
        else:
            for note in chord.noteList:
                if note.identifier == 0:
                    time = int(note.restBeforeNote * constant_ticks_per_beat * constant_note_length_ratio)
                else:
                    time = 0
                notePitch = note.octave * 12 + note.position + key_shift + constant_C0
                track.append(mido.Message('note_on', note=notePitch, velocity=note.velocity, time=time))
            noteLength = int(chord.duration * constant_ticks_per_beat * constant_note_length_ratio)
            for note in chord.noteList:
                if note.identifier == 0: #if the note is the first note in chord, the delta time should be used
                    time = noteLength
                else:
                    time = 0
                notePitch = note.octave * 12 + note.position + key_shift + constant_C0
                track.append(mido.Message('note_off', note=notePitch, velocity=note.velocity, time=time))
            time = 0
    midiFile.tracks.append(track)
    midiName = 'midi_No.' + str(serialNumber) + '.mid'
    try:
        os.mkdir('./midifiles')
    except OSError:
        os.chdir('./midifiles')
    midiFile.save(midiName)
    os.chdir('../')