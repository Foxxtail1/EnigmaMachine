from typing import List, Dict
from Rotor import Rotor

class MyToolKit:

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, charSet: str = alphabet):
        self.reflector: dict[int, int] = MyToolKit.genReflector(len(charSet))
        self.alphaNum: dict[chr, int] = MyToolKit.genAlphaNum(charSet)
        self.numAlpha: dict[int, chr] = MyToolKit.flipAlphaNum(self.alphaNum)

    def genRotor(self, outWireing: str) -> Rotor:
        outBound = {}
        outW = [char for char in outWireing]
        i = 0
        while i < len(outW):
            outBound[i] = self.alphaNum[outW[i]]
            i += 1

        return Rotor(outBound)
    
    @staticmethod
    def genAlphaNum(charSet: str) -> Dict[chr, int]:
        output = {}
        charaArray = [char for char in charSet]
        i = 0 
        while i < len(charaArray):
            output[charaArray[i]] = i
            i += 1
        return output
    
    @staticmethod
    def flipAlphaNum(charaArray: Dict[chr, int]) -> Dict[int, chr]:
        return {v: k for k, v in charaArray.items()}

    @staticmethod
    def genReflector(setLength: int) -> Dict[int, int]:
        output = {}
        i = 0
        while i < setLength:
            output[i] = setLength - i
            i += 1
        return output
    
    @staticmethod
    def genPlugboard(plugboard: Dict[chr, chr]) -> Dict[chr, chr]:
        outputBoard = plugboard.copy()
        for k,v in plugboard.items():
            outputBoard[v] = k
        return outputBoard