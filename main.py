# -*- coding: utf-8 -*-
#Harmony Generator by Kevin Jin
#Last edit: Feburary 12th, 2025

from procession import *
from classes_group.applical import *
from error_operations import errorReturn
from classes_group.structures import Returner
from configs import writeConfig

VERSION = "1.3"
exit = False
successInput = False

while not exit:
    print(f"Harmony generator version {VERSION}\n1. start the main program, 2. change configurations, 3. about the program, enter 'exit' to exit the program")
    while not successInput:
        selection = input('selection:')
        if selection not in {'1','2','3', 'exit'}:
            print('invalid selection, please try again')
        else:
            successInput = True
    if selection == '1':
        initiate()
        melody = NoteSeries([], 0)
        harmony = ChordSeries([],0)
        returner = inputAll()
        i = 1
        if returner.returnCode < 0:
            errorReturn(returner.returnCode)
            error = True
        else:
            melody = returner.object
            error = False

        if not error:
            generateVoicingToCache(melody)
            harmonyList = buildHarmony(melody)
            print('start outputting...')
            if harmonyList == []:
                print('no harmony avaliable')
            for harmonyToPrint in harmonyList:

                printHarmony(harmonyToPrint, serialNumber = i)
                i = i + 1
    elif selection == '2':
        writeConfig()
    elif selection == '3':
        print('Informations to be filled out.')
    elif selection == 'exit':
        exit = True
    successInput = False