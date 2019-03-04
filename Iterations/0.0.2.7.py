#Bradley McInerney 30/10/2016
#Ver 0.0.2.7

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
    #[[1, 7], [4, 7], [5, 7]]
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

def alignToList(num, array, closest=True):
    
    a = array[:]
    a.sort()

    #Definate outputs
    if num in a: return num
    if num < a[0]: return a[0]
    if num > a[len(a)-1]: return a[len(a)-1]

    #Chance outputs
    pos = -1
    for x in a:
        if x < num:
            pos += 1
        else:
            break

    low  = num - a[pos]
    high = a[pos+1] - num
    
    if high < low:
        if closest:
            return a[pos]
        else:
            return skewedChoice([a[pos+1], a[pos]], low-high)
    elif low < high:
        if closest:
            return a[pos]
        else:
            return skewedChoice([a[pos], a[pos+1]], high-low)
    else:
        return a[pos + randint(0, 1)]


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
    progression = choice(chordProgressions)
    timesig = int(specs[0][0])
    length = section[0]*timesig

    out = []
    choiceLog = []
    for i in range(length):
        addChance = section[1][0] #Base chance to add a note is x/100
        if i % timesig == 0: addChance = section[1][1]

        #add continuation, rest or note
        if addChance <= randint(1, 100):
            if section[1][2] > randint(1, 100):
                out.append("r")
            else:
                out.append("~")
        elif section[1][2] > randint(1, 100):
            out.append("r")
        else:
            chord = []

            #Get random notes with higher chance of variety
            note = condensedChoice(progression, choiceLog, 20)
            
            #Add 1st, 3rd, 5th else add as hidden
            for x in range(3):
                if section[1][x+3] > randint(1, 100):
                    chord.append(note[0]+(x*2))
                else:
                    chord.append(str(note[0]+(x*2)))
                           
            #Add 2nd, 4th, 6th notes
            for x in range(3):
                if section[1][x+6][0] > randint(1, 100):
                    chord.append(note[0]+(x*2)+1)
                elif section[1][x+6][1] > randint(1, 100):
                    chord.append(str(note[0]+(x*2)+1))
            
            #add 7th note
            if section[1][9][0] > randint(1, 100):
                chord.append(note[0]+6)
            elif section[1][9][1] > randint(1, 100):
                chord.append(str(note[0]+6))
                                  
            #add other notes
            if len(note) > 1:
                for x in range(len(note)-1):
                    if note[x+1] not in chord: chord.append(note[0]+note[x+1]-1)

            #Check to make sure chord not empty
            empty = True
            for x in chord:
                if isinstance(x, int): empty = False
                
            if empty:
                out.append("r")
            else:
                out.append(chord)
    return out
                                  
def composeMelody(specs, section):
    timesig = int(specs[0][0])
    length = section[0]*timesig

    out = []
    note = randint(1, 7)
    for i in range(length):
        addChance = section[1][0] #Base chance to add a note is x/100
        
        #add continuation, rest or note
        if addChance <= randint(1, 100):
            if section[1][1] > randint(1, 100):
                out.append("r")
            else:
                out.append("~")
        elif section[1][1] > randint(1, 100):
            out.append("r")
        else:
            chord = []

            #Get random notes depending on unison and conjunct
            if section[1][2] <= randint(1, 100):
                #Conjunct
                if section[1][3] > randint(1, 100):
                    if note == 1:
                        note += 1
                    elif note == 7:
                        note -= 1
                    else:
                        note += choice([-1, 1])
                #Disjunct
                else:
                    options = [1, 2, 3, 4, 5, 6, 7]
                    if note in options: options.remove(note)
                    if note-1 in options: options.remove(note-1)
                    if note+1 in options: options.remove(note+1)
                    note = choice(options)
            chord.append(note)
            
            #Add other notes into a chord
            for x in range(6):
                if section[1][x+4] > randint(1, 100): chord.append(note+x)

            out.append(chord)
    return out

def alignMelody(melodyList1, chordList1):
    melodyList = melodyList1[:]
    chordList = chordList1[:]

    for grouping in range(len(melodyList)):
        if (not isinstance(chordList[grouping], str)) and (not isinstance(melodyList[grouping], str)):
            #Re-create the grouping with integers instead of the strings
            newGroup = []
            for x in range(len(chordList[grouping])):
                newGroup.append(int(chordList[grouping][x]))
                           
            #Align notes and add to new array
            newNotes = []
            for note in melodyList[grouping]:
                newNote = alignToList(note, newGroup, False)
                #Note sure yet what to do when both notes return the same, so for now I am ignoring it
                if newNote not in newNotes: newNotes.append(newNote)
            melodyList[grouping] = newNotes
    return(melodyList)


def changeMelody_KeepStructure(melodyList1, section):
    melodyList = melodyList1[:]

    note = randint(1, 7)
    for grouping in range(len(melodyList)):
        if not isinstance(melodyList[grouping], str): #Only change numbers
            chord = []

            #Get random notes depending on unison and conjunct
            if section[1][2] <= randint(1, 100):
                #Conjunct
                if section[1][3] > randint(1, 100):
                    if note == 1:
                        note += 1
                    elif note == 7:
                        note -= 1
                    else:
                        note += choice([-1, 1])
                #Disjunct
                else:
                    options = [1, 2, 3, 4, 5, 6, 7]
                    if note in options: options.remove(note)
                    if note-1 in options: options.remove(note-1)
                    if note+1 in options: options.remove(note+1)
                    note = choice(options)
            chord.append(note)
            
            #Add other notes into a chord
            for x in range(6):
                if section[1][x+4] > randint(1, 100): chord.append(note+x)

            melodyList[grouping] = chord

    return melodyList

def change_doubleDurations(List):
    out = []
    count = 0
    for x in List:
        out.append(x)
        out.append("~")
    return out

def change_invert(List, center):
    #Center = 1 will invert around the base note
    #Center = 4 will invert around the middle note (out of all 7 notes)
    out = []
    for grouping in List:
        #Ignore non-notes
        if isinstance(grouping, str):
            out.append(grouping)
        else:
            newGroup = []
            for note in grouping:
                #invert notes around center
                newGroup.append(note-((note-center)*2))
            out.append(newGroup)
    return out

def debug_unison(List):
    out = []
    for grouping in List:
        #Ignore non-notes
        if isinstance(grouping, str):
            out.append(grouping)
        else:
            newGroup = []
            for note in grouping:
                if note not in newGroup: newGroup.append(note)
            out.append(newGroup)
    return out
            
               
###OPTIONS------------------------------------------------------------
#TimeSig, KeySig, scaleMode(0-6)
specTimeSig = str(skewedChoice([4, 3], 5))+"/4"
specKeySig  = choice(notes)
specMode    = skewedChoice([0, randint(1, 6)], 2)
songSpecs = [specTimeSig, specKeySig, specMode]

#Base, rest, unison, conjunct, 2nd, 3rd, 4th, 5th, 6th, 7th
melodyChance = [60, 10, 15, 60, 2, 2, 2, 2, 2, 2]

#number of groups, number of bars per group, chances
section1Specs = [4, melodyChance]

#Base, onBeat, rest, 1st, 3rd, 5th, [2nd], [4th], [6th], [7th]. [x, y] = chance, chance to add as hidden
chordChance = [2, 97, 5, 98, 98, 98, [2, 2], [2, 4], [2, 5], [5, 3]]

#number of groups, number of bars per group, chances
section2Specs = [4, chordChance]

#Create a sequence: choras - verse - choras
melodyInfo = composeMelody(songSpecs, section1Specs)
melodyInfo = (melodyInfo + change_invert(melodyInfo, choice([1, 4])) + melodyInfo + composeMelody(songSpecs, section1Specs))*2
melodyInfo = debug_unison(melodyInfo)
chordInfo = change_doubleDurations(composeChords(songSpecs, section2Specs)) * 4

#output
print(chordInfo)
print("-----------------------")
print(melodyInfo)
print("-----------------------")
melodyInfo = alignMelody(melodyInfo, chordInfo)
print(melodyInfo)

###Main---------------------------------------------------------------
compression = 2 #choice([0.5, 1, 2, 3, 4])
print("->", compression)
outStream = stream.Score()
outStream.insert(0, noteListToStream(songSpecs, [[4], melodyInfo], compression))
outStream.insert(0, noteListToStream(songSpecs, [[3], chordInfo], compression))
outStream.show()
