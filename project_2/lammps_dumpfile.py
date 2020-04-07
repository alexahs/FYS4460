import numpy as np
import os


class File:
    def __init__(self, filename, nTimesteps, dumpFrequency, nDims = 3):
        self.dataDict = {}
        self.keywords = []
        self.nTimesteps = nTimesteps
        self.dumpFrequency = dumpFrequency
        self.nWindows = floor(nTimesteps / dumpFrequency) + 1
        self.nDims = nDims
        self.dumpfile = open(filename, "r")
        self.read_file_to_dict()

    def read_file_to_dict(self):
        nInfoLines = 6 + self.nDims
        contents = self.dumpfile.readlines()

        assert("ITEM: NUMBER OF ATOMS" in contens[2].split())
        self.nAtoms = int(contents[3].split())

        assert("ITEM: BOX BOUNDS" in contens[4].split())
        boxBounds = contents[5].split()
        self.boundsMin = float(boxBounds[0])
        self.boundsMax = float(boxBounds[1])

        tempKeywords = contents[nInfoLines].split()
        assert("ATOMS:" in tempKeywords[0])
        for k in range(4, len(tempKeywords)):
            self.keywords.append(tempKeywords[k])

        for T in range(nWindows):
            # self.dataDict[f"T{T}"] = {}
            tempDict = {}
            for k in range(len(self.keywords)):
                tempDict[self.keywords[k]] = np.zeros((self.nAtoms, ))
            for i in range(self.nAtoms):

                tempDict
