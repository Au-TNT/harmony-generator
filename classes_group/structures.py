class Tree:
    __assignSeriesNum = 0 #root with seriesNum=0
    def __init__(self, node=0, branch=[], *seriesNum, **kwarg):
        if 'isEmpty' in kwarg.keys():
            self.isEmpty = kwarg.get('isEmpty')
        else:
            self.isEmpty = False
        if 'isEnd' in kwarg.keys():
            self.isEnd = kwarg.get('isEnd')
        else:
            self.isEnd = False
        if 'isRoot' in kwarg.keys():
            self.isRoot = kwarg.get('isRoot')
        else:
            self.isRoot = False
        if seriesNum != ():
            self.__assignSeriesNum = seriesNum[0]
        self.node = node
        self.branch = branch
        self.seriesNum = self.__assignSeriesNum
    def addBranch(self, newNode):
        self.__assignSeriesNum = self.__assignSeriesNum + 1
        newTree = Tree(newNode, [], self.__assignSeriesNum)
        self.branch.append(newTree)
    def traversal(self):
        list = []
        if self.branch != []:
            for branch in self.branch:
                subList = branch.traversal()
                for item in subList:
                    item.insert(0,self.node)
                    list.append(item.copy())
        else:
            list = [[self.node]]
        return list

    def replaceBranch(self, matchingSeriesNum, newBranch):
        i = 0
        while i < len(self.branch):
            if self.branch[i].seriesNum == matchingSeriesNum:
                self.branch[i] = newBranch
                break
            i = i + 1

    def copy(self):
        try:
            node = self.node.copy()
        except:
            node = self.node
        if self.isEnd:
            return Tree(node,[],self.seriesNum, isEnd=True, isEmpty=self.isEmpty, isRoot=self.isRoot)
        else:
            newBranches = []
            for subTree in self.branch:
                newBranches.append(subTree.copy())
            return Tree(node, newBranches, self.seriesNum, 
                        isEnd=self.isEnd, isEmpty=self.isEmpty, isRoot=self.isRoot
                        )
class Queue:
    queue = []
    pointer = 0
    def __init__(self, queue=[], pointer=0):
        self.queue = queue
        self.pointer = pointer
    def getCurrent(self):
        return self.queue[self.pointer-1]
    def deleteCurrent(self):
        self.pointer = self.pointer - 1
    def add(self, item):
        if self.pointer >= len(self.queue):
            self.queue.append(item)
        else:
            self.queue[self.pointer] = item
        self.pointer = self.pointer + 1
    def checkOutOfBounce(self):
        if self.pointer > len(self.queue):
            return True
        else:
            return False
    def checkLastInQueue(self):
        if self.pointer == len(self.queue):
            return True
        else:
            return False
    def resetQueue(self):
        self.queue = []
        self.pointer = 0 
    
class Returner:
    object = []
    returnCode = 0
    def __init__(self, returnCode, object=0):
        self.object = object
        self.returnCode = returnCode

class Stack:
    def __init__(self, stack, pointer):
        self.stack = stack
        self.pointer = pointer
    def add(self, item):
        if self.pointer >= len(self.stack):
            self.stack.append(item)
        else:
            self.stack[self.pointer] = item
        self.pointer = self.pointer + 1
    def pop(self):
        self.pointer -= 1
    def get(self):
        return self.stack[self.pointer-1]
    def print(self, start=0, end=-1) -> list:
        pointer = start
        list = []
        if end < 0:
            end = self.pointer+end+1
        while pointer < self.pointer and pointer < end:
            list.append(self.stack[pointer])
            pointer += 1
        return list