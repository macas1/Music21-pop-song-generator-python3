#Bradley McInerney 23/08/2016
#Ver 0.0.0.2

###Imports------------------------------------------------------------
from music21 import *
from random import randint

###Functions----------------------------------------------------------
def noteListToStream(specs, noteInfo, timeSplit):
    stream1 = stream.Stream()
    stream1.insert(0, meter.TimeSignature(specs[0]))
    stream1.insert(0, key.Key(specs[1] + str(noteInfo[0][0])))

    noteList = []
    tempD = None
    tempN = None
    for pitch in noteInfo[1]:
        if pitch != "~":
            if tempN != None:
                tempN.duration = duration.Duration(tempD/timeSplit)
                noteList.append(tempN)
                
            #Get the note as a note relative to the key
            if isinstance(pitch, list):
                tempN = []
                for x in pitch:
                    tempN.append(note.Note(key.Key(specs[1] + str(noteInfo[0][0])).pitchFromDegree(x + specs[2])))
                tempN = chord.Chord(tempN)
            else:
                tempN = note.Note(key.Key(specs[1] + str(noteInfo[0][0])).pitchFromDegree(pitch + specs[2]))
            
            tempD = 1
        else:
            tempD += 1
    tempN.duration = duration.Duration(tempD/timeSplit)
    noteList.append(tempN)
    stream1.append(noteList)
    return stream1

      
###OPTIONS------------------------------------------------------------
#TimeSig, KeySig, scaleMode(0-6)
songSpecs =     ["4/4", "D-", 0] 

#[[Octave, Chord], [notes]]
melodyInfo =    [[5], [1, "~", "~", 5, 2, 1, "~", 2, 5, 4, 3, 2, 1, "~", "~", "~"]]
chordInfo =     [[4], [[1, 3, 5], "~", "~", "~", [2, 4, 6], "~", "~", "~", [5, 7, 9], "~", [3, 5, 7], "~", [1, 3, 5], "~", "~", "~"]]


###Main---------------------------------------------------------------
outStream = stream.Score()
outStream.insert(0, noteListToStream(songSpecs, melodyInfo, 2))
outStream.insert(0, noteListToStream(songSpecs, chordInfo, 2))
outStream.show()
