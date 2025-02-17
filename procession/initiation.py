import os

def initiate():
    print('initiating...')
    runtimeLog = open("runtime_log.txt", 'w')
    runtimeLog.close()
    open("chord_list_log.txt", 'w').close()
    try:
        os.chdir("./midifiles")
        for file in os.listdir("./"):
            os.remove(file)
        os.chdir("../")
    except:
        os.mkdir("./midifiles")
    try:
        os.chdir("./caches")
        os.chdir("../")
        '''
        for file in os.listdir("./"):
            os.remove(file)
        os.chdir("../")
        '''
    except:
        os.mkdir("./caches")
