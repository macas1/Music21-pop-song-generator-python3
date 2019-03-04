#Bradley McInerney 19/10/2016
#Ver 0.0.1.4

###Imports------------------------------------------------------------
from music21 import *
from random import randint, choice
import math

###Data---------------------------------------------------------------
notes = ["C", "C#", "D", "E-", "E", "F", "F#", "G", "A-", "A", "B-", "B"]

chordProgressions = [
    #Basic
    [[1], [4], [5]],
    [[1], [2], [5]],
    [[1], [6], [2], [5]],
    [[1], [3], [6], [2], [5]],
    #Blues
    [[1, 7], [4, 7], [5, 7]]
    ]    

###Functions (snippits)-----------------------------------------------
def skewedChoice(array, skew):
    total = 1
    for x in array:
        total = math.ceil(total*skew)

    total2 = int(total/skew)
    for x in array:
        if total2 <= randint(1, total):
            return x
        total2 = int(total2/skew)

def condensedChoice(array, log, skew):
    newArray = []
    newArray = array[:]

    for x in log:
        for y in array:
            for z in range(skew):
                if x != y: newArray.append(y)

    out = choice(newArray)
    log.append(out)
    return out

###Functions (unique)-------------------------------------------------
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
    first = True
    for pitch in noteInfo[1]:
        if pitch == "~":
            #Extend the current temp note duration
            if first: tempD = 0
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

        first = False
            
    addToNoteList()
    stream1.append(noteList)
    return stream1

def composeChords(specs, section):
    progression = chordProgressions[2]
    timesig = int(specs[0][0])
    length = section[1]*timesig

    out = []
    choiceLog = []
    for i in range(length):
        addChance = section[2][0] #Base chance to add a note is x/100
        if i % timesig == 0: addChance = section[2][1]

        #add continuation, rest or note
        if addChance <= randint(1, 100):
            if section[2][2] > randint(1, 100):
                out.append("r")
            else:
                out.append("~")
        elif section[2][2] > randint(1, 100):
            out.append("r")
        else:
            chord = []

            #Get random notes with higher chance of variety
            note = condensedChoice(progression, choiceLog, 20)
            
            #Add 1st, 3rd, 5th else add as hidden
            for x in range(3):
                if section[2][x+3] > randint(1, 100):
                    chord.append(note[0]+(x*2))
                else:
                    chord.append(str(note[0]+(x*2)))
                           
            #Add 2nd, 4th, 6th notes
            for x in range(3):
                if section[2][x+6][0] > randint(1, 100):
                    chord.append(note[0]+(x*2)+1)
                elif section[2][x+6][1] > randint(1, 100):
                    chord.append(str(note[0]+(x*2)+1))
            
            #add 7th note
            if section[2][9][0] > randint(1, 100):
                chord.append(note[0]+6)
            elif section[2][9][1] > randint(1, 100):
                chord.append(str(note[0]+6))
                                  
            #add other notes
            if len(note) > 1:
                for x in range(len(note)-1):
                    if x not in chord: chord.append(note[0]+note[x+1]-1)

            #Check to make sure chord not empty
            empty = True
            for x in chord:
                if isinstance(x, int): empty = False
                
            if empty:
                out.append("r")
            else:
                out.append(chord)

    return out
                                  
                
            

      
###OPTIONS------------------------------------------------------------
#TimeSig, KeySig, scaleMode(0-6)
specTimeSig = str(skewedChoice([4, 3], 5))+"/4"
specKeySig  = choice(notes)
specMode    = skewedChoice([0, randint(1, 6)], 2)
songSpecs = [specTimeSig, specKeySig, specMode]

#Base, onBeat, rest, 1st, 3rd, 5th, [2nd], [4th], [6th], [7th]. [x, y] = chance, chance to add as hidden
chordChance = [2, 95, 7, 98, 98, 98, [2, 2], [2, 2], [2, 2], [2, 15]]

#number of groups, number of bars per group, chord chance
sectionSpecs = [2, 4, chordChance]


#[[Octave, Chord], [notes]]
chordInfo = composeChords(songSpecs, sectionSpecs)
print(chordInfo)


###Main---------------------------------------------------------------
outStream = stream.Score()
#outStream.insert(0, noteListToStream(songSpecs, melodyInfo, 2))
outStream.insert(0, noteListToStream(songSpecs, [[3], chordInfo], 1))
outStream.show()
