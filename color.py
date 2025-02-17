from classes_group import analytics
import library
from tools import MultiTraversal, DeleteIdenticals


def function_component_calculator(noteList:list, bass:int):
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
    return chordComponent

def function_square_difference(componentOne, componentTwo):
    differenceDict = {}
    totalDifference = 0
    for key in componentOne.keys():
        valueOne = componentOne.get(key)
        valueTwo = componentTwo.get(key)
        difference = valueOne - valueTwo
        if difference <= 0:
            squareDifference = difference * difference
        else:
            squareDifference = -difference * difference
        differenceDict[key] = squareDifference
        totalDifference = totalDifference + difference * difference #abs(squareDifference)
    differenceDict["total"] = totalDifference
    #print(totalDifference)
    return differenceDict

def createIntervalDict(noteList:list):
    intervalDict = {0 : 0, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0}
    combinationList = DeleteIdenticals(MultiTraversal(noteList, 2), False)
    for combination in combinationList:
        if combination[0] > combination [1]:
            interval = combination[0] - combination[1]
        else:
            interval = combination[1] - combination[0]
        if interval > 6: #anything larger than tritone will be changed to the complementary of itself
            interval = 12 - interval
        intervalDict[interval] = intervalDict[interval] + 1
    return intervalDict

def tension_calculator(intervalDict:dict):
    tension = 0
    weight = library.TensionWeight
    for key, value in intervalDict.items():
        tension = tension + weight.get(key)*value
    if intervalDict.get(4) - intervalDict.get(3) >= 2:#Augmented fifth
        tension = tension + weight.get("aug5")
        #print("aug5")
    if intervalDict.get(3) - intervalDict.get(4) >=3:#Diminished seventh
        tension = tension + weight.get("dim7")
        #print("dim7")
    return tension

def mood_calculator(noteList:list, bass:int, tension:int):
    ABSOLUTE_MINOR = -100
    ABSOLUTE_MAJOR = 100
    mood = 0
    consistedInterval = []
    for note in noteList:
        interval = note - bass
        if interval < 0:
            interval = interval + 12
        intervalMoodValue = library.Mood_IntervalWeight.get(interval)
        if interval not in consistedInterval:
            mood += intervalMoodValue
        consistedInterval.append(interval)
    mood = mood * library.Mood_TensionDilution(tension)
    return round(mood,1)

def tritone_tendency(third:int, seventh:int) -> list:
    tendencyList = [[(third+1)%12,(seventh-1)%12],
                    [(third+1)%12,(seventh-2)%12],
                    [(third+2)%12,(seventh-1)%12],
                    [(seventh+1)%12,(third-1)%12],
                    [(seventh+1)%12,(third-2)%12],
                    [(seventh+2)%12,(third-1)%12]]
    return tendencyList





'''
i = 0
chordList = []
bassList = []  
while i < 2:       
    noteList = []
    string = input(':')
    noteBassData = string.split('_')
    bassList.append(int(noteBassData[1]))
    rawNoteList = noteBassData[0].split(',')
    for note in rawNoteList:
        noteList.append(int(note))
    chordList.append(noteList)
    i = i + 1
componentOne = function_component_calculator(chordList[0], bassList[0])
componentTwo = function_component_calculator(chordList[1], bassList[1])
function_square_difference(componentOne, componentTwo)
'''
'''
print(DeleteIdenticals(MultiTraversal([1,2,3,4], 3), False))
print(createIntervalDict([5,9,0,3,6,2]))
print(tension_calculator(createIntervalDict([11,3,5,8])))
'''
if __name__ == '__main__':
    chord = [0,4,7,11]
    chordTwo = [5,9,0]
    bass = 0
    bassTwo = 5
    print(tension_calculator(createIntervalDict(chord)))
    print(mood_calculator(chord, bass, tension_calculator(createIntervalDict(chord))))
    print(function_square_difference(function_component_calculator(chord,bass), function_component_calculator(chordTwo,bassTwo)))
