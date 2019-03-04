#Bradley McInerney 23/08/2016
#Ver 0.0.0.1

from music21 import *
from random import randint

def numbersToStream(specs, noteInfo, timeSplit):
    stream1 = stream.Stream()
    stream1.insert(0, meter.TimeSignature(specs[0]))
    stream1.insert(0, key.Key(specs[1] + str(noteInfo[0])))

    noteList = []
    tempD = None
    tempN = None
    for pitch in noteInfo[1]:
        if pitch != "~":
            if tempN != None:
                tempN.duration = duration.Duration(tempD/timeSplit)
                noteList.append(tempN)
            tempN = note.Note(key.Key(specs[1] + str(noteInfo[0])).pitchFromDegree(pitch)) #Get the note as a note relative to the pitch
            tempD = 1
        else:
            tempD += 1
    tempN.duration = duration.Duration(tempD/timeSplit)
    noteList.append(tempN)
    stream1.append(noteList)
    return stream1
    
                   
##OPTIONS-------------------
songSpecs =     ["4/4", "D-"]
melodyNotes =   [5, [1, "~", "~", 5, 2, 1, "~", 2, 5, 4, 3, 2, 1, "~"]]
chordNotes =    [4, [1, "~", "~", "~", 2, "~", "~", "~", 5, "~", 3, "~", 1, "~"]]
##/OPTIONS------------------


outStream = stream.Score()
outStream.insert(0, numbersToStream(songSpecs, melodyNotes, 2))
outStream.insert(0, numbersToStream(songSpecs, chordNotes, 2))
outStream.show()
