#Bradley McInerney 15/10/2016
#Ver 0.0.0.4

###Imports------------------------------------------------------------
from music21 import *
from random import randint

###Functions----------------------------------------------------------
def noteListToStream(specs, noteInfo, timeSplit):
    def addToNoteList():
        tempN.duration = duration.Duration(tempD/timeSplit)
        noteList.append(tempN)
    
    stream1 = stream.Stream()
    stream1.insert(0, meter.TimeSignature(specs[0]))
    stream1.insert(0, key.Key(specs[1] + str(noteInfo[0][0])))

    noteList = []
    tempD = None
    tempN = None
    for pitch in noteInfo[1]:
        print(pitch)
        if pitch == "~":
            #Extend the current temp note duration
            tempD += 1
        elif pitch == "r":
            if tempN != None: addToNoteList() #If there is a current temp note, end it
            #Add a rest
            tempN = note.Rest()
            tempD = 1
        else:
            if tempN != None: addToNoteList() #If there is currently a temp note, combine with temp duration and add it to output
            #Create a new temp chord and add it's pitch(s) responding to the key with the duration of 1
            tempN = []
            for x in pitch:
                if isinstance(x, int): tempN.append(note.Note(key.Key(specs[1] + str(noteInfo[0][0])).pitchFromDegree(x + specs[2]))) #Get pitch in corrispondsnce to the number, key, octave and mode
            tempN = chord.Chord(tempN)
            tempD = 1
            
    addToNoteList()
    stream1.append(noteList)
    return stream1

      
###OPTIONS------------------------------------------------------------
#TimeSig, KeySig, scaleMode(0-6)
songSpecs =     ["4/4", "D-", 0] 

#[[Octave, Chord], [notes]]
melodyInfo =    [[5], [[0, -2], "~", "r", [5], [2], [1], "~", [2], [5], [4], [3], [2], [1], "~", "~", "~"]]
chordInfo =     [[4], [[1, 3, 5, "7"], "~", "~", "~", [2, 4, 6], "~", "~", "~", [5, 7, 9], "~", [3, 5, 7], "~", [1, 3, 5], "~", "~", "~"]]


###Main---------------------------------------------------------------
outStream = stream.Score()
outStream.insert(0, noteListToStream(songSpecs, melodyInfo, 2))
outStream.insert(0, noteListToStream(songSpecs, chordInfo, 2))
outStream.show()
