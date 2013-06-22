#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import os
import re

def checkData(aliasFile):
    source = open(aliasFile, "r")
    line = source.readline()
    error = 0
    tempBracket = 0
    currentLineNb = 1

    while line and not error:
        bo = line.find('{')
        bf = line.find('}')

        if bo != -1:
            error = (tempBracket == 1)
            tempBracket = 1

        elif bf != -1:
            error = (tempBracket == 0)
            tempBracket = 0
        line = source.readline()
        currentLineNb += 1

    if error:
        print("Error in file " + aliasFile + ", line %s.\n" %(currentLineNb-1))
        return True

    return False


def search(request, aliasFile):
    if checkData(aliasFile):
        return -1

    source = open(aliasFile, "r")
    tempSearch = ""
    action = ""
    line = source.readline()

    while not tempSearch and line:
        tempSearch = re.match("^\s*req=" + request, line)

        if tempSearch and request:
            tempAction = ""
            line = source.readline()
            while not tempAction and line and line.find("}") == -1:
                tempAction = re.match("/S^action=", line)
                action = line.rstrip('\t')[len("    action="):]
                line = source.readline()

        else :
            line = source.readline()

    if action:
        eval(action)
    source.close()


def main(request):
    aliasFiles = glob.glob('data/*.txt')

    for aliasFile in aliasFiles:
        search(request, aliasFile)

main("Bonjour Jarvis")
