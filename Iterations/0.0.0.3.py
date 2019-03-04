#Bradley McInerney 15/10/2016
#Ver 0.0.0.3

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
    tempC = None
    for pitch in noteInfo[1]:
        if pitch == "~":
            #If called, extend the temp duration
            tempD += 1
        else:
            if tempC != None:
                #If there is currently a temp chord, combine with temp duration and add it to output
                tempC.duration = duration.Duration(tempD/timeSplit)
                noteList.append(tempC)

            #Create a new temp chord and add it's pitch(s) responding to the key  
            tempC = []
            for x in pitch:
                tempC.append(note.Note(key.Key(specs[1] + str(noteInfo[0][0])).pitchFromDegree(x + specs[2]))) #Get pitch in corrispondsnce to the number, key, octave and mode
            tempC = chord.Chord(tempC)
            
            tempD = 1 #Add temp duration to the temp note
            
    tempC.duration = duration.Duration(tempD/timeSplit)
    noteList.append(tempC)
    stream1.append(noteList)
    return stream1

      
###OPTIONS------------------------------------------------------------
#TimeSig, KeySig, scaleMode(0-6)
songSpecs =     ["4/4", "D-", 0] 

#[[Octave, Chord], [notes]]
melodyInfo =    [[5], [[1], "~", "~", [5], [2], [1], "~", [2], [5], [4], [3], [2], [1], "~", "~", "~"]]
chordInfo =     [[4], [[1, 3, 5], "~", "~", "~", [2, 4, 6], "~", "~", "~", [5, 7, 9], "~", [3, 5, 7], "~", [1, 3, 5], "~", "~", "~"]]


###Main---------------------------------------------------------------
outStream = stream.Score()
outStream.insert(0, noteListToStream(songSpecs, melodyInfo, 2))
outStream.insert(0, noteListToStream(songSpecs, chordInfo, 2))
outStream.show()
