def MultiTraversal(list:list, numberOfMemberInGroup:int):
    i = 0
    combinationList = []
    n = numberOfMemberInGroup
    if n > len(list) or n < 0:
        return []
    elif n == 0:
        return [[]]
    elif n == 1:
        for item in list:
            combinationList.append([item])
        return combinationList
    while i < len(list):
        item = list[i]
        listCopy = list.copy()
        del listCopy[i]
        subCombinationList = MultiTraversal(listCopy, numberOfMemberInGroup - 1)
        for combination in subCombinationList:
            combination.insert(0,item)
            combinationList.append(combination)
        i = i + 1
    return combinationList

def DeleteIdenticals(list:list, ordered:bool, sort=True): #ordered = True: do not delete list with identical items but in different order
    i = 0
    deleteNeeded = False
    while i < len(list):
        listCopy = [subList[:] for subList in list]
        del listCopy[i]
        for item in listCopy:
            if ordered:
                if item == list[i]:
                    deleteNeeded = True
            elif not ordered:
                if sorted(item) == sorted(list[i]):
                    deleteNeeded = True
        if deleteNeeded:
            del list[i]
        else:
            i = i + 1
        deleteNeeded = False
    if sort:
        i = 0
        while i < len(list):
            list[i].sort()
            i = i + 1
    return list

def limitRange(num:float, roof:float, floor:float):
    if num > roof:
        return roof
    elif num < floor:
        return floor
    else:
        return num
    
def isfloat(str:str):
    if isinstance(str, int) or isinstance(str, float):
        return True
    try:
        float(str)
        return True
    except:
        return False
    
def KeyShift(key, keyShiftValueDict):
    if key in keyShiftValueDict.keys():
        keyShiftValue = keyShiftValueDict.get(key)
    else:
        keyShiftValue = 0
    return keyShiftValue
